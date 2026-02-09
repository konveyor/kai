# Konveyor AI (Kai) Roadmap

For the current project roadmap and planning, see the [Konveyor project board](https://github.com/orgs/konveyor/projects/72).

## Active Components

- **MCP Solution Server** (`kai_mcp_solution_server/`) - Stores and retrieves
  solved migration examples via the Model Context Protocol.
- **Analyzer RPC** (`kai_analyzer_rpc/`) - Go-based analyzer plugin for serving
  code analysis over RPC.
- **IDE Extension** - The primary Kai product lives in the
  [editor-extensions](https://github.com/konveyor/editor-extensions) repository.

## Guiding Principles

**Model agnostic - Bring Your Own Model**
We recognize the rapid pace of evolving Large Language Models (LLM), for that
reason the team approaches implementation in a manner to allow swappable
artifacts to aid the adoption of various LLM providers.

**Embrace a Learning Mindset for Experiments to Solidify Knowledge**
Konveyor AI is committed to a learning mindset in regard to feature development.
We recognize that not all features will have an immediate beneficial impact, and
the nature of this domain involves making small bets to explore different
approaches.

## Themes

- **Use Konveyor Data to improve generated results** - Improve the RAG approach
  using application modernization data from Konveyor.
- **IDE Integrations** - VSCode, IntelliJ, Eclipse integration with real-time
  analysis updates. See the
  [editor-extensions](https://github.com/konveyor/editor-extensions) repository
  for IDE-related development.
- **Repository Level Code Generation** - Techniques to overcome limited context
  windows for broader repository-level understanding.
- **External Tool integrations** - Integrate linters, compilers, and test
  execution in agent workflows.
- **Evaluation Tools** - Benchmark and measure the quality of generated results.
