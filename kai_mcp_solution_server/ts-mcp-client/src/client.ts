/**
 * MCP Solution Server Test Client
 *
 * This script tests the functionality of the MCP Solution Server by establishing
 * a proper Model Context Protocol connection and testing the available tools and resources.
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { spawn } from "child_process";
import { Command } from "commander";
import * as https from "https";
import { URL } from "url";
import * as process from "process";

// Type definitions for our data structures
interface ExtendedIncident {
  uri: string;
  message: string;
  line_number: number;
  variables: Record<string, any>;
  ruleset_name: string;
  violation_name: string;
}

interface SolutionFile {
  uri: string;
  content: string;
}

interface SolutionChangeSet {
  diff: string;
  before: SolutionFile[];
  after: SolutionFile[];
}

interface ViolationID {
  ruleset_name: string;
  violation_name: string;
}

interface MCPClientConfig {
  host: string;
  port: number;
  transport: "http" | "stdio";
  serverPath: string;
  mountPath: string;
  verbose: boolean;
  insecure: boolean;
  bearerToken?: string;
}

// Configure logging
let verbose = false;
const logger = {
  debug: (message: string, ...args: any[]) => {
    if (verbose) console.log(`DEBUG - ${message}`, ...args);
  },
  info: (message: string, ...args: any[]) =>
    console.log(`INFO - ${message}`, ...args),
  error: (message: string, ...args: any[]) =>
    console.error(`ERROR - ${message}`, ...args),
};

/**
 * Generate a random client ID for testing
 */
function generateClientId(): string {
  return (
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15)
  );
}

/**
 * Test the create_incident tool by creating a new incident.
 */
async function runCreateIncident(
  client: Client,
  clientId: string,
): Promise<number> {
  console.log("\n--- Testing create_incident ---");

  const extendedIncident: ExtendedIncident = {
    uri: "file://ExampleService.java",
    message: "Example incident for testing",
    line_number: 1,
    variables: {},
    ruleset_name: "test-ruleset",
    violation_name: "test-violation",
  };

  const request = {
    client_id: clientId,
    extended_incident: extendedIncident,
  };

  logger.debug(`Preparing create_incident request: ${JSON.stringify(request)}`);

  try {
    const result = await client.callTool({
      name: "create_incident",
      arguments: request,
    });

    // Extract incident ID from result
    let incidentId: number | undefined;
    if (result?.content && Array.isArray(result.content)) {
      for (const contentItem of result.content) {
        if (contentItem.type === "text" && contentItem.text) {
          incidentId = parseInt(contentItem.text, 10);
          break;
        }
      }
    }

    if (incidentId === undefined) {
      throw new Error("Incident ID is undefined, check server response");
    }

    console.log(`✅ Incident created with ID: ${incidentId}`);
    return incidentId;
  } catch (e) {
    logger.error(`Error creating incident: ${e}`);
    console.log(`❌ Error creating incident: ${e}`);
    throw e;
  }
}

/**
 * Test the create_solution tool by creating a new solution.
 */
async function runCreateSolution(
  client: Client,
  clientId: string,
  incidentIds: number[],
): Promise<number> {
  console.log("\n--- Testing create_solution ---");

  const beforeCode = `
// Original Java EE code
@Stateless
public class ExampleService {
    @PersistenceContext
    private EntityManager em;

    public List<Entity> findAll() {
        return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
    }
}
`;

  const afterCode = `
// Migrated Quarkus code
@ApplicationScoped
public class ExampleService {
    @Inject
    EntityManager em;

    public List<Entity> findAll() {
        return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
    }
}
`;

  const diff = `
-// Original Java EE code
-@Stateless
+// Migrated Quarkus code
+@ApplicationScoped
 public class ExampleService {
-    @PersistenceContext
+    @Inject
     private EntityManager em;

     public List<Entity> findAll() {
         return em.createQuery("SELECT e FROM Entity e", Entity.class).getResultList();
     }
 }
`;

  logger.debug(`Before code prepared (length: ${beforeCode.length})`);
  logger.debug(`After code prepared (length: ${afterCode.length})`);
  logger.debug(`Diff prepared (length: ${diff.length})`);

  const changeSet: SolutionChangeSet = {
    diff: diff,
    before: [
      {
        uri: "file://ExampleService.java",
        content: beforeCode,
      },
    ],
    after: [
      {
        uri: "file://ExampleService.java",
        content: afterCode,
      },
    ],
  };

  const request = {
    client_id: clientId,
    incident_ids: incidentIds,
    change_set: changeSet,
  };

  try {
    logger.debug("Calling create_solution tool");
    const result = await client.callTool({
      name: "create_solution",
      arguments: request,
    });

    // Extract solution ID from result
    let solutionId: number | undefined;
    if (result?.content && Array.isArray(result.content)) {
      for (const contentItem of result.content) {
        if (contentItem.type === "text" && contentItem.text) {
          solutionId = parseInt(contentItem.text, 10);
          break;
        }
      }
    }

    if (solutionId === undefined) {
      throw new Error("Solution ID is undefined, check server response");
    }

    console.log(`✅ Solution created with ID: ${solutionId}`);
    return solutionId;
  } catch (e) {
    logger.error(`Error creating solution: ${e}`);
    console.log(`❌ Error creating solution: ${e}`);
    throw e;
  }
}

/**
 * Test the accept_file tool.
 */
async function runAcceptFile(client: Client, clientId: string): Promise<void> {
  console.log("\n--- Testing accept_file ---");

  const request = {
    client_id: clientId,
    solution_file: {
      uri: "file://ExampleService.java",
      content: "//example content",
    },
  };

  try {
    logger.debug(
      `Calling accept_file tool with request: ${JSON.stringify(request)}`,
    );
    const result = await client.callTool({
      name: "accept_file",
      arguments: request,
    });
    logger.debug(
      `accept_file tool call completed, result: ${JSON.stringify(result)}`,
    );
    console.log("✅ File accepted successfully");
  } catch (e) {
    logger.error(`Error accepting file: ${e}`);
    console.log(`❌ Error accepting file: ${e}`);
    throw e;
  }
}

/**
 * Test the get_best_hint tool.
 */
async function runGetBestHint(client: Client): Promise<any> {
  console.log("\n--- Testing get_best_hint ---");

  const request = {
    ruleset_name: "test-ruleset",
    violation_name: "test-violation",
  };

  try {
    logger.debug(`Preparing get_best_hint request: ${JSON.stringify(request)}`);
    const result = await client.callTool({
      name: "get_best_hint",
      arguments: request,
    });

    console.log(
      `get_best_hint tool call completed, result: ${JSON.stringify(result)}`,
    );

    if (
      !result?.content ||
      !Array.isArray(result.content) ||
      result.content.length === 0
    ) {
      console.log("ℹ️ No related solutions found");
      return null;
    }

    return result;
  } catch (e) {
    logger.error(`Error finding related solutions: ${e}`);
    console.log(`❌ Error finding related solutions: ${e}`);
    throw e;
  }
}

/**
 * Test the get_success_rate tool.
 */
async function runGetSuccessRate(client: Client): Promise<any> {
  console.log("\n--- Testing get_success_rate ---");

  const violationIds: ViolationID[] = [
    {
      violation_name: "test-violation",
      ruleset_name: "test-ruleset",
    },
  ];

  const request = {
    violation_ids: violationIds,
  };

  try {
    logger.debug(
      `Preparing get_success_rate request: ${JSON.stringify(request)}`,
    );
    const result = await client.callTool({
      name: "get_success_rate",
      arguments: request,
    });

    console.log(
      `get_success_rate tool call completed, result: ${JSON.stringify(result)}`,
    );

    if (
      !result?.content ||
      !Array.isArray(result.content) ||
      result.content.length === 0
    ) {
      console.log("ℹ️ No success rate data found");
      return null;
    }

    return result;
  } catch (e) {
    logger.error(`Error retrieving success rate: ${e}`);
    console.log(`❌ Error retrieving success rate: ${e}`);
    throw e;
  }
}

/**
 * Apply SSL bypass for insecure connections (Node.js specific)
 */
function applySSLBypass(): () => void {
  logger.debug("Applying SSL bypass for insecure connections");

  // Store original values
  const originalRejectUnauthorized = process.env.NODE_TLS_REJECT_UNAUTHORIZED;

  // Disable SSL verification through environment variable
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

  console.log("⚠️ Warning: SSL certificate verification is disabled");

  // Return cleanup function
  return () => {
    logger.debug("Restoring SSL settings");
    if (originalRejectUnauthorized !== undefined) {
      process.env.NODE_TLS_REJECT_UNAUTHORIZED = originalRejectUnauthorized;
    } else {
      delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    }
  };
}

/**
 * Run the full test suite against an initialized MCP client.
 */
async function runTestSuite(client: Client): Promise<void> {
  console.log("Connected to MCP server successfully!");
  logger.debug("MCP client connection established");

  // Generate a client ID
  const clientId = generateClientId();
  console.log(`Using client ID: ${clientId}`);

  // Run tests
  const incidentId = await runCreateIncident(client, clientId);
  logger.debug(
    `create_incident test completed with incident_id: ${incidentId}`,
  );

  const solutionId = await runCreateSolution(client, clientId, [incidentId]);
  logger.debug(
    `create_solution test completed with solution_id: ${solutionId}`,
  );

  await runAcceptFile(client, clientId);
  logger.debug("accept_file test completed");

  const bestHint = await runGetBestHint(client);
  logger.debug(
    `get_best_hint test completed with result: ${JSON.stringify(bestHint)}`,
  );

  const successRates = await runGetSuccessRate(client);
  logger.debug(
    `get_success_rate test completed with result: ${JSON.stringify(successRates)}`,
  );

  console.log("\n✅ All tests completed successfully!");
  logger.debug("All test functions completed successfully");
}

/**
 * Run all tests with the appropriate transport.
 */
async function runTests(config: MCPClientConfig): Promise<boolean> {
  console.log("MCP Solution Server Test Client");
  console.log("==============================");
  console.log(`Host: ${config.host}`);
  console.log(`Port: ${config.port}`);
  console.log(`Transport: ${config.transport}`);

  if (config.insecure && config.transport === "http") {
    console.log("SSL verification: Disabled (insecure mode)");
  }

  logger.debug(`Starting test run with config: ${JSON.stringify(config)}`);

  let cleanupSSL: (() => void) | undefined;

  try {
    let transport: StreamableHTTPClientTransport | StdioClientTransport;
    let clientOptions: any = {
      name: "ts-mcp-client",
      version: "1.0.0",
    };

    if (config.transport === "http") {
      // Setup HTTP transport
      let serverUrl = "";
      if (!config.host.startsWith("http")) {
        serverUrl = "http://";
      }
      let host = config.host;
      if (host.endsWith(config.mountPath)) {
        host = host.slice(0, -config.mountPath.length);
      }
      serverUrl += `${host}:${config.port}${config.mountPath}`;

      console.log(`Connecting to server at ${serverUrl}...`);
      logger.debug(`Initializing HTTP transport with URL: ${serverUrl}`);

      if (config.insecure) {
        logger.debug("Applying SSL bypass to disable certificate verification");
        cleanupSSL = applySSLBypass();
      }

      // Create HTTP transport with optional authentication
      const transportOptions: any = {};

      if (config.bearerToken) {
        transportOptions.requestInit = {
          headers: {
            Authorization: `Bearer ${config.bearerToken}`,
          },
        };
        logger.debug("Added bearer token authentication");
        console.log("🔐 Bearer token authentication enabled");
      }

      transport = new StreamableHTTPClientTransport(
        new URL(serverUrl),
        transportOptions,
      );
    } else {
      // Setup stdio transport
      console.log(`Using server path: ${config.serverPath}`);
      logger.debug(
        `Initializing STDIO transport with server path: ${config.serverPath}`,
      );

      // Spawn the server process
      const serverProcess = spawn(
        "python",
        ["-m", "kai_mcp_solution_server", "--transport", "stdio"],
        {
          cwd: config.serverPath,
          env: {
            ...process.env,
            KAI_DB_DSN:
              process.env.KAI_DB_DSN ||
              "sqlite+aiosqlite:///kai_mcp_solution_server.db",
            KAI_LLM_PARAMS: process.env.KAI_LLM_PARAMS || '{"model": "fake"}',
          },
        },
      );

      transport = new StdioClientTransport({
        command: "python",
        args: ["-m", "kai_mcp_solution_server", "--transport", "stdio"],
        env: {
          ...process.env,
          KAI_DB_DSN:
            process.env.KAI_DB_DSN ||
            "sqlite+aiosqlite:///kai_mcp_solution_server.db",
          KAI_LLM_PARAMS: process.env.KAI_LLM_PARAMS || '{"model": "fake"}',
        },
        cwd: config.serverPath,
      });
    }

    logger.debug(`Client options: ${JSON.stringify(clientOptions)}`);

    try {
      // Create MCP client
      const client = new Client(clientOptions, {
        capabilities: {
          tools: {},
          resources: {},
        },
      });

      const runWithTimeout = async (): Promise<boolean> => {
        await client.connect(transport);
        logger.debug(
          `${config.transport.toUpperCase()} client connection established`,
        );
        await runTestSuite(client);
        logger.debug(
          `Test suite completed successfully with ${config.transport.toUpperCase()} transport`,
        );
        return true;
      };

      // Run with timeout to prevent hanging indefinitely
      return await Promise.race([
        runWithTimeout(),
        new Promise<boolean>((_, reject) =>
          setTimeout(() => reject(new Error("Timeout")), 15000),
        ),
      ]);
    } catch (e) {
      if (e instanceof Error && e.message === "Timeout") {
        logger.error(
          `${config.transport.toUpperCase()} transport timed out after 15 seconds`,
        );
        console.log(
          `❌ ${config.transport.toUpperCase()} transport timed out after 15 seconds`,
        );
        return false;
      }

      logger.error(`${config.transport.toUpperCase()} transport error: ${e}`);
      console.log(
        `❌ Error with ${config.transport.toUpperCase()} transport: ${e}`,
      );

      if (config.transport === "http") {
        console.log(`! Make sure the server is running at the specified URL`);
        if (
          e instanceof Error &&
          (e.message.toLowerCase().includes("ssl") ||
            e.message.toLowerCase().includes("certificate"))
        ) {
          console.log(
            "! SSL certificate verification error. Try --insecure flag for testing",
          );
        }
        console.log(
          "! Try using the STDIO transport instead with --transport stdio",
        );
      } else {
        console.log(
          `! Make sure the server script exists: ${config.serverPath}`,
        );
      }

      return false;
    }
  } catch (e) {
    logger.error(`Unexpected error: ${e}`);
    console.log(`❌ Unexpected error: ${e}`);
    return false;
  } finally {
    // Clean up SSL patches if they were applied
    if (cleanupSSL) {
      cleanupSSL();
    }
  }
}

/**
 * Main function to parse arguments and run tests.
 */
async function main(): Promise<void> {
  const program = new Command();

  program
    .name("ts-mcp-client")
    .description("TypeScript test client for MCP Solution Server")
    .version("1.0.0")
    .option(
      "--host <host>",
      "Hostname of the MCP server (for http transport)",
      "localhost",
    )
    .option(
      "--port <port>",
      "Port of the MCP server (for http transport)",
      "8000",
    )
    .option(
      "--transport <transport>",
      "Transport protocol (http or stdio)",
      "stdio",
    )
    .option(
      "--mount-path <path>",
      "Path the MCP server is mounted behind (for http transport)",
      "/",
    )
    .option(
      "--server-path <path>",
      "Path to the MCP server script (for stdio transport)",
      "../",
    )
    .option("--verbose, -v", "Show detailed debug information")
    .option(
      "--insecure",
      "Allow insecure connections (skip SSL verification for http transport)",
    )
    .option(
      "--bearer-token <token>",
      "Bearer token for authentication (for http transport)",
    );

  program.parse();

  const options = program.opts();

  // Set verbose logging
  verbose = options.verbose;
  if (verbose) {
    logger.debug("Debug logging enabled");
  }

  const config: MCPClientConfig = {
    host: options.host,
    port: parseInt(options.port, 10),
    transport: options.transport as "http" | "stdio",
    serverPath: options.serverPath,
    mountPath: options.mountPath,
    verbose: options.verbose,
    insecure: options.insecure,
    bearerToken: options.bearerToken,
  };

  const success = await runTests(config);
  process.exit(success ? 0 : 1);
}

// Run the main function
main().catch((err) => {
  console.error("Unhandled error:", err);
  process.exit(1);
});
