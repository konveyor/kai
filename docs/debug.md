# Debug Kai And File Issues

Logs are divided into two separate files under your working directory at /.vscode/konveyor-logs:

- kai-analyzer-server.log: This file is useful for debugging issues related to running analysis. It provides details about the Java and Maven installation, the initialization of the Java connection, and the startup process of the analyzer server.

- kai-rpc-server.log: This log is intended for debugging the RPC server and any communication with the AI system. It captures interactions involved in fixing incidents and retrieving results.

## File an Issue

Please Fill out all the information requested below when opening an issue [here](https://github.com/konveyor/kai/issues).

### Detailed Guidelines

```md
Help us resolve your issue faster by providing detailed information. Please follow the structure below to ensure we have all the necessary details:

1.Issue Description\*\*

- Summary: Briefly describe the problem.
- Logs: Attach any relevant log files (e.g., `kai-analyzer-server.log` or `kai-rpc-server.log`) to help us identify the issue.

2. Steps to Reproduce\*\*

- Provide a step-by-step guide on how to reproduce the issue if possible.

3. Environment Details
   Please include the following information to help us better understand your setup:

- Operating System (OS): (e.g., Windows 11, macOS Ventura, Ubuntu 22.04)
- Java Version: (e.g., OpenJDK 17.0.2)
- Maven Version: (e.g., Apache Maven 3.8.4)
- VS Code Version: (e.g., 1.82.0)
- Kai Version: (e.g., v0.0.6)

4.  Additional Details

- Error Messages: Include any error messages or stack traces you encountered.
- Screenshots: Attach screenshots to illustrate the issue, if applicable.
- Expected Behavior: Describe what you expected to happen.
- Actual Behavior: Describe what actually happened.
```

### Troubleshooting

- **No Incidents Found**: Check the `.vscode/settings.json` file in your working directory to ensure the targets are correctly recorded.

- **Failed to Run Initial Analysis**: Verify that the correct Java and Maven versions are set in the current environment. Detailed logs can be found in `kai-analyzer-server.log`.
