# TypeScript MCP Test Client

A TypeScript test client for the KAI MCP Solution Server, demonstrating Model Context Protocol integration in Node.js environments.

## Features

- **Transport Support**: Both HTTP and stdio transport protocols
- **Authentication**: Bearer token support for HTTP connections
- **SSL Options**: Insecure mode for development and testing
- **MCP Tools**: Tests all available MCP tools including:
  - `create_incident` - Create new migration incidents
  - `create_solution` - Create proposed solutions
  - `update_solution_status` - Update solution status
  - `get_best_hint` - Retrieve migration hints
  - `get_success_rate` - Get success rate metrics
- **TypeScript**: Full type safety and modern async/await patterns

## Installation

```bash
npm install
```

## Usage

### Build the client

```bash
npm run build
```

### Basic Usage

```bash
# Test with stdio transport (default)
node dist/client.js

# Test with HTTP transport
node dist/client.js --transport http --host localhost --port 8000

# Show help
node dist/client.js --help
```

### Advanced Options

```bash
# With authentication
node dist/client.js --transport http --bearer-token "your-jwt-token"

# Skip SSL verification (for testing)
node dist/client.js --transport http --insecure

# Verbose debugging output
node dist/client.js --verbose

# Custom server path for stdio
node dist/client.js --transport stdio --server-path /path/to/server

# Custom mount path for HTTP
node dist/client.js --transport http --mount-path /custom
```

### Makefile Integration

From the main project directory:

```bash
# Test with TypeScript client using stdio
make test-stdio-ts

# Test with TypeScript client using HTTP
make test-http-ts

# With bearer token
make test-http-ts BEARER_TOKEN="your-token"
```

## Configuration Options

| Option           | Description                            | Default     |
| ---------------- | -------------------------------------- | ----------- |
| `--host`         | Server hostname for HTTP transport     | `localhost` |
| `--port`         | Server port for HTTP transport         | `8000`      |
| `--transport`    | Transport protocol (`http` or `stdio`) | `stdio`     |
| `--mount-path`   | Server mount path for HTTP transport   | `/`         |
| `--server-path`  | Server script path for stdio transport | `../`       |
| `--bearer-token` | Bearer token for HTTP authentication   | none        |
| `--insecure`     | Skip SSL verification for HTTP         | `false`     |
| `--verbose`      | Enable debug logging                   | `false`     |

## Architecture

The client is built using:

- **TypeScript**: For type safety and modern JavaScript features
- **@modelcontextprotocol/sdk**: Official MCP SDK for TypeScript/JavaScript
- **Commander.js**: For CLI argument parsing
- **Node.js**: Runtime environment

## Integration Example

This client serves as a reference implementation for integrating MCP servers into TypeScript/Node.js applications:

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

// Create transport
const transport = new StreamableHTTPClientTransport(
  new URL("http://localhost:8000/"),
  {
    requestInit: {
      headers: {
        Authorization: "Bearer your-token",
      },
    },
  },
);

// Create and connect client
const client = new Client({
  name: "my-app",
  version: "1.0.0",
});

await client.connect(transport);

// Call MCP tools
const result = await client.callTool({
  name: "create_incident",
  arguments: {
    client_id: "my-client",
    extended_incident: {
      uri: "file://example.java",
      message: "Migration needed",
      line_number: 42,
      variables: {},
      ruleset_name: "java-ee-to-quarkus",
      violation_name: "jpa-migration",
    },
  },
});
```

## Development

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Run in development mode with file watching
npm run dev

# Run the built client
npm start
```

## Environment Variables

For stdio transport, the client passes these environment variables to the server:

- `KAI_DB_DSN`: Database connection string
- `KAI_LLM_PARAMS`: LLM configuration parameters

Example:

```bash
export KAI_DB_DSN="sqlite+aiosqlite:///kai_mcp_solution_server.db"
export KAI_LLM_PARAMS='{"model": "fake"}'
node dist/client.js
```
