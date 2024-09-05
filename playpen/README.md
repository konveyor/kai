# Playpen

Playpen is intended to be a location for exploring and sharing concepts. The material created under this directory may be broken and contain approaches that end up not being useful, or the material here may help to rapidly try out a concept that ends up being incorporated into Kai.

## PyInstaller and JSON-RPC Client

The goals of this effort are:

- Figure out how we can enable communication between the Kai Client and different IDE extensions (possibly running in restricted environments) in a uniform way.
- Figure out a way to package the client into an independent binary that can be run on different platforms.

As of writing this, here's the progress we made on the goals above:

- We have a JSON-RPC interface in front of the Client CLI. The JSON-RPC interface can be found in [./client/rpc.py](./client/rpc.py). It exposes `get_incident_solutions_for_file` function that generates a fix for one file. There are two example clients (Python and Javascript) we have written that talk with the interface over I/O streams.

- We have a `build.spec` file that builds the JSON-RPC client into a binary using PyInstaller.

### Building JSON-RPC interface into a binary

Before you can build the binary, you need to activate Kai virtual environment. Once venv is activated, you need to install Kai module in the env. To install Kai module, navigate to the Kai project root and run:

```sh
pip install -e .
```

Now we install pyinstaller in current venv:

```sh
pip install pyinstaller
```

Next, we run pyinstaller to generate a binary:

```sh
pyinstaller build.spec
```

Once successful, a binary will be generated at `./dist/cli`.

#### Building for different platforms

We are using PyInstaller to create binaries. To create a binary for a certain platform / arch, we are building on the same platform + arch. As per our understanding, it is possible to potentially cross-compile for different architectures but not the platform itself.

So far, we have successfully built and tested binaries for MacOS and Windows (built on respective machines).

### Testing JSON-RPC binary

Now that we have built our JSON-RPC interface into a binary, we will test it using a Python and a JS client that communicates. Both of these clients use a hardcoded path `./dist/cli` to run the JSON-RPC server. Make sure you have built the binary before moving forward.

#### Testing with Python client

To run the Python JSON-RPC client, install a dependency:

```sh
pip install pylspclient
```

To run the client:

```sh
python rpc-client.py <KAI_TOML_CONFIG> <APP_NAME> <ANALYSIS_OUTPUT_PATH> <INPUT_FILE_PATH>
```

See [arguments](#client-arguments) for help on arguments above.

#### Testing with JS client

To run the Javascript client, install a dependency:

```sh
npm install vscode-jsonrpc
```

To run the client:

```sh
node rpc-client.js <KAI_TOML_CONFIG> <APP_NAME> <ANALYSIS_OUTPUT_PATH> <INPUT_FILE_PATH>
```

##### Client arguments

Both the Python and JS clients take exactly the same arguments in order:

- <KAI_TOML_CONFIG>: Absolute path to the Kai config you want to use to generate fix
- <APP_NAME>: The name of the application you're analyzing
- <ANALYSIS_OUTPUT_PATH>: Absolute path to an analysis report containing incidents
- <INPUT_FILE_PATH>: Absolute path to the input file for which you want to generate incidents

When successful, both clients will print the updated file followed by the following message:

```sh
Received response successfully!
```
