# uv run -m kai_mcp_solution_server --transport streamable-http --host 0.0.0.0 --port 8000
# uv run llama stack run config/run.yaml

from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="http://localhost:8321")

models = client.models.list()

print("Available models:")
for model in models:
    print(f" - {model.identifier} ({model.model_type})")

print("---")

print("Tool groups:")
for tool_group in client.toolgroups.list():
    print(f" - {tool_group}")

print("---")

print("Tools:")
for tool in client.tools.list():
    print(f" - {tool}")
