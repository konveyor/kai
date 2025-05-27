declare module "@modelcontextprotocol/sdk" {
  export class Client {
    constructor(options: { name: string; version: string });
    connect(transport: Transport): Promise<void>;
    callTool(params: { name: string; arguments: any }): Promise<CallToolResult>;
    readResource(params: { uri: string }): Promise<ReadResourceResult>;
  }

  export class SSEClientTransport {
    constructor(url: URL, options?: any);
    close(): Promise<void>;
  }

  export interface Transport {
    close(): Promise<void>;
  }

  export interface ReadResourceResult {
    contents?: Array<{ text?: string; uri?: string }>;
  }

  export interface CallToolResult {
    content?: Array<{ type: string; text?: string }>;
  }
}
