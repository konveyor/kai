# Requires

- Kai backend to be running locally
  - You can see [docs/Getting_Started.md](docs/Getting_Started.md) for guidance

## To run this demo client

1. `fetch.sh` - Ensures that needed source code for the demo app is fetched
1. `source ../env/bin/activate`
   - Assumes that we are running in the python virtual environment from kai
   - If you haven't created a virtual environment yet, refer to [docs/contrib/Dev_Environment.md](docs/contrib/Dev_Environment.md)
1. `./run_demo.py`
   - After the script has run you will see it has updated the associated .java files under the 'coolstore' source code directory, there are also files written to show the prompt used and the raw result from the LLM.
