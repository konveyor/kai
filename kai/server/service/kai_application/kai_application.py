import logging
import time
import traceback
from typing import Iterator, Optional

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

        KAI_LOG.info(f"Selected incident store: {config.incident_store.args.provider}")

        # Create solution consumer

        self.solution_consumer = solution_consumer_factory(config.solution_consumers)

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
                        llm_result = self.model_provider.llm.invoke(prompt)
                        trace.llm_result(count, retry_attempt_count, llm_result)

                        content = parse_file_solution_content(
                            src_file_language, llm_result.content
                        )

                        if not content.updated_file:
                            raise Exception(
                                f"Error in LLM Response: The LLM did not provide an updated file for {file_name}"
                            )

                        result.updated_file = content.updated_file
                        result.used_prompts.append(prompt)
                        result.total_reasoning.append(content.reasoning)
                        result.additional_information.append(content.additional_info)
                        if include_llm_results:
                            result.llm_results.append(llm_result.content)

                        break
                except Exception as e:
                    KAI_LOG.warn(
                        f"Request to model failed for batch {count}/{len(batched_incidents)} for {file_name} with exception, retrying in {self.model_provider.llm_retry_delay}s\n{e}"
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
