import datetime

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel

from kai.report import Report
from kai.routes.util import to_route
from kai.service.incident_store.incident_store import Application


# NOTE(@JonahSussman): This class can be removed if the other Application Class
# inherits from BaseModel.
class PostLoadAnalysisReportApplication(BaseModel):
    application_name: str
    repo_uri_origin: str
    repo_uri_local: str
    current_branch: str
    current_commit: str
    generated_at: datetime.datetime


class PostLoadAnalysisReportParams(BaseModel):
    path_to_report: str
    application: PostLoadAnalysisReportApplication


@to_route("post", "/load_analysis_report")
async def post_load_analysis_report(request: Request):
    params = PostLoadAnalysisReportParams.model_validate(await request.json())

    application = Application(**params.application.model_dump())
    report = Report.load_report_from_file(params.path_to_report)

    count = request.app["incident_store"].load_report(application, report)

    return web.json_response(
        {
            "number_new_incidents": count[0],
            "number_unsolved_incidents": count[1],
            "number_solved_incidents": count[2],
        }
    )
