# Usage

- Kai is intended to be used via an IDE Plugin
- A REST API is also available, this is what the IDE Plugin uses to generate fixes from the kai backend.

_In the future, in addition to an IDE Plugin we may explore a tighter integration to [Konveyor Hub](https://github.com/konveyor/tackle2-hub) to generate fixes to certain categories of analysis issues automatically._

## Usage Overview

The primary way to use Kai is via an IDE Plugin that communicates to the backend RST API.

- IDE setup: See: [Install the Kai VSCode Plugin](https://github.com/konveyor-ecosystem/kai-vscode-plugin/blob/main/docs/user-guide.md)

### Alternate usage for evaluation purposes

- We have a python script that will attempt a partial migration of a sample Java EE application [coolstore](https://github.com/konveyor-ecosystem/coolstore) to Quarkus.

  - This is migration is NOT complete.
    - We lack sufficient analysis rules for a full migration, but this workflow can begin to show a preview of Kai in action to see directionally where the project is headed.

  [example/run_demo.py](example/run_demo.py), that will run through a migration of

      * We have an example script that shows what usage to API looks like

  1. We have a script: [example/run_demo.py](example/run_demo.py) that will look at Kantra analysis of the [coolstore](https://github.com/konveyor-ecosystem/coolstore) application and will issue a series of requests to Kai to generate a Fix and then store those fixes back to the application.
  1. See [example/README.md](example/README.md) to learn more how to run this

# Usage Overview

- We have a demo that will walk through the migration of a sample application written for EAP with Java EE and bring it to Quarkus.
- Sample Application
  - https://github.com/konveyor-ecosystem/coolstore
    - We will use the `main` branch which has the Java EE version.
    - We have found [these issues](https://github.com/jmle/kai-examples/blob/main/coolstore-examples/examples.md) in the `main` branch which need to be addressed before we move to Quarkus:
      - This information was obtained by running [Kantra](https://github.com/konveyor/kantra) (Konveyor's static code analyzer) with these [custom-rules](https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules)
        - Full output from [Kantra](https://github.com/konveyor/kantra) is checked into the git repo here: [example/analysis/coolstore](example/analysis/coolstore)

### What are the general steps of the demo?

1. We launch VSCode with our Kai VS Code extension from [konveyor-ecosystem/kai-vscode-plugin](https://github.com/konveyor-ecosystem/kai-vscode-plugin/tree/main)
2. We open a git checkout of a sample application: [coolstore](https://github.com/konveyor-ecosystem/coolstore)
3. We run [Kantra](https://github.com/konveyor/kantra) inside of VSCode to do an analysis of the application to learn what issues are present that need to be addressed before migrating to Quarkus
4. We view the analysis information in VSCode
5. We look at the impacted files and choose what files/issues we want to fix
6. We click 'Generate Fix' in VSCode on a given file/issue and wait ~45 seconds for the Kai backend to generate a fix
7. We view the suggested fix as a 'Diff' in VSCode
8. We accept the generated fix
9. The file in question has now been updated
10. We move onto the next file/issue and repeat
