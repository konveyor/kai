const cp = require("child_process");
const rpc = require("vscode-jsonrpc/node");
const fs = require("fs");

if (process.argv.length < 6) {
  console.error(
    "All arguments are required\nUsage: node rpc-client.js <kai_toml_config> <app_name> <report_path> <input_file_path>",
  );
  process.exit(1);
}

const kaiConfigToml = process.argv[2];
const appName = process.argv[3];
const reportPath = process.argv[4];
const inputFilePath = process.argv[5];

const binaryPath = "./dist/cli";
if (!fs.existsSync(binaryPath)) {
  console.error(
    `Kai client binary not found at path ${binaryPath}, build a binary by running 'pyinstaller build.spec'`,
  );
  process.exit(1);
}

const params = {
  app_name: appName,
  report_path: reportPath,
  input_file_path: inputFilePath,
  config_path: kaiConfigToml,
};

let rpcServer = cp.spawn(binaryPath, [], {
  stdio: ["pipe", "pipe", process.stderr],
});

setTimeout(() => {
  let connection = rpc.createMessageConnection(
    new rpc.StreamMessageReader(rpcServer.stdout),
    new rpc.StreamMessageWriter(rpcServer.stdin),
  );

  console.log("created rpc process");
  connection.listen();
  connection
    .sendRequest("get_incident_solutions_for_file", { kwargs: params })
    .then((result) => {
      console.log(result);
      console.log("\nReceived response successfully!");
    })
    .catch((error) => {
      console.error(error);
      console.error("error generating fix");
    })
    .finally(() => {
      connection.dispose();
      rpcServer.kill();
    });
}, 4000);
