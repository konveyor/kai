import time
import traceback
from typing import Iterator, Optional
from unittest.mock import MagicMock

from aiohttp import web
from langchain_core.messages import BaseMessage, BaseMessageChunk
from pydantic import BaseModel

from kai.kai_logging import KAI_LOG
from kai.models.file_solution import guess_language, parse_file_solution_content
from kai.models.kai_config import KaiConfig, SolutionProducerKind
from kai.models.report_types import ExtendedIncident
from kai.service.incident_store.incident_store import IncidentStore
from kai.service.kai_application.util import (
    BatchMode,
    batch_incidents,
    get_prompt,
    playback_if_demo_mode,
)
from kai.service.llm_interfacing.model_provider import ModelProvider
from kai.service.solution_handling.consumption import (
    SolutionConsumerAlgorithm,
    solution_consumer_factory,
)
from kai.service.solution_handling.detection import solution_detection_factory
from kai.service.solution_handling.production import (
    SolutionProducer,
    SolutionProducerLLMLazy,
    SolutionProducerTextOnly,
)

# FIXME: Add back in tracing
trace = MagicMock()


# TODO: Possibly merge with FileSolutionContent?
class UpdatedFileContent(BaseModel):
    updated_file: str
    total_reasoning: list[str]
    used_prompts: list[str]
    model_id: str
    additional_information: list[str]

    llm_results: Optional[list[str | list[str | dict]]]


class KaiApplication:
    config: KaiConfig
    model_provider: ModelProvider
    incident_store: IncidentStore
    solution_consumer: SolutionConsumerAlgorithm

    def __init__(self, config: KaiConfig):
        self.config = config

        KAI_LOG.setLevel(config.log_level.upper())
        print(
            f"Logging for KAI has been initialized and the level set to {config.log_level.upper()}"
        )

        KAI_LOG.info(
            f"Tracing of actions is {'enabled' if config.trace_enabled else 'disabled'}"
        )

        if config.demo_mode:
            KAI_LOG.info("DEMO_MODE is enabled. LLM responses will be cached")

        self.model_provider = ModelProvider(config.models)

        KAI_LOG.info(f"Selected provider: {config.models.provider}")
        KAI_LOG.info(f"Selected model: {self.model_provider.model_id}")

        solution_detector = solution_detection_factory(
            config.incident_store.solution_detectors
        )
        solution_producer: SolutionProducer

        match config.incident_store.solution_producers:
            case SolutionProducerKind.TEXT_ONLY:
                solution_producer = SolutionProducerTextOnly()
            case SolutionProducerKind.LLM_LAZY:
                solution_producer = SolutionProducerLLMLazy(self.model_provider)

        self.incident_store = IncidentStore(
            config.incident_store,
            solution_detector,
            solution_producer,
        )

        KAI_LOG.info(f"Selected incident store: {config.incident_store.args.provider}")

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
    ):
        src_file_language = guess_language(file_contents, filename=file_name)
        KAI_LOG.debug(f"{file_name} classified as language {src_file_language}")

        result = UpdatedFileContent(
            updated_file=file_contents,
            total_reasoning=[],
            used_prompts=[],
            model_id=self.model_provider.model_id,
            additional_information=[],
            llm_results=[],
        )

        batched_incidents = batch_incidents(incidents, batch_mode)

        for count, (_group_by, incidents) in enumerate(batched_incidents, 1):
            KAI_LOG.info(
                f"Processing incident batch {count}/{len(batched_incidents)} for {file_name}"
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
                        pb_incident["solution_str"] = self.solution_consumer(
                            solutions[0]
                        )

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

    # NOTE(@JonahSussman): This function should probably become deprecated at some
    # point. `get_incident_solutions_for_file` does everything this function does,
    # aside from streaming.
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
