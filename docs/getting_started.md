# Getting Started

- [Getting Started](#getting-started)
  - [Overview](#overview)
  - [Installation](#installation)

## Overview

Running Kai consists of:

1. Installing the Kai dependencies
1. Launching the backend Kai RPC Server
   - This is the component that will construct prompts,
     talk to Large Language Models (LLMs), and generate code fixes
1. A client that performs analysis and issues RPC calls to generate fixes. This is the [IDE Extension](https://github.com/konveyor/editor-extension).
   - It's also possible to issue API requests directly, and we have a python
     script that does this to aid demonstrations. See
     [example/README.md](/example/README.md)

## Installation
Download Kai server and analyzer binaries for your machine and place them in
our example directory. First, download the zip file for your OS
[here](https://github.com/konveyor/kai/releases/tag/v0.0.1). Unzip the
directory and copy the binaries to `example/analysis`.
```
$ cp ~/Downloads/kai-rpc-server.linux-x86_64/kai-rpc-server /usr/local/bin
$ cp ~/Downloads/kai-rpc-server.linux-x86_64/kai-analyzer-rpc /usr/local/bin
```
