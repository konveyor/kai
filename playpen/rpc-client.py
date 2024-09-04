import logging

# trunk-ignore-begin(bandit/B404)
import subprocess

# trunk-ignore-end(bandit/B404)
import sys

sys.path.append("./client")
from client import rpc as kaiRpcClient


def main():
    file_handler = logging.FileHandler("client.log")
    kaiRpcClient.log.addHandler(file_handler)
    kaiRpcClient.log.setLevel(logging.DEBUG)
    if len(sys.argv) < 5:
        print(
            "All arguments are required\nUsage: node rpc-client.js <kai_toml_config> <app_name> <report_path> <input_file_path>"
        )
        sys.exit(1)

    # "python", "client/rpc.py"
    # "./dist/cli"
    # trunk-ignore-begin(bandit/B603)
    binary_path = "./dist/cli"
    rpc_server = subprocess.Popen(
        [binary_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    # trunk-ignore-end(bandit/B603)

    rpc = kaiRpcClient.CustomRpcServer(
        json_rpc_endpoint=kaiRpcClient.CustomRpcEndpoint(
            rpc_server.stdin, rpc_server.stdout
        ),
        timeout=60,
    )
    rpc.start()
    request_params = {
        "config_path": sys.argv[1],
        "app_name": sys.argv[2],
        "report_path": sys.argv[3],
        "input_file_path": sys.argv[4],
    }
    try:
        print(f"running get_incident_solutions_for_file() with params {request_params}")
        response = rpc.call_method(
            "get_incident_solutions_for_file",
            kwargs=request_params,
        )
        print(response)
        print("\nReceived response successfully!")
    except Exception as e:
        print(str(e))
        print("\nFailed to generate fix")
    finally:
        rpc_server.stdin.close()
        rpc_server.stdout.close()
        rpc_server.terminate()
        rpc_server.wait()
        rpc.stop()


if __name__ == "__main__":
    main()
