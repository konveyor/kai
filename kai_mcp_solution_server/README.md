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
   python tests/test_client.py --transport stdio

   # Test against a running HTTP server
   python tests/test_client.py --transport http --host localhost --port 8000

   # Show detailed output for resources
   python tests/test_client.py --full-output
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

| Tool                     | Description                      | Parameters                                            |
| ------------------------ | -------------------------------- | ----------------------------------------------------- |
| `store_solution`         | Create a new solution            | `task`, `before_code`, `after_code`, `diff`, `status` |
| `find_related_solutions` | Find solutions based on criteria | `task_key`, `limit`                                   |

### Resources

| Resource                            | Description                     | Parameters |
| ----------------------------------- | ------------------------------- | ---------- |
| `kai://success_rate/{task_key}`     | Get success rate for a task     | `task_key` |
| `kai://solutions/{task_key}`        | Get solution history for a task | `task_key` |
| `kai://example_solution/{task_key}` | Get best solution example       | `task_key` |

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

The test client (`tests/test_client.py`) is provided to help test and verify the functionality of the MCP solution server. It can connect to the server using either HTTP or stdio transport.

```bash
# Basic usage with HTTP transport
python tests/test_client.py --transport http --host localhost --port 8000

# Using stdio transport (spawns a server process)
python tests/test_client.py --transport stdio

# Use a specific task key for testing
python tests/test_client.py --task-key migration-task-123

# Show full output for resources instead of truncated summaries
python tests/test_client.py --full-output

# Show verbose output for debugging
python tests/test_client.py --verbose
```

The test client will run through all available tools and resources, demonstrating how to interact with the MCP solution server.

## Integration with Claude and other LLMs

This MCP server can be integrated with Claude and other LLMs that support the Model Context Protocol. For detailed instructions on how to configure Claude Desktop with this MCP server, refer to the [Claude Desktop documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## License

This project is part of the Konveyor/Kai project and is licensed under the same license.
