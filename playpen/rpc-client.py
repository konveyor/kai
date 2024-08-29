import json
import subprocess
import sys

import jsonrpyc


def main():
    print("running in client mode")

    if len(sys.argv) < 5:
        print(
            "All arguments are required\nUsage: node rpc-client.js <kai_toml_config> <app_name> <report_path> <input_file_path>"
        )
        sys.exit(1)

    # "python", "client/rpc.py"
    # "./dist/cli"
    rpc_server = subprocess.Popen(
        ["./dist/cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    rpc = jsonrpyc.RPC(stdin=rpc_server.stdout, stdout=rpc_server.stdin)
    request_params = {
        "config_path": sys.argv[1],
        "app_name": sys.argv[2],
        "report_path": sys.argv[3],
        "input_file_path": sys.argv[4],
    }
    print(f"sending params {json.dumps(request_params)}")
    try:
        response = rpc(
            "get_incident_solutions_for_file",
            args=(json.dumps(request_params),),
            block=0.1,
            timeout=30,
        )
        print(response)
    finally:
        rpc_server.stdin.close()
        rpc_server.stdout.close()
        rpc_server.terminate()
        rpc_server.wait()


if __name__ == "__main__":
    main()
