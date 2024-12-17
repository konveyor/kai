# Configuration

- [Configuration](#configuration)
  - [Configuration Precedence](#configuration-precedence)
  - [Demo Mode and Cached LLM Results](#demo-mode-and-cached-llm-results)
    - [Notes on Cached Responses](#notes-on-cached-responses)
    - [Updating Cached Responses](#updating-cached-responses)
    - [Seeing a `401` while running with `KAI__DEMO_MODE=TRUE`?](#seeing-a-401-while-running-with-kai__demo_modetrue)

## Configuration Options

Kai is configured via the VSCode IDE extension. You can use the setup page or
configure the values directly in `settings.json`.

## Demo Mode and Cached LLM Results

TODO: UPDATE THIS SECTION WITH LATEST DEMO MODE

The kai server is able to cache results from a LLM and later replay these to aid
test or demonstration scenarios. This mode uses a project called
[vcr](https://vcrpy.readthedocs.io/en/latest/) to record the interaction with a
given LLM.

**IF** the `data/<application_name>/<model>` directory contains a
request which has been cached **AND** if `KAI__DEMO_MODE` is enabled **then** a
request that has the same exact parameters as what was seen during recording
will return the cached data and will instead of talking to the LLM.

This mode is most useful for situations where you want to demo functionality but
are concerned about conference wifi. The data replayed is actual data that
specific LLM generated in past, it's just cached for convenience.

> [!NOTE]
>
> The kai server will always cache responses in the
> `data/vcr/<application_name>/<model>` directory. In non-demo mode, these
> responses will be overwritten whenever a new request is made.
>
> When the server is run with `KAI__DEMO_MODE=true`, these responses will be
> played back. The request will be matched on everything except for
> authorization headers, cookies, content-length and request body.

### Demo Mode - Notes on Cached Responses

We do not actively maintain cached responses for all models/requests.

You may look at [kai/data/vcr/coolstore](kai/data/vcr/coolstore/) to see a list
of what models have cached responses. In general when we cache responses we are
running [example/run_demo.py](example/run_demo.py) and saving those responses.
This corresponds to a 'Kai Fix All' being run per file in Analysis.

When running from IDE and attempting to use cached response, we likely only have
cached responses for 'Fix All', and we do not have cached responses for
individual issues in a file.

### Demo Mode - Updating Cached Responses

There are two ways to record new responses:

1. Run the requests while the server is not in `KAI__DEMO_MODE`
1. Delete the specific existing cached response (under
   `kai/data/vcr/<application_name>/<model>/<source-file-path-with-slashes-replaced-with-dashes.java.yaml>`),
   then rerun. When a cached response does not exist, a new one will be recorded
   and played back on subsequent runs.

### Seeing a `401` while running in demo mode?

If you are running with `KAI__DEMO_MODE=TRUE` and you see a `401` being returned
from the LLM Provider consider that this is likely 'correct' behavior, if you do
not have a valid API key defined. Note that `KAI__DEMO_MODE` will attempt to
play back a cached response, yet if there is no cached data for the request Kai
will attempt to talk to the LLM and will make a 'real' request, which if you
don't have a valid API key will result in a `401`. To 'fix' this you will want
to look at the request you are sending to Kai and ensure it is cached for the
model you have configured, if you don't have valid cached data then you will
need to get a valid api key and re-run so the data may be cached.

```sh
WARNING - 2024-07-11 14:11:44,063 - [   llm_io_handler.py:243  - get_incident_solutions_for_file()] - Request to model failed for batch 1/1 for src/main/java/com/redhat/coolstore/model/InventoryEntity.java with exception, retrying in 10s
Failed to handle request to https://bam-api.res.ibm.com/v2/text/chat_stream?version=2024-01-10.
{
  "error": "Unauthorized",
  "extensions": {
    "code": "AUTH_ERROR",
    "state": null,
    "reason": "TOKEN_INVALID"
  },
  "message": "Invalid or missing JWT token",
  "status_code": 401
}
```
