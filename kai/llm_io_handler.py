import itertools
import os
import time
import traceback
from contextlib import contextmanager
from typing import Any, Callable, Literal, Optional

import vcr
from kai_logging import KAI_LOG

from kai.incident_store import IncidentStore
from kai.model_provider import ModelProvider
from kai.prompt_builder import build_prompt
from kai.pydantic_models import guess_language, parse_file_solution_content

LLM_RETRIES = 5
LLM_RETRY_DELAY = 10

DEMO_MODE = os.getenv("DEMO_MODE") == "true"


@contextmanager
def playback_if_demo_mode(model_id, application_name, filename):
    """A context manager to conditionally use a VCR cassette when demo mode is enabled."""
    record_mode = "once" if DEMO_MODE else "all"
    my_vcr = vcr.VCR(
        cassette_library_dir=f"{os.path.dirname(__file__)}/data/vcr/{application_name}/{model_id}/",
        record_mode=record_mode,
        match_on=[
            "uri",
            "method",
            "scheme",
            "host",
            "port",
            "path",
            "query",
            "headers",
        ],
        record_on_exception=False,
        filter_headers=["authorization", "cookie", "content-length"],
    )
    KAI_LOG.debug(
        f"record_mode='{record_mode}' - Using cassette {application_name}/{model_id}/{filename}.yaml",
    )

    # Workaround to actually blow away the cassettes instead of appending
    if my_vcr.record_mode == "all":
        my_vcr.persister.load_cassette = lambda cassette_path, serializer: ([], [])

    with my_vcr.use_cassette(f"{filename}.yaml"):
        yield


def get_key_and_res_function(
    batch_mode: str,
) -> tuple[Callable[[Any], tuple], Callable[[Any, Any], tuple[dict, list]]]:
    return {
        "none": (lambda x: (id(x),), lambda k, g: ({}, list(g))),
        "single_group": (lambda x: (0,), lambda k, g: ({}, list(g))),
        "ruleset": (
            lambda x: (x.get("ruleset_name"),),
            lambda k, g: ({"ruleset_name": k[0]}, list(g)),
        ),
        "violation": (
            lambda x: (x.get("ruleset_name"), x.get("violation_name")),
            lambda k, g: ({"ruleset_name": k[0], "violation_name": k[1]}, list(g)),
        ),
    }.get(batch_mode)


async def get_incident_solutions_for_file(
    model_provider: ModelProvider,
    incident_store: IncidentStore,
    file_contents: str,
    file_name: str,
    application_name: str,
    incidents: list[dict],  # TODO(@JonahSussman): Add a type for this
    # Dict keys are:
    # - ruleset_name: str
    # - violation_name: str
    # - incident_snip: str optional
    # - incident_variables: object
    # - line_number: int (0-indexed)
    # - analysis_message: str
    batch_mode: Optional[
        Literal["none", "single_group", "ruleset", "violation"]
    ] = "single_group",
    include_solved_incidents: Optional[
        bool
    ] = True,  # NOTE(@JonahSussman): Should this be renamed to "include_solutions"?
    include_llm_results: bool = False,
):
    src_file_language = guess_language(file_contents, filename=file_name)

    KAI_LOG.debug(f"{file_name} classified as filetype {src_file_language}")

    # NOTE: Looks worse than it is, `trunk check` mangled the heck out of this
    # section. It doesn't like lambdas for some reason :(
    updated_file = file_contents
    total_reasoning = []
    llm_results = []
    additional_info = []
    used_prompts = []
    model_id = model_provider.get_current_model_id()

    batch_key_fn, batch_res_fn = get_key_and_res_function(batch_mode)

    incidents.sort(key=batch_key_fn)
    batched_groupby = itertools.groupby(incidents, batch_key_fn)

    # NOTE: To get out of itertools hell
    batched: list[tuple[dict, list]] = []
    for batch_key, batch_group in batched_groupby:
        batch_dict, batch_list = batch_res_fn(batch_key, batch_group)
        batched.append((batch_dict, batch_list))

    for count, (_, incidents) in enumerate(batched, 1):
        for i, incident in enumerate(incidents, 1):
            incident["issue_number"] = i
            incident["src_file_language"] = src_file_language
            incident["analysis_line_number"] = incident["line_number"]

            if include_solved_incidents:
                solutions = incident_store.find_solutions(
                    incident["ruleset_name"],
                    incident["violation_name"],
                    incident["incident_variables"],
                    incident.get("incident_snip", ""),
                )

                if len(solutions) != 0:
                    incident["solved_example_diff"] = solutions[0][
                        "solution_small_diff"
                    ]
                    incident["solved_example_file_name"] = solutions[0]["incident_uri"]

        args = {
            "src_file_name": file_name,
            "src_file_language": src_file_language,
            "src_file_contents": updated_file,
            "incidents": incidents,
        }

        prompt = build_prompt(
            model_provider.get_prompt_builder_config("multi_file"), args
        )

        KAI_LOG.debug(f"Sending prompt: {prompt}")

        KAI_LOG.info(
            f"Processing incident batch {count}/{len(batched)} for {file_name}"
        )
        llm_result = None
        for _ in range(LLM_RETRIES):
            try:
                with playback_if_demo_mode(
                    model_id,
                    application_name,
                    f'{file_name.replace("/", "-")}',
                ):
                    llm_result = model_provider.invoke(prompt)
                    content = parse_file_solution_content(
                        src_file_language, llm_result.content
                    )
                    if include_llm_results:
                        llm_results.append(llm_result.content)

                    total_reasoning.append(content.reasoning)
                    used_prompts.append(prompt)
                    additional_info.append(content.additional_info)
                    if not content.updated_file:
                        raise Exception(
                            f"Error in LLM Response: The LLM did not provide an updated file for {file_name}"
                        )
                    updated_file = content.updated_file
                    break
            except Exception as e:
                KAI_LOG.warn(
                    f"Request to model failed for batch {count}/{len(batched)} for {file_name} with exception, retrying in {LLM_RETRY_DELAY}s\n{e}"
                )
                KAI_LOG.debug(traceback.format_exc())
                time.sleep(LLM_RETRY_DELAY)
        else:
            KAI_LOG.error(f"{file_name} failed to migrate")

            # TODO: These should be real exceptions
            raise web.HTTPInternalServerError(
                reason="Migration failed",
                text=f"The LLM did not generate a valid response: {llm_result}",
            )

    response = {
        "updated_file": updated_file,
        "total_reasoning": total_reasoning,
        "used_prompts": used_prompts,
        "model_id": model_id,
        "additional_information": additional_info,
    }
    if include_llm_results:
        response["llm_results"] = llm_results

    return response
