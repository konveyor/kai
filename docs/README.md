# Konveyor AI (Kai) Documentation

## End Users

For installation, configuration, and usage of the Kai IDE extension, see the
[editor-extensions](https://github.com/konveyor/editor-extensions) repository
and the
[extension README](https://github.com/konveyor/editor-extensions/blob/main/vscode/core/README.md).

### Migration Scenarios

Step-by-step walkthroughs for common migration tasks:

- [Scenarios overview](scenarios/README.md)
- [Java EE to Quarkus](scenarios/javaEE_to_quarkus/README.md)
- [JDK 8 to 17](scenarios/jdk_8_to_17_migration/README.md)
- [Migrating custom library apps using solution server](scenarios/migrating_custom_library_apps_using_solution_server/)

### Other Guides

- [Demo Mode](demo_mode.md) - Using cached LLM responses for demos and testing

## Backend Components

- [MCP Solution Server](../kai_mcp_solution_server/README.md) - Stores and
  retrieves solved migration examples via the Model Context Protocol

## Design

- [Technical Background](design/technical_background.md)
- [Solved Incident Store](design/solved_incident_store.md)
- [Hub Integration](design/hub_integration.md)

## Contributing

- [Development Environment](contrib/dev_environment.md)
- [Testing](contrib/testing.md)
