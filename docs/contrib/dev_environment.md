# Kai Binary Development Environment

This document describes how to setup a local development environment for Kai's
backend.

- [Kai Binary Development Environment](#kai-binary-development-environment)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Building and using the Binaries](#building-and-using-the-binaries)
  - [Debugging from VSCode](#debugging-from-vscode)

## Overview

Running Kai's backend involves running a few processes:

- Postgres instance which we deliver via container
- Backend REST API server
- [Optional] Hub Importer process to sync data from Konveyor

## Prerequisites

1. [Python 3.12](https://www.python.org/downloads/)
2. Access to a Large Language Model.

> [!NOTE]
>
> If you want to run Kai against an LLM you will likely need to configure a LLM
> API key to access your service (unless running against a local model).
>
> We do provide a means of running Kai against previously cached data from a few
> models to aid demo flows. This allows you to run through the steps of using
> Kai without requiring access to a LLM. We call this **demo mode**.
>
> If you do not provide LLM API access then demo mode will **only** be able to
> replay previous cached responses.

## Building and using the Binaries

First, clone the repo and ensure you have the virtual environment setup

```sh
git clone https://github.com/konveyor-ecosystem/kai.git
cd kai
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Next, build the binary with:

```sh
make build-binaries
```

You should have 2 new files: `dist/kai-rpc-server` and `dist/kai-analyzer-rpc`.

For ease of development, set `"konveyor.kaiRpcServerPath"` and
`"konveyor.analyzerPath"` to their respective paths, pointing to the newly built
binaries.

Now whenever you make a change, you can rebuild the project and
restart from within the ide extension.

<!--

NOTE(@JonahSussman): We should add this back once the solution server exists.

Next, open a new terminal run the postgres container via podman:

```sh
make run-postgres
```

Finally, return to your previous terminal run the Kai server:

```sh
make run-server
```

> [!NOTE]
>
> If you want to run with cached LLM responses run with:
> `KAI__DEMO_MODE=true make run-server`. The `KAI__DEMO_MODE` option will cache
> responses and play them back on subsequent runs.
>
> If you want to run with debug information, set the environment variable with:
> `KAI__LOG_LEVEL=debug make run-server`.

On your first run, there will be no solved examples in the database. You can
load some sample data to get started. Open a new terminal and run:

```sh
source env/bin/activate
pushd samples
./fetch_apps.py
popd
make load-data
```

This should complete in ~1-2 minutes.

-->

## Debugging from VSCode

You may want to use VSCode's built in debugger at some point (i.e. to set
breakpoints, watch expressions, etc...). This requires some set up to get
working.

Add the following to your `launch.json`'s `"configurations"` list. (For more
information, click [here](https://go.microsoft.com/fwlink/?linkid=830387).)

```json
{
  "name": "Python Debugger: Attach using Process Id",
  "type": "debugpy",
  "request": "attach",
  "processId": "${command:pickProcess}",
  "justMyCode": false,
},
```

Now, if you got the process id of the Kai binary and used the debugger as-is,
you would get some very strange behavior. This is because we compile our Python
code to a binary using [Pyinstaller](https://pyinstaller.org/en/stable/), which
the debugger doesn't know how to handle. Additionally, the IDE simply calls the
binary outright, with no arguments. In other words, we can't tell the IDE to
execute `python main.py`, we can only tell it to execute `./main.py`.

Thus, we need to have the IDE spawn a Python process (not a compiled binary) by
calling the `main.py` file itself (so the IDE spawn it) to allow the debugger to
work properly.

First, make sure `kai/rpc_server/main.py` is executable with:

```sh
chmod +x kai/rpc_server/main.py
```

Next, make sure you are inside your virtual environment and find the location of
your Python interpreter:

```sh
which python
```

The `python` binary should be inside your virtual environment folder.

```
/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/venv/bin/python
```

Next, add the following to the top of `kai/rpc_server/main.py`:

```python
#!<result of `which python`>
```

Now executing `./kai/rpc_server/main.py` will call the script directly using the
python interpreter found in your virtual environment.

Next, modify `"konveyor.kaiRpcServerPath"` inside the IDE's `settings.json` to
be the location of `main.py`. For example:

```json
"konveyor.kaiRpcServerPath": "/home/jonah/Projects/github.com/konveyor-ecosystem/kai-jonah/kai/rpc_server/main.py",
```

Next, start the server inside the IDE extension. Open up the `Output` tab, click
on `Konveyor-Analyzer` and scroll until you see the log `kai rpc server has been
spawned!`. Copy the pid inside the square brackets.

![](images/kai-rpc-server-has-been-spawned.png)
