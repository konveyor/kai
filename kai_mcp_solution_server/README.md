# Kai Solution MCP Server

A Model Context Protocol (MCP) server for managing Kai solutions database. This server allows AI agents to store, retrieve, and analyze solutions for code migration tasks.

## Overview

<img src="https://img.shields.io/badge/MCP-Compatible-blue" alt="MCP Compatible">

This MCP server provides tools and resources for managing code migration solutions used by the [Konveyor/Kai](https://github.com/konveyor/kai) project, which assists with modernizing application source code to new platforms via Generative AI.

The server implements the following functionality:

- Store and manage solutions for code migration tasks
- Query success rates for specific migration tasks
- Find related solutions for LLM retrieval augmented generation (RAG)
- Format solution examples for LLM consumption

## Installation

### Prerequisites

- Python 3.9 or higher
- pip

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/kai-mcp-server.git
   cd kai-mcp-server
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   .venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install mcp-sdk
   ```

## Running the Server

Start the MCP server:

```bash
python main.py
```

The server will run using the STDIO transport, which is the standard transport for MCP servers.

## Development and Testing

### Creating Test Data

You can use the MCP Inspector to create test data for your Kai solutions database:

1. Use the `store_solution` tool to create a new solution
2. Provide test data in the parameters
3. Update the solution status using the `update_solution_status` tool
4. Test querying success rates and retrieving solutions

## Integration with Claude Desktop

To use this MCP server with Claude Desktop:

1. Make sure you have Claude Desktop installed
2. Open the Claude Desktop configuration file:

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add your server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "kaiSolutions": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/your/kai-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

4. Restart Claude Desktop

## API Reference

### Tools

| Tool                     | Description                      | Parameters                                            |
| ------------------------ | -------------------------------- | ----------------------------------------------------- |
| `store_solution`         | Create a new solution            | `task`, `before_code`, `after_code`, `diff`, `status` |
| `update_solution_status` | Update solution status           | `solution_id`, `status`                               |
| `find_related_solutions` | Find solutions based on criteria | `task_key`, `limit`                                   |

### Resources

| Resource                            | Description                     | Parameters |
| ----------------------------------- | ------------------------------- | ---------- |
| `kai://success_rate/{task_key}`     | Get success rate for a task     | `task_key` |
| `kai://solutions/{task_key}`        | Get solution history for a task | `task_key` |
| `kai://example_solution/{task_key}` | Get best solution example       | `task_key` |

## Architecture

This project consists of two main components:

1. **DAO Layer** (`kai_solutions_dao.py`):

   - Data structures and database operations
   - Connection pool management
   - Solution querying and filtering logic

2. **MCP Server** (`main.py`):
   - MCP server setup and lifecycle management
   - Tool implementations
   - Resource formatting and exposure

## Example Usage with Claude

Once connected to Claude Desktop, you can interact with your database using natural language:

```
Could you create a new solution for migrating from Java EE to Quarkus? Here's an example:

Task:
{
  "key": "jms-to-quarkus",
  "description": "Convert JMS Topic to Quarkus Reactive Messaging",
  "source_framework": "java-ee",
  "target_framework": "quarkus",
  "language": "java"
}

Before code:
@Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
private Topic topic;

After code:
@Inject
@Channel("prices")
Emitter<String> pricesEmitter;

Diff:
- @Resource(lookup = "java:/topic/HELLOWORLDMDBTopic")
- private Topic topic;
+ @Inject
+ @Channel("prices")
+ Emitter<String> pricesEmitter;
```

Then you can ask about success rates:

```
What's the success rate for jms-to-quarkus migrations?
```

Or find related solutions:

```
Can you find me related solutions for Java EE to Quarkus migrations involving JMS?
```
