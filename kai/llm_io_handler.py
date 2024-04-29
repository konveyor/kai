import itertools
from typing import Any, Callable, Literal, Optional

from kai_logging import KAI_LOG

from kai.incident_store import IncidentStore
from kai.model_provider import ModelProvider
from kai.pydantic_models import guess_language, parse_file_solution_content


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
    # ruleset_name: str
    # violation_name: str
    # incident_snip: str optional
    # incident_variables: object
    # line_number: int (0-indexed)
    # analysis_message: str
    batch_mode: Optional[
        Literal["none", "single_group", "ruleset", "violation"]
    ] = "single_group",
    include_solved_incidents: Optional[bool] = True,
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
                solved_incident, match_type = request.app[
                    "incident_store"
                ].get_fuzzy_similar_incident(
                    incident["violation_name"],
                    incident["ruleset_name"],
                    incident.get("incident_snip", ""),
                    incident["incident_variables"],
                )

                KAI_LOG.debug(solved_incident)

                if not isinstance(solved_incident, dict):
                    raise Exception("solved_example not a dict")

                if bool(solved_incident) and match_type == "exact":
                    solved_example = request.app[
                        "incident_store"
                    ].select_accepted_solution(solved_incident["solution_id"])
                    incident["solved_example_diff"] = solved_example[
                        "solution_small_diff"
                    ]
                    incident["solved_example_file_name"] = solved_incident[
                        "incident_uri"
                    ]

        args = {
            "src_file_name": request_json["file_name"],
            "src_file_language": src_file_language,
            "src_file_contents": updated_file,
            "incidents": incidents,
        }

        prompt = build_prompt(
            request.app["model_provider"].get_prompt_builder_config("multi_file"), args
        )

        KAI_LOG.debug(f"Sending prompt: {prompt}")

        KAI_LOG.info(
            f"Processing incident batch {count}/{len(batched)} for {request_json['file_name']}"
        )
        llm_result = None
        for _ in range(LLM_RETRIES):
            try:
                with playback_if_demo_mode(
                    model_id,
                    request_json["application_name"],
                    f'{request_json["file_name"].replace("/", "-")}',
                ):
                    llm_result = request.app["model_provider"].invoke(prompt)
                    content = parse_file_solution_content(
                        src_file_language, llm_result.content
                    )
                    if request_json.get("include_llm_results"):
                        llm_results.append(llm_result.content)

                    total_reasoning.append(content.reasoning)
                    used_prompts.append(prompt)
                    additional_info.append(content.additional_info)
                    if not content.updated_file:
                        raise Exception(
                            f"Error in LLM Response: The LLM did not provide an updated file for {request_json['file_name']}"
                        )
                    updated_file = content.updated_file
                    break
            except Exception as e:
                KAI_LOG.warn(
                    f"Request to model failed for batch {count}/{len(batched)} for {request_json['file_name']} with exception, retrying in {LLM_RETRY_DELAY}s\n{e}"
                )
                KAI_LOG.debug(traceback.format_exc())
                time.sleep(LLM_RETRY_DELAY)
        else:
            KAI_LOG.error(f"{request_json['file_name']} failed to migrate")
            raise web.HTTPInternalServerError(
                reason="Migration failed",
                text=f"The LLM did not generate a valid response: {llm_result}",
            )

    return something
