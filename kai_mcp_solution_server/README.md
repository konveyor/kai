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

- Python 3.9 or higher
- pip
- Podman (for containerized deployment)
- Kubernetes/OpenShift (for cluster deployment)

## Getting Started

### Local Development

1. Install dependencies:

   ```bash
   pip install mcp
   ```

2. Run the server locally:

   ```bash
   # Using SSE transport (HTTP server)
   python -m main --transport sse --host 0.0.0.0 --port 8000

   # Using stdio transport (for direct process communication)
   python -m main --transport stdio

   # Using a custom database path
   python -m main --db-path /path/to/custom/database.db

   # With debug logging
   python -m main --log-level debug
   ```

3. Test with the provided test client:

   ```bash
   # Test using stdio transport
   python tests/mcp_client.py --transport stdio

   # Test against a running HTTP server
   python tests/mcp_client.py --transport http --host localhost --port 8000

   # Show detailed output for resources
   python tests/mcp_client.py --full-output
   ```

4. For convenience, you can also use the Makefile:

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

### Tools

#### `create_solution`

Creates a proposed solution in the database.

- **Parameters**:
  - `extended_incident`: An `ExtendedIncident` object containing details about the incident.
  - `proposed_solution`: A `Solution` object containing details about the proposed solution.
- **Returns**: `CreateProposedSolutionResult` (object with `incident_id` and `solution_id`).

#### `update_solution_status`

Updates the status of a solution with the given ID in the database.

- **Parameters**:
  - `solution_id`: The ID of the solution to update.
  - `solution_status`: The new status for the solution (default: `SolutionStatus.ACCEPTED`).
- **Returns**: `DBSolution` (the updated solution object).

#### `delete_solution`

Deletes a solution with the given ID from the database.

- **Parameters**:
  - `solution_id`: The ID of the solution to delete.
- **Returns**: `bool` (True if the solution was deleted, False otherwise).

### Resources

#### `get_best_hint`

Retrieves the best hint for a given incident. It prioritizes hints associated with accepted solutions, otherwise, it returns the most recently created hint.

- **Parameters**:
  - `incident_id`: The ID of the incident.
- **Returns**: `str | None` (The text of the best hint, or None if no hints are available).

#### `get_success_rate`

Retrieves the success rate for a specific violation from the database.

- **Parameters**:
  - `ruleset_name` (str): The name of the ruleset containing the violation.
  - `violation_name` (str): The specific violation identifier to be evaluated.
  - `all_attempts` (bool, optional): If True, an incident is marked as successful if at least one solution is accepted. Defaults to False.
- **Returns**: `float` (A value between 0.0 and 1.0 indicating the success rate. Returns NaN if the specified violation does not exist. Returns -1.0 if there are no solutions for the violation.).

## Development

### Project Structure

- **main.py**: The main MCP server implementation
- **kai_solutions_dao.py**: Data access layer for the SQLite database
- **deploy/**: Contains the Containerfile and deployment resources
  - **ansible/**: Ansible playbooks and roles for Kubernetes/OpenShift deployment
- **tests/**: Contains utility tests for testing and deployment

### Running Tests

- Test with STDIO transport (spawns a new server):

  ```bash
  make test-stdio
  ```

- Test with HTTP transport (requires a running server):

  ```bash
  make run-local  # In one terminal
  make test-http  # In another terminal
  ```

- Test with a full containerized setup:
  ```bash
  make run-with-tests
  ```

## Test Client Usage

The test client (`tests/mcp_client.py`) is provided to help test and verify the functionality of the MCP solution server. It can connect to the server using either HTTP or stdio transport.

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
```

The test client will run through all available tools and resources, demonstrating how to interact with the MCP solution server.

## Integration with Claude and other LLMs

This MCP server can be integrated with Claude and other LLMs that support the Model Context Protocol. For detailed instructions on how to configure Claude Desktop with this MCP server, refer to the [Claude Desktop documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## License

This project is part of the Konveyor/Kai project and is licensed under the same license.
