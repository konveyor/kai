# Configuring the Kai-IDE Plugin

For initial configuration, see the [configure analysis](./getting_started.md#configure-analysis) steps in the Getting Started guide.

## Advanced Configuration

Access the Kai settings from `Extensions > Konveyor AI Extension for VS Code settings icon > Settings`.

This will bring you to the screen shown below.  
 ![advancedConfig](images/advanced_config.png)

### Understanding the Settings

#### **Log Level**

Defines the logging level for server binaries. Logs can be found in your project directory under `/.vscode/konveyor-logs`.  
The verbosity of event logs can be increased or decreased using this option.

#### **Analyzer Path**

Allows the user to specify a custom analyzer binary path. If not provided, the default analyzer binary will be used.

#### **Diff: Auto Accept on Save**

Allows users to automatically apply diff changes when saving files.

#### **Analysis: Analyze on Save**

Enables real-time analysis upon saving a file.  
This is automatically enabled while using Agent Mode

#### **Genai: Agent Mode**

Use agentic flow for getting solutions using automatic analysis.  
Read more about Agent Mode [here](./getting_started.md#agent-mode).

#### **Genai: Cache Dir**

Path to a directory containing cached responses

#### **Genai: Trace Dir**

Path to directory containing traces of LLM interactions

#### **Genai: Trace Enabled**

Enables tracing of communication with the model. If enabled, traces will be stored under `/.vscode/konveyor-logs/traces`.

#### **Genai: Demo Mode**

Enables Kai’s **demo mode**, which uses cached LLM responses for learning and testing functionality.  
Click [here](./demo_mode.md) for more information on Demo Mode.

#### **Solution Server**

Configuration for the solution server. Read more details [here](./getting_started.md#solution-server).

#### **Debug: Webview**

Debug logging for webview message handilng
