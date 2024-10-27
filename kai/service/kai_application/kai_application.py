import logging
import re
import time
import traceback
from difflib import unified_diff
from typing import Iterator, Optional, cast

import tiktoken
from aiohttp import web
from langchain_core.messages import BaseMessage, BaseMessageChunk
from pydantic import BaseModel, ConfigDict

from kai.kai_trace import KaiTrace
from kai.models.file_solution import guess_language, parse_file_solution_content
from kai.models.kai_config import KaiConfig
from kai.models.report_types import ExtendedIncident
from kai.service.incident_store.backend import incident_store_backend_factory
from kai.service.incident_store.incident_store import IncidentStore
from kai.service.kai_application.util import (
    BatchMode,
    batch_incidents,
    get_prompt,
    playback_if_demo_mode,
)
from kai.service.llm_interfacing.model_provider import ModelProvider
from kai.service.solution_handling.consumption import solution_consumer_factory
from kai.service.solution_handling.detection import solution_detection_factory
from kai.service.solution_handling.production import solution_producer_factory

KAI_LOG = logging.getLogger(__name__)


# TODO: Possibly merge with FileSolutionContent?
class UpdatedFileContent(BaseModel):
    updated_file: str
    total_reasoning: list[str]
    used_prompts: list[str]
    model_id: str
    additional_information: list[str]
    response_metadatas: list[dict]

    llm_results: Optional[list[str | list[str | dict]]]

    # "model_" is a Pydantic protected namespace, so we must remove it
    model_config = ConfigDict(protected_namespaces=())


class KaiApplication:
    """
    A Kai application that can be used to interact with the LLM and incident
    store. Its main job is to generate "fixes" for given incidents.
    """

    def __init__(self, config: KaiConfig):
        self.config = config

        if config.trace_enabled:
            KAI_LOG.info("Tracing enabled.")

        if config.demo_mode:
            KAI_LOG.info("KAI__DEMO_MODE enabled. LLM responses will be cached.")

        # Create model provider

        self.model_provider = ModelProvider(config.models)

        KAI_LOG.info(f"Selected provider: {config.models.provider}")
        KAI_LOG.info(f"Selected model: {self.model_provider.model_id}")

        # Create incident store

        backend = incident_store_backend_factory(config.incident_store.args)

        solution_detector = solution_detection_factory(
            config.incident_store.solution_detectors
        )

        solution_producer = solution_producer_factory(
            config.incident_store.solution_producers, self.model_provider
        )

        self.incident_store = IncidentStore(
            backend,
            solution_detector,
            solution_producer,
        )

        # Create Tiktoken configurations
        self.tiktoken_encoding_base = self.config.token_estimation_encoding_base
        KAI_LOG.info(f"Encoding base selected: {self.tiktoken_encoding_base}")

        KAI_LOG.info(f"Selected incident store: {config.incident_store.args.provider}")

        # Create solution consumer

        self.solution_consumer = solution_consumer_factory(config.solution_consumers)

    def is_response_request_merge_needed(self, content: str):
        comments_pattern = r"(Rest of the code remains unchanged)|(rest of the code remains the same)|(Other methods remain unchanged)|(Rest of the class remains unchanged)|(Rest of the methods remain unchanged)"
        comments_pattern_matches = re.findall(comments_pattern, content, re.DOTALL)
        if comments_pattern_matches:
            return True

    def merging_response(self, input_file: str, llm_response: str) -> str:
        diff_output = unified_diff(
            llm_response.splitlines(), input_file.splitlines(), lineterm=""
        )
        diff_lines = "\n".join(list(diff_output))
        diff_line_list = diff_lines.splitlines()

        updated_lines = [line for line in diff_line_list]
        backtick_indices = []
        commented_text = ""

        commented_line_index = 1

        for line in updated_lines:
            if "Rest of" in line:
                commented_line_index += updated_lines.index(line)
                commented_text += line
            if "```" in line:
                backtick_indices.append(updated_lines.index(line))

        cleaned_comment_text = commented_text.replace("-", "").strip()
        extracted_code = ""
        for i in range(commented_line_index, backtick_indices[1]):
            if "+" in updated_lines[i]:
                extracted_code += updated_lines[i].replace("+", "") + "\n"

        return llm_response.replace(cleaned_comment_text, extracted_code)

    def estimating_prompt_tokens(self, prompt: str) -> int:
        try:
            enc = tiktoken.encoding_for_model(self.tiktoken_encoding_base)
            return len(enc.encode(prompt))
        except KeyError as e:
            KAI_LOG.warning(f"Encoding base could not be found {e}")
            return 0

    def has_tokens_exceeded(
        self, response_metadata: dict, estimated_tokens: int, file_name: str
    ):
        """Checks if the token usage exceeds the estimated limit and logs a warning."""

        token_keys = [
            "prompt_token_count",
            "prompt_tokens",
            "input_prompt",
            "input_tokens",
        ]
        key_found = False
        for key, value in response_metadata.items():
            if isinstance(value, dict):
                for token in token_keys:
                    actual_prompt_tokens = value.get(token)
                    if actual_prompt_tokens:
                        if (
                            isinstance(actual_prompt_tokens, int)
                            and actual_prompt_tokens > estimated_tokens
                        ):
                            key_found = True
                            KAI_LOG.warning(
                                f"{file_name} exceeds the estimated token count. Estimated Tokens: {estimated_tokens}, Actual Tokens: {actual_prompt_tokens}. Consider reducing the prompt size."
                            )
                        else:
                            key_found = True
                            return None
            else:
                if key in token_keys:
                    if isinstance(value, int) and value > estimated_tokens:
                        key_found = True
                        KAI_LOG.warning(
                            f"{file_name} exceeds the estimated token count. Estimated Tokens: {estimated_tokens}, Actual Tokens: {value}. Consider reducing the prompt size."
                        )
                    else:
                        key_found = True
                        return None

        if key_found is False:
            KAI_LOG.warning(
                "None of the token key are not found in the response metadata. Please verify the response metadata for the specified model."
            )

    def get_incident_solutions_for_file(
        self,
        file_name: str,
        file_contents: str,
        application_name: str,
        incidents: list[ExtendedIncident],
        batch_mode: BatchMode = BatchMode.SINGLE_GROUP,
        include_solved_incidents: bool = True,
        include_llm_results: bool = False,
        trace: Optional[KaiTrace] = None,
    ):
        """
        Get the updated file content for a given file and set of incidents.

        TODO: Add checks on the incidents' uri to ensure they all match
        file_name.
        """

        if trace is None:
            trace = KaiTrace(
                trace_enabled=self.config.trace_enabled,
                log_dir=self.config.log_dir,
                model_id=self.model_provider.model_id,
                batch_mode=batch_mode,
                application_name=application_name,
                file_name=file_name,
            )

        src_file_language = guess_language(file_contents, filename=file_name)
        KAI_LOG.debug(f"{file_name} classified as language {src_file_language}")

        result = UpdatedFileContent(
            updated_file=file_contents,
            total_reasoning=[],
            used_prompts=[],
            model_id=self.model_provider.model_id,
            additional_information=[],
            response_metadatas=[],
            llm_results=[] if include_llm_results else None,
        )

        batched_incidents = batch_incidents(incidents, batch_mode)

        for count, (_group_by, incidents) in enumerate(batched_incidents, 1):
            KAI_LOG.info(
                f"Processing incident batch {count}/{len(batched_incidents)} with {len(incidents)} incident(s) for {file_name}"
            )

            # Transform incidents into a format that can be passed to Jinja

            pb_incidents = [incident.model_dump() for incident in incidents]

            for pb_incident in pb_incidents:
                if include_solved_incidents:
                    solutions = self.incident_store.find_solutions(
                        pb_incident["ruleset_name"],
                        pb_incident["violation_name"],
                        pb_incident["variables"],
                        pb_incident["code_snip"],
                    )

                    if len(solutions) != 0:
                        solution_str = self.solution_consumer(solutions[0])

                        if len(solution_str) != 0:
                            pb_incident["solution_str"] = solution_str

            pb_vars = {
                "src_file_name": file_name,
                "src_file_language": src_file_language,
                "src_file_contents": result.updated_file,
                "incidents": pb_incidents,
                "model_provider": self.model_provider,
            }

            # Render the prompt

            prompt = get_prompt(self.model_provider.template, pb_vars)
            estimated_prompt_tokens = self.estimating_prompt_tokens(prompt)
            trace.prompt(count, prompt, pb_vars)

            # Send the prompt to the llm

            KAI_LOG.debug(f"Sending prompt: {prompt}")
            llm_result = None
            for retry_attempt_count in range(self.model_provider.llm_retries):
                try:
                    with playback_if_demo_mode(
                        self.config.demo_mode,
                        self.model_provider.model_id,
                        application_name,
                        f'{file_name.replace("/", "-")}',
                    ):
                        llm_request = [("human", prompt)]
                        llm_result = self.model_provider.llm.invoke(llm_request)
                        content = parse_file_solution_content(
                            src_file_language, str(llm_result.content)
                        )

                        # The LLM response must include code blocks (formatted within triple backticks) to be considered complete. Usually, the LM responds with code blocks, but occasionally it fails to do so, as noted in issue #350 [https://github.com/konveyor/kai/issues/350] . Complete responses are saved in the trace directory directly. For incomplete responses, an additional prompt is sent to the LLM, and the resulting complete response (with code blocks) is saved in the trace directory as a new file.
                        if len(content.updated_file) == 0:
                            trace.llm_result(
                                count,
                                retry_attempt_count,
                                llm_result.content,
                                "llm_result_without_codeblocks",
                            )
                            trace.response_metadata(
                                count,
                                retry_attempt_count,
                                llm_result.response_metadata,
                                "response_metadata_without_codeblocks.json",
                            )
                            self.has_tokens_exceeded(
                                llm_result.response_metadata,
                                estimated_prompt_tokens,
                                file_name,
                            )
                            llm_request.append(
                                (
                                    "human",
                                    "I request you to generate a complete response.",
                                )
                            )
                            llm_result = self.model_provider.llm.invoke(llm_request)
                            content = parse_file_solution_content(
                                src_file_language, str(llm_result.content)
                            )

                        trace.llm_result(
                            count,
                            retry_attempt_count,
                            llm_result.content,
                            "llm_result_with_codeblocks",
                        )
                        trace.response_metadata(
                            count,
                            retry_attempt_count,
                            llm_result.response_metadata,
                            "response_metadata_with_codeblocks.json",
                        )
                        trace.estimated_tokens(
                            count,
                            retry_attempt_count,
                            estimated_prompt_tokens,
                            self.tiktoken_encoding_base,
                        )
                        self.has_tokens_exceeded(
                            llm_result.response_metadata,
                            estimated_prompt_tokens,
                            file_name,
                        )

                        if self.is_response_request_merge_needed(
                            str(llm_result.content)
                        ):
                            KAI_LOG.warning("This file contains unnecessary comments.")
                            new_llm_response = self.merging_response(
                                prompt, str(llm_result.content)
                            )
                            trace.llm_result(
                                count,
                                retry_attempt_count,
                                new_llm_response,
                                "llm_result_with_no_unnecessary_comments",
                            )

                        if not content.updated_file:
                            raise Exception(
                                f"Error in LLM Response: The LLM did not provide an updated file for {file_name}"
                            )

                        result.updated_file = content.updated_file
                        result.used_prompts.append(prompt)
                        result.total_reasoning.append(content.reasoning)
                        result.response_metadatas.append(llm_result.response_metadata)
                        result.additional_information.append(content.additional_info)
                        if include_llm_results:
                            result.llm_results = cast(
                                list[str | list[str | dict]], result.llm_results
                            )
                            result.llm_results.append(str(llm_result.content))

                        break
                except Exception as e:
                    KAI_LOG.warn(
                        f"Request to model failed for batch {count}/{len(batched_incidents)} for {file_name} with exception {e}, retrying in {self.model_provider.llm_retry_delay}s\n{e}"
                    )
                    KAI_LOG.debug(traceback.format_exc())
                    trace.exception(
                        count, retry_attempt_count, e, traceback.format_exc()
                    )
                    time.sleep(self.model_provider.llm_retry_delay)
            else:
                KAI_LOG.error(f"{file_name} failed to migrate")

                # TODO: These should be real exceptions
                raise web.HTTPInternalServerError(
                    reason="Migration failed",
                    text=f"The LLM did not generate a valid response: {llm_result}",
                )

        return result

    # NOTE(@JonahSussman): This function should probably become deprecated at
    # some point. `get_incident_solutions_for_file` does everything this
    # function does, aside from streaming.
    def get_incident_solution(
        self,
        application_name: str,
        ruleset_name: str,
        violation_name: str,
        incident_snip: Optional[str],
        incident_variables: dict,
        file_name: str,
        file_contents: str,
        line_number: int,
        analysis_message: str,
        stream: bool = False,
    ) -> Iterator[BaseMessageChunk] | BaseMessage:
        KAI_LOG.info(
            f"START - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{self.model_provider.model_id}'"
        )

        start = time.time()

        solved_incidents = self.incident_store.find_solutions(
            ruleset_name,
            violation_name,
            incident_variables,
            incident_snip,
        )

        KAI_LOG.debug(f"Found {len(solved_incidents)} solved incident(s)")

        pb_vars = {
            "src_file_name": file_name,
            "src_file_contents": file_contents,
            "line_number": str(line_number),
            "analysis_message": analysis_message,
        }

        if len(solved_incidents) >= 1:
            pb_vars["solution_str"] = self.solution_consumer(solved_incidents[0])

        prompt = get_prompt(self.model_provider.template, pb_vars)

        if stream:
            end = time.time()
            KAI_LOG.info(
                f"END - completed in '{end-start}s: - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{self.model_provider.model_id}'"
            )
            return self.model_provider.llm.stream(prompt)
        else:
            llm_result = self.model_provider.llm.invoke(prompt)

            end = time.time()
            KAI_LOG.info(
                f"END - completed in '{end-start}s: - App: '{application_name}', File: '{file_name}' '{ruleset_name}'/'{violation_name}' @ Line Number '{line_number}' using model_id '{self.model_provider.model_id}'"
            )
            return llm_result
