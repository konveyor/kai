import logging
import sys

from pydantic import BaseModel, FilePath

from kai.rpc_server.rpc import RpcEndpoint, RpcServer
from kai.shared.models.report_types import ExtendedIncident


class ParamsGetIncidentSolutionsForFile(BaseModel):
    app_name: str
    config_path: FilePath
    input_file_path: FilePath
    incidents: list[ExtendedIncident]
    report_path: FilePath
    log_level: str = "INFO"


def get_incident_solutions_for_file(self, **kwargs) -> str:
    return "Success!"


def main():
    file_handler = logging.FileHandler("server.log")
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger = logging.getLogger("kai_rpc")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    server = RpcServer(
        json_rpc_endpoint=RpcEndpoint(
            io_send=sys.stdout.buffer, io_recv=sys.stdin.buffer
        ),
        method_callbacks={
            "get_incident_solutions_for_file": get_incident_solutions_for_file,
        },
        timeout=60,
    )

    server.run()


if __name__ == "__main__":
    main()
