import logging

# trunk-ignore-begin(bandit/B404)
import subprocess

# trunk-ignore-end(bandit/B404)
import sys

from kai.rpc_server.rpc import RpcEndpoint, RpcServer, logger

sys.path.append("./client")

# Call this with:
# python kai/rpc_client/ide_client.py ../kai/server/config.toml coolstore ../example/analysis/coolstore/output.yaml ../example/coolstore/


def main():
    file_handler = logging.FileHandler("client.log")
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    if len(sys.argv) < 5:
        print(
            "All arguments are required\nUsage: node rpc-client.js <kai_toml_config> <app_name> <report_path> <input_file_path>"
        )
        sys.exit(1)

    # "python", "client/rpc.py"
    # "./dist/cli"
    # trunk-ignore-begin(bandit/B603)
    # binary_path = "./dist/cli"
    rpc_server = subprocess.Popen(
        # [binary_path],
        ["python", "kai/rpc_server/rpc_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=False,  # Change text mode to binary mode
    )
    # trunk-ignore-end(bandit/B603)

    rpc = RpcServer(
        json_rpc_endpoint=RpcEndpoint(
            io_send=rpc_server.stdin,
            io_recv=rpc_server.stdout,
        ),
        timeout=60,
    )
    rpc.start()
    request_params = {
        "config_path": sys.argv[1],
        "app_name": sys.argv[2],
        "report_path": sys.argv[3],
        "input_file_path": sys.argv[4],
        "incidents": [],
    }
    try:
        print(f"running get_incident_solutions_for_file() with params {request_params}")
        response = rpc.call_method(
            "get_incident_solutions_for_file",
            kwargs=request_params,
        )
        print(response)
        print("\nReceived response successfully!")
    finally:
        rpc_server.stdin.close()
        rpc_server.stdout.close()
        rpc_server.terminate()
        rpc_server.wait()
        rpc.stop()


if __name__ == "__main__":
    main()
