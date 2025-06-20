# Kai MCP Solution Server

A Model Context Protocol (MCP) server for managing Kai solutions database. This server allows AI agents to store, retrieve, and analyze solutions for code migration tasks.

## Overview

<img src="https://img.shields.io/badge/MCP-Compatible-blue" alt="MCP Compatible">

This MCP server provides tools and resources for managing code migration solutions used by the [Konveyor/Kai](https://github.com/konveyor/kai) project, which assists with modernizing application source code to new platforms via Generative AI.

The server implements the following functionality:

- Store and manage solutions for code migration tasks
- Query success rates for specific migration tasks
- Find related solutions for LLM retrieval augmented generation (RAG)
- Format solution examples for LLM consumption

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/)
- Podman (for containerized deployment)
- Kubernetes/OpenShift (for cluster deployment)

## Getting Started

### Local Development

1. Install dependencies:

   ```bash
   uv sync
   ```

1. Set the `KAI_LLM_PARAMS` environment variable. The environment variable will be turned into a Python dictionary and passed along to Langchain's [`init_chat_model`](https://python.langchain.com/docs/how_to/chat_models_universal_init/). Look there for more detailed information. Here are some standard configurations:

   ```bash
   # GPT 4o
   KAI_LLM_PARAMS='{"model": "gpt-4o", "model_provider": "openai"}'
   # Claude 3
   KAI_LLM_PARAMS='{"model": "claude-3-opus-20240229", "model_provider": "anthropic"}'
   # Gemini 1.5
   KAI_LLM_PARAMS='{"model": "gemini-1.5-pro", "model_provider": "google_vertexai"}'
   # Custom fake model, returns fake responses
   KAI_LLM_PARAMS='{"model": "fake"}'
   ```

1. Set the `KAI_DB_DSN` environment variable. Here are two common ones:

   ```bash
   # Postgres
   KAI_DB_DSN='postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres'
   # SQLite (Yes, quadruple slashes are required)
   KAI_DB_DSN='sqlite+aiosqlite:////path/to/a/file.db'
   ```

1. Run the server locally:

   ```bash
   # Using HTTP transport (HTTP server)
   uv run python -m kai_mcp_solution_server --transport streamable-http --host 0.0.0.0 --port 8000

   # Using stdio transport (for direct process communication)
   uv run python -m kai_mcp_solution_server --transport stdio

   # With debug logging
   uv run python -m kai_mcp_solution_server --log-level debug
   ```

1. Test with the provided test client:

   ```bash
   # Test using stdio transport
   python tests/mcp_client.py --transport stdio

   # Test against a running HTTP server
   python tests/mcp_client.py --transport http --host localhost --port 8000

   # Show detailed output for resources
   python tests/mcp_client.py --full-output
   ```

1. For convenience, you can also use the Makefile:

   ```bash
   # Run server locally
   make run-local

   # Test with stdio transport
   make test-stdio

   # Test with HTTP transport
   make test-http
   ```

### Containerized Deployment

1. Build the container image:

   ```bash
   make build
   ```

2. Run the server in a container:

   ```bash
   make run-podman
   ```

3. Test against the containerized server:
   ```bash
   make test-http
   ```

### Kubernetes/OpenShift Deployment

The KAI MCP Solution Server can be deployed to Kubernetes or OpenShift using our Ansible-based deployment:

1. Deploy to Kubernetes or OpenShift:

   ```bash
   make deploy
   ```

2. Deploy with custom settings:

   ```bash
   # Custom namespace
   make deploy NAMESPACE=my-namespace

   # Custom image
   make deploy IMAGE=quay.io/custom/image:v1.0.0

   # Ansible variables using EXTRA_VARS
   make deploy EXTRA_VARS="storage_class=gp2 storage_size=5Gi"

   # OpenShift route settings
   make deploy EXTRA_VARS="route_tls_enabled=false"

   # Multiple Ansible variables
   make deploy EXTRA_VARS="route_tls_enabled=true route_tls_termination=edge route_tls_insecure_policy=Allow"

   # Combined customizations
   make deploy NAMESPACE=my-namespace IMAGE=quay.io/custom/image:v1.0.0 EXTRA_VARS="storage_class=gp2"
   ```

3. Check the deployment status:

   ```bash
   make status
   ```

4. Remove the deployment:
   ```bash
   make undeploy
   ```

See the [Ansible deployment documentation](deploy/ansible/README.md) for more details.

## MCP API Reference

---

### Tools

#### `create_incident`

Creates a new incident in the database.

- **Parameters**:
  - `client_id`: A string identifier for the client.
  - `extended_incident`: An `ExtendedIncident` object containing details about the incident.
- **Returns**: `int` (the ID of the created incident).

#### `create_solution`

Creates a proposed solution in the database and associates it with one or more incidents.

- **Parameters**:
  - `client_id`: A string identifier for the client.
  - `incident_ids`: A list of IDs of the incidents this solution addresses.
  - `change_set`: A `SolutionChangeSet` object detailing the proposed changes.
  - `reasoning`: An optional string explaining the reasoning behind the solution.
  - `used_hint_ids`: An optional list of IDs of hints used to generate this solution.
- **Returns**: `int` (the ID of the created solution).

#### `update_solution_status`

Updates the status of solutions associated with the given client ID in the database.

- **Parameters**:
  - `client_id`: A string identifier for the client.
  - `solution_status`: The new status for the solution (default: `SolutionStatus.ACCEPTED`).
- **Returns**: `None`.

#### `delete_solution`

Deletes a solution with the given ID from the database.

- **Parameters**:
  - `client_id`: A string identifier for the client.
  - `solution_id`: The ID of the solution to delete.
- **Returns**: `bool` (True if the solution was deleted, False otherwise).

#### `get_best_hint`

Retrieves the most recent accepted hint for a given ruleset and violation.

- **Parameters**:
  - `ruleset_name`: The name of the ruleset.
  - `violation_name`: The name of the violation.
- **Returns**: `GetBestHintResult` (an object with `hint` and `hint_id`) or `None` if no hint is found.

#### `get_success_rate`

Calculates the success rate (accepted solutions) for a list of violations.

- **Parameters**:
  - `violation_ids`: A list of `ViolationID` objects, each containing `ruleset_name` and `violation_name`.
- **Returns**: `list[SuccessRateMetric]` (a list of objects with `counted_solutions` and `accepted_solutions`) or `None` if no violations are provided.

## Development

### Project Structure

- **src/kai_mcp_solution_server/**: Main MCP server implementation
  - **server.py**: The main MCP server implementation
  - **dao.py**: Data access layer for the database
  - **analyzer_types.py**: Type definitions for code analysis
  - **util.py**: Utility functions
- **tests/**: Contains test clients and integration tests
  - **mcp_client.py**: Python test client for MCP server
  - **test_integration.py**: Pytest integration tests
  - **ssl_utils.py**: SSL bypass utilities for testing
- **ts-mcp-client/**: TypeScript test client for Node.js environments
  - **src/client.ts**: TypeScript MCP client implementation
  - **package.json**: Node.js dependencies and scripts
- **deploy/**: Contains the Containerfile and deployment resources
  - **ansible/**: Ansible playbooks and roles for Kubernetes/OpenShift deployment

### Running Tests

- Test with STDIO transport (spawns a new server):

  ```bash
  make test-stdio     # Python client
  make test-stdio-ts  # TypeScript client
  ```

- Test with HTTP transport (requires a running server):

  ```bash
  make run-local    # In one terminal
  make test-http    # Python client in another terminal
  make test-http-ts # TypeScript client in another terminal
  ```

- Run pytest integration tests:

  ```bash
  make pytest
  ```

- Test with a full containerized setup:
  ```bash
  make run-with-tests
  ```

## Authentication

The KAI MCP Solution Server supports bearer token authentication for HTTP transport connections.

### Bearer Token Authentication

Bearer tokens can be provided through the test client for HTTP connections:

```bash
# Using bearer token with test client
python tests/mcp_client.py --transport http --host api.example.com --bearer-token "your-jwt-token"

# Using Makefile with bearer token
make test-http BEARER_TOKEN="your-jwt-token"

# Combined with other options
python tests/mcp_client.py --transport http --host secure-server.com --port 443 --bearer-token "token" --insecure
```

### Authentication Headers

When a bearer token is provided, the client automatically adds the proper Authorization header to all HTTP requests:

```text
Authorization: Bearer your-jwt-token
```

## Test Client Usage

Two test clients are provided to help test and verify the functionality of the MCP solution server: a Python client and a TypeScript client. Both can connect to the server using either HTTP or stdio transport.

### Python Test Client

The Python test client (`tests/mcp_client.py`) provides comprehensive testing functionality:

```bash
# Basic usage with HTTP transport
python tests/mcp_client.py --transport http --host localhost --port 8000

# Using stdio transport (spawns a server process)
python tests/mcp_client.py --transport stdio

# Use a specific task key for testing
python tests/mcp_client.py --task-key migration-task-123

# Show full output for resources instead of truncated summaries
python tests/mcp_client.py --full-output

# Show verbose output for debugging
python tests/mcp_client.py --verbose

# Using bearer token for authentication
python tests/mcp_client.py --transport http --host localhost --port 8000 --bearer-token "your-token"

# Using Makefile shortcuts
make test-stdio      # Test with stdio transport
make test-http       # Test with HTTP transport
```

### TypeScript Test Client

The TypeScript test client (`ts-mcp-client/`) demonstrates MCP integration in Node.js environments:

```bash
# Build and run with stdio transport
cd ts-mcp-client
npm install
npm run build
node dist/client.js --transport stdio --server-path ../

# Using HTTP transport
node dist/client.js --transport http --host localhost --port 8000

# With authentication and SSL options
node dist/client.js --transport http --host localhost --port 8000 --bearer-token "your-token" --insecure

# Show verbose output for debugging
node dist/client.js --verbose

# Using Makefile shortcuts
make test-stdio-ts   # Test with stdio transport (TypeScript)
make test-http-ts    # Test with HTTP transport (TypeScript)
```

Both test clients will run through all available tools and resources, demonstrating how to interact with the MCP solution server.

## Integration with Claude and other LLMs

This MCP server can be integrated with Claude and other LLMs that support the Model Context Protocol. For detailed instructions on how to configure Claude Desktop with this MCP server, refer to the [Claude Desktop documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## License

This project is part of the Konveyor/Kai project and is licensed under the same license.
