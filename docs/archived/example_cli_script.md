# Example CLI Script

- We have a demo script at [example/README.md](/example/README.md) that will walk through the migration of a sample application written for EAP with Java EE and bring it to Quarkus.
- Sample Application
  - https://github.com/konveyor-ecosystem/coolstore
    - We will use the `main` branch which has the Java EE version.
    - We have found [these issues](https://github.com/jmle/kai-examples/blob/main/coolstore-examples/examples.md) in the `main` branch which need to be addressed before we move to Quarkus:
      - This information was obtained by running [Kantra](https://github.com/konveyor/kantra) (Konveyor's static code analyzer) with these [custom-rules](https://github.com/konveyor-ecosystem/kai/tree/main/kai_solution_server/samples/custom_rules)
        - Full output from [Kantra](https://github.com/konveyor/kantra) is checked into the git repo here: [example/analysis/coolstore](example/analysis/coolstore)
  - Limitations:
    - Kai will perform a partial migration to Quarkus, but manual changes will be required.
    - We lack sufficient analysis rules for a full migration, but this workflow can begin to show a preview of Kai in action to see directionally where the project is headed.

## Details of Example CLI Script

- [example/run_demo.py](example/run_demo.py) is a python script that will issue a partial migration of a sample Java EE application [coolstore](https://github.com/konveyor-ecosystem/coolstore) to Quarkus.
- What is `run_demo.py` doing?

  - `run_demo.py` will look at Kantra analysis of the [coolstore](https://github.com/konveyor-ecosystem/coolstore) application and will issue a series of requests to Kai to generate a fix and then write those fixes back to the application's git checkout.

- How to execute `run_demo.py`?
  - See [example/README.md](example/README.md) to learn more of how to run this
