/**
 * MCP Solution Server Test Client
 *
 * This script tests the functionality of the MCP Solution Server by establishing
 * a proper Model Context Protocol connection and testing the available tools and resources.
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

// Configure logging
const verbose =
  process.argv.includes("--verbose") || process.argv.includes("-v");
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
 * Test the store_solution tool by creating a new solution.
 */
async function testStoreSolution(client: Client): Promise<number> {
  console.log("\n--- Testing store_solution ---");

  const task = {
    key: "test-migration",
    description: "Test migration task",
    source_framework: "java-ee",
    target_framework: "quarkus",
    language: "java",
  };
  logger.debug("Preparing task data: %o", task);

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
  logger.debug(`Before code prepared (length: ${beforeCode.length})`);

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
  logger.debug(`After code prepared (length: ${afterCode.length})`);

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
  logger.debug(`Diff prepared (length: ${diff.length})`);
  const status = "accepted";

  try {
    logger.debug(`Calling store_solution tool with status: ${status}`);
    const result = await client.callTool({
      name: "store_solution",
      arguments: {
        task,
        before_code: beforeCode,
        after_code: afterCode,
        diff,
        status,
      },
    });
    logger.debug("store_solution tool call completed, processing result");

    // Extract the solution ID from the result
    let solutionId: number | undefined;
    if (result?.content && Array.isArray(result.content)) {
      logger.debug(
        `Result has content attribute with ${result.content.length} items`,
      );
      for (const contentItem of result.content) {
        if (contentItem.type === "text" && contentItem.text) {
          try {
            solutionId = parseInt(contentItem.text, 10);
            logger.debug(`Found solution_id: ${solutionId}`);
            break;
          } catch (e) {
            logger.debug(
              `Failed to parse content item as integer: ${contentItem.text}`,
            );
          }
        } else {
          logger.debug(`Content item has no text attribute: %o`, contentItem);
        }
      }
    }

    console.log(`✅ Solution created with ID: ${solutionId}`);
    return solutionId || -1;
  } catch (e) {
    logger.error(`Error creating solution: ${e}`);
    console.log(`❌ Error creating solution: ${e}`);
    return -1;
  }
}

/**
 * Test the find_related_solutions tool by searching for existing solutions.
 */
async function testRelatedSolutions(
  client: Client,
  taskKey: string,
): Promise<void> {
  console.log("\n--- Testing find_related_solutions ---");

  try {
    logger.debug(
      `Calling find_related_solutions tool with task_key: ${taskKey}, limit: 5`,
    );
    const result = await client.callTool({
      name: "find_related_solutions",
      arguments: {
        task_key: taskKey,
        limit: 5,
      },
    });
    logger.debug(
      "find_related_solutions tool call completed, processing result",
    );

    // Extract the solutions from the result
    const solutions: any[] = [];
    if (result?.content && Array.isArray(result.content)) {
      logger.debug(
        `Result has content attribute with ${result.content.length} items`,
      );
      for (const contentItem of result.content) {
        if (contentItem.type === "text" && contentItem.text) {
          try {
            // Parse each item as an individual JSON object
            const truncatedText =
              contentItem.text.length > 100
                ? contentItem.text.substring(0, 100) + "..."
                : contentItem.text;
            logger.debug(`Parsing JSON from content item: ${truncatedText}`);

            const solutionData = JSON.parse(contentItem.text);
            solutions.push(solutionData);
            logger.debug(
              `Successfully parsed JSON solution: ${solutionData.id || "No ID"}`,
            );
          } catch (e) {
            logger.error(`Failed to parse JSON: ${e}`);
            console.log(`Failed to parse JSON from: ${contentItem.text}`);
          }
        } else {
          logger.debug(`Content item has no text attribute: %o`, contentItem);
        }
      }
    }

    if (solutions.length > 0) {
      logger.debug(`Found ${solutions.length} solutions`);
      console.log(`✅ Found ${solutions.length} related solutions:`);
      for (let i = 0; i < solutions.length; i++) {
        const solution = solutions[i];
        logger.debug(`Processing solution ${i}: ${solution.id}`);
        console.log(`  - ID: ${solution.id}`);
        console.log(`    Status: ${solution.status}`);
        console.log(`    Task Key: ${solution.task_key}`);

        // Add snippet of before/after code if available
        const beforeCode = solution.before_code || "";
        const afterCode = solution.after_code || "";

        if (beforeCode) {
          logger.debug(
            `Solution has before_code (length: ${beforeCode.length})`,
          );
          console.log(
            beforeCode.length > 30
              ? `    Before: ${beforeCode.substring(0, 30)}...`
              : `    Before: ${beforeCode}`,
          );
        }
        if (afterCode) {
          logger.debug(`Solution has after_code (length: ${afterCode.length})`);
          console.log(
            afterCode.length > 30
              ? `    After: ${afterCode.substring(0, 30)}...`
              : `    After: ${afterCode}`,
          );
        }

        console.log();
      }
    } else {
      logger.debug(`No solutions found for task_key: ${taskKey}`);
      console.log("ℹ️ No related solutions found");
    }
  } catch (e) {
    logger.error(`Error finding related solutions: ${e}`);
    console.log(`❌ Error finding related solutions: ${e}`);
  }
}

/**
 * Test the success_rate resource by getting the success rate for a task key.
 */
async function testSuccessRate(client: Client, taskKey: string): Promise<void> {
  console.log("\n--- Testing success_rate resource ---");

  try {
    const resourceUri = `kai://success_rate/${taskKey}`;
    logger.debug(`Reading resource: ${resourceUri}`);
    const result = await client.readResource({
      uri: resourceUri,
    });
    logger.debug("Resource read completed, processing result");

    // Extract the content from ReadResourceResult
    let content = "";
    if (
      result?.contents &&
      Array.isArray(result.contents) &&
      result.contents.length > 0
    ) {
      logger.debug(
        `Result has contents attribute with ${result.contents.length} items`,
      );
      for (const contentItem of result.contents) {
        if ("text" in contentItem && typeof contentItem.text === "string") {
          content = contentItem.text;
          logger.debug(`Found content text: ${content}`);
          break;
        } else {
          logger.debug(`Content item has no text attribute: %o`, contentItem);
        }
      }
    }

    if (content) {
      logger.debug("Successfully retrieved success rate information");
      console.log(`✅ ${content}`);
    } else {
      logger.debug(
        `No success rate information available for task_key: ${taskKey}`,
      );
      console.log("ℹ️ No success rate information available");
    }
  } catch (e) {
    logger.error(`Error fetching success rate: ${e}`);
    console.log(`❌ Error fetching success rate: ${e}`);
  }
}

/**
 * Run all tests with the MCP client
 */
async function runTests(
  host: string,
  port: number,
  taskKey: string,
): Promise<void> {
  // Setup HTTP transport using SSE
  const serverUrl = `http://${host}:${port}/sse`;
  console.log(`Connecting to server at ${serverUrl}...`);

  try {
    // Create SSE transport
    const transport = new SSEClientTransport(new URL(serverUrl));

    // Create client
    const client = new Client({
      name: "ts-mcp-client",
      version: "1.0.0",
    });

    try {
      // Connect client to transport
      await client.connect(transport);
      console.log("Connected to MCP server successfully!");

      // Run tests
      const solutionId = await testStoreSolution(client);

      // Wait a bit for data to be persisted
      console.log("Waiting for database operations to complete...");
      await new Promise((resolve) => setTimeout(resolve, 1000));

      await testRelatedSolutions(client, taskKey);
      await testSuccessRate(client, taskKey);

      console.log("\n✅ All tests completed successfully!");
    } finally {
      // Clean up
      await transport.close();
      console.log("Disconnected from MCP server");
    }
  } catch (e) {
    console.error(`Error connecting to MCP server: ${e}`);
    process.exit(1);
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
const host = args.includes("--host")
  ? args[args.indexOf("--host") + 1]
  : "localhost";
const port = args.includes("--port")
  ? parseInt(args[args.indexOf("--port") + 1], 10)
  : 8000;
const taskKey = args.includes("--task-key")
  ? args[args.indexOf("--task-key") + 1]
  : "test-migration";

// Print help if requested
if (args.includes("--help") || args.includes("-h")) {
  console.log("Usage: node client.js [options]");
  console.log("Options:");
  console.log(
    "  --host <host>        Host name of the MCP server (default: localhost)",
  );
  console.log("  --port <port>        Port of the MCP server (default: 8000)");
  console.log(
    "  --task-key <key>     Task key to use for tests (default: test-migration)",
  );
  console.log("  --verbose, -v        Show detailed debug information");
  console.log("  --help, -h           Show this help message");
  process.exit(0);
}

// Run the tests
runTests(host, port, taskKey).catch((err) => {
  console.error("Unhandled error:", err);
  process.exit(1);
});
