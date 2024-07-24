# Demo Mode - Cached LLM Results

The kai server is able to cache results from a LLM and later replay these to aid test or demonstration scenarios.

This mode uses a project called [vcr](https://vcrpy.readthedocs.io/en/latest/) to record the interaction with a given LLM.

## What to expect from `DEMO_MODE`

_if_ the `kai/data/vcr/<application_name>/<model>` directory contains a request which has been cached AND if `DEMO_MODE` is enabled then a request that has the same exact parameters as what was seen during recording will return the cached data and will instead of talking to the LLM.

This mode is most useful for situations where you want to demo functionality but are concerned about conference wifi. The data replayed is actual data that specific LLM generated in past, it's just cached for convenience.

## Notes on `DEMO_MODE` and cached responses

The kai server will always cache responses in the `kai/data/vcr/<application_name>/<model>` directory. In non-demo mode, these responses will be overwritten whenever a new request is made.
When the server is run with `DEMO_MODE=true`, these responses will be played back. The request will be matched on everything except for authorization headers, cookies, content-length and request body.

### `DEMO_MODE` Cached Responses

- We do not actively maintain cached responses for all models/requests.
- You may look at: [kai/data/vcr/coolstore](kai/data/vcr/coolstore/) to see a list of what models have cached responses.
  - In general when we cache responses we are running: [example/run_demo.py](example/run_demo.py) and saving those responses.
    - This corresponds to a 'KAI Fix All' being run per file in Analysis.
- When running from IDE and attempting to use cached response, we likely only have cached responses for 'Fix All', and we do not have cached responses for individual issues in a file.

### `DEMO_MODE` Updating Cached Responses

There are two ways to record new responses:

1. Run the requests while the server is not in `DEMO_MODE`
1. Delete the specific existing cached response (under `kai/data/vcr/<application_name>/<model>/<source-file-path-with-slashes-replaced-with-dashes.java.yaml>`), then rerun. When a cached response does not exist, a new one will be recorded and played back on subsequent runs.
