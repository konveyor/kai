# Development Environment

This document describes how to set up a local development environment for Kai's
backend components.

- [Development Environment](#development-environment)
  - [Overview](#overview)
  - [MCP Solution Server](#mcp-solution-server)
  - [Go Analyzer RPC](#go-analyzer-rpc)
  - [Debugging from VSCode](#debugging-from-vscode)

## Overview

This repository contains two active backend components:

- **`kai_mcp_solution_server/`** - Python MCP solution server (self-contained
  project with its own `pyproject.toml`)
- **`kai_analyzer_rpc/`** - Go-based analyzer RPC plugin

## MCP Solution Server

The MCP solution server is a self-contained Python project. See
[kai_mcp_solution_server/README.md](../../kai_mcp_solution_server/README.md) for
setup and development instructions.

## Go Analyzer RPC

Build the Go analyzer binary:

```sh
cd kai_analyzer_rpc
go build -o kai-analyzer main.go
```

Or use the Makefile:

```sh
make build-kai-analyzer
```

## Debugging from VSCode

You may want to use VSCode's built-in debugger at some point (i.e. to set
breakpoints, watch expressions, etc...). This requires some setup to get
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

For ease of development, you can set the IDE's binaries to reference the
location of the newly built binaries. In the VSCode extension, open your
[`settings.json
file`](https://code.visualstudio.com/docs/editor/settings#_settings-json-file)
and set `"konveyor.analyzerPath"` to the path of your locally built
`kai-analyzer` binary.
