# Makefile for Kai MCP Solution Server

# Configuration
IMAGE ?= quay.io/konveyor/kai-mcp-solution-server:latest
NAMESPACE ?= konveyor-kai-solution-server
MOUNT_PATH ?= ""
KAI_DB_DSN ?= sqlite+aiosqlite:///kai_solution_server.db

# Directories
PROJECT_ROOT = $(shell pwd)

BUILD_DIR = $(PROJECT_ROOT)/tools/deploy

TESTS_DIR = $(PROJECT_ROOT)/tests

HOST ?= localhost
PORT ?= 8000
BEARER_TOKEN ?=

# Default target
.PHONY: all
all: build

# Build the container image with Podman
.PHONY: build
build:
	@echo "Building container image $(IMAGE) with Podman..."

	podman build -t $(IMAGE) -f $(BUILD_DIR)/Containerfile $(PROJECT_ROOT)


# Push the container image to the registry
.PHONY: push
push:
	@echo "Pushing container image $(IMAGE)..."
	podman push $(IMAGE)


# Deploy to Kubernetes/OpenShift
# Usage: make deploy [NAMESPACE="..."] [IMAGE="..."] [EXTRA_VARS="..."]
# Example: make deploy EXTRA_VARS="storage_class=gp2 storage_size=5Gi route_tls_enabled=false"
.PHONY: deploy
deploy: build push
	@echo "Deploying to Kubernetes/OpenShift..."
	cd $(BUILD_DIR)/ansible && ansible-playbook deploy.yml \
		-e "namespace=$(NAMESPACE)" \
		-e "image=$(IMAGE)" \
		-e "state=present" \
		$(if $(EXTRA_VARS),-e "$(EXTRA_VARS)",)
	@echo "Deployment complete. To check status: make status"

# Delete the deployment
# Usage: make undeploy [NAMESPACE="..."] [EXTRA_VARS="..."]
.PHONY: undeploy
undeploy:
	@echo "Undeploying from Kubernetes/OpenShift..."
	cd $(BUILD_DIR)/ansible && ansible-playbook deploy.yml \
		-e "namespace=$(NAMESPACE)" \
		-e "state=absent" \
		$(if $(EXTRA_VARS),-e "$(EXTRA_VARS)",)
	@echo "Undeployment complete."

# Check deployment status
.PHONY: status
status:
	@echo "Checking deployment status in namespace $(NAMESPACE)..."
	kubectl get all,ingress,pvc -n $(NAMESPACE) -l app=kai-mcp-solution-server

# Clean up local resources
.PHONY: clean
clean:
	@echo "Cleaning local resources..."
	-podman rmi $(IMAGE) 2>/dev/null || true

# Port forward for local testing
.PHONY: port-forward
port-forward:
	@echo "Port forwarding to localhost:8000..."
	kubectl port-forward -n $(NAMESPACE) svc/kai-mcp-solution-server 8000:8000

# Run locally for testing
.PHONY: run-local
run-local:
	@echo "Running MCP solution server locally..."
	@if [ -z "$(KAI_LLM_PARAMS)" ]; then echo "Error: KAI_LLM_PARAMS is required"; exit 1; fi
	cd $(PROJECT_ROOT) && KAI_DB_DSN='$(KAI_DB_DSN)' KAI_LLM_PARAMS='$(KAI_LLM_PARAMS)' uv run python -m kai_mcp_solution_server --transport streamable-http --host 0.0.0.0 --port 8000 --mount-path=$(MOUNT_PATH)


# Run with Podman for testing (flexible - any database via KAI_DB_DSN)
.PHONY: run-podman
run-podman: build
	@echo "Running MCP solution server in Podman..."
	@if [ -z "$(KAI_LLM_PARAMS)" ]; then echo "Error: KAI_LLM_PARAMS is required"; exit 1; fi
	podman run --rm -it -p 8000:8000 \
		-e MOUNT_PATH='$(MOUNT_PATH)' \
		-e KAI_LLM_PARAMS='$(KAI_LLM_PARAMS)' \
		-e KAI_DB_DSN='$(KAI_DB_DSN)' \
		$(if $(PODMAN_ARGS),$(PODMAN_ARGS),) \
		--name kai-mcp-solution-server $(IMAGE)

# Convenience target: Run with PostgreSQL via podman-compose
.PHONY: podman-postgres
podman-postgres: build
	@echo "Starting MCP solution server with PostgreSQL using podman-compose..."
	@if [ -z "$(KAI_LLM_PARAMS)" ]; then echo "Error: KAI_LLM_PARAMS is required"; exit 1; fi
	IMAGE=$(IMAGE) KAI_LLM_PARAMS='$(KAI_LLM_PARAMS)' MOUNT_PATH='$(MOUNT_PATH)' \
		podman-compose up --force-recreate


# Run stress test against external server (e.g., one started with run-local or podman-postgres)
# First start a server: make run-local or make podman-postgres
# Then run: make test-stress
.PHONY: test-stress
test-stress:
	@if [ -z "$${MCP_SERVER_URL}" ]; then \
		echo "Error: MCP_SERVER_URL is required for stress testing."; \
		echo "Start a server first:"; \
		echo "  make run-local"; \
		echo "  make podman-postgres"; \
		echo "Then set MCP_SERVER_URL and run the stress test:"; \
		echo "  MCP_SERVER_URL=http://localhost:8000 make test-stress"; \
		exit 1; \
	fi
	@echo "Running stress test against external server at $${MCP_SERVER_URL}"
	@echo "Testing with $${NUM_CONCURRENT_CLIENTS:-30} concurrent clients..."
	MCP_SERVER_URL=$${MCP_SERVER_URL} \
	NUM_CONCURRENT_CLIENTS=$${NUM_CONCURRENT_CLIENTS:-30} \
	uv run python -m pytest tests/test_multiple_integration.py::TestMultipleIntegration::test_multiple_users -xvs

# Test against HTTP server
.PHONY: test-http
test-http:
	@echo "Running MCP test client against HTTP server..."
	@echo "Make sure the server is running with 'make run-local' or 'make run-podman'"
	cd $(PROJECT_ROOT)/.. && python $(TESTS_DIR)/mcp_client.py --transport http --host $(HOST) --port $(PORT) --insecure --mount-path $(MOUNT_PATH) $(if $(BEARER_TOKEN),--bearer-token $(BEARER_TOKEN),)

# Test against HTTP server with TypeScript client
.PHONY: test-http-ts
test-http-ts:
	@echo "Running TypeScript MCP test client against HTTP server..."
	@echo "Make sure the server is running with 'make run-local' or 'make run-podman'"
	cd $(PROJECT_ROOT)/ts-mcp-client && npm run build && node --es-module-specifier-resolution=node dist/client.js --transport http --host $(HOST) --port $(PORT) --insecure --mount-path $(MOUNT_PATH) $(if $(BEARER_TOKEN),--bearer-token $(BEARER_TOKEN),)

# Test using stdio transport
.PHONY: test-stdio
test-stdio:
	@echo "Running MCP test client using stdio transport..."
	cd $(PROJECT_ROOT)/.. && python $(TESTS_DIR)/mcp_client.py --transport stdio --server-path $(PROJECT_ROOT)

# Test using stdio transport with TypeScript client
.PHONY: test-stdio-ts
test-stdio-ts:
	@echo "Running TypeScript MCP test client using stdio transport..."
	cd $(PROJECT_ROOT)/ts-mcp-client && npm run build && node --es-module-specifier-resolution=node dist/client.js --transport stdio --server-path $(PROJECT_ROOT)

# Run with test client in separate pod
.PHONY: run-with-tests
run-with-tests: build
	@echo "Creating Podman pod for MCP server and test client..."
	-podman pod rm -f kai-mcp-pod 2>/dev/null || true
	podman pod create --name kai-mcp-pod -p 8000:8000

	@echo "Creating volume for MCP data..."
	-podman volume rm -f kai-mcp-data 2>/dev/null || true
	podman volume create kai-mcp-data

	@echo "Starting MCP server in the pod..."
	podman run -d --pod kai-mcp-pod \
		--name kai-mcp-server \
		--volume kai-mcp-data:/data:Z \
		$(IMAGE)

	@echo "Waiting for server to start..."
	sleep 5

	@echo "Running MCP test client..."
	cd $(PROJECT_ROOT)/.. && python $(TESTS_DIR)/mcp_client.py --transport http --host localhost --port 8000

	@echo "Cleaning up..."
	podman pod rm -f kai-mcp-pod

# Run pytest integration tests
.PHONY: pytest
pytest:
	@echo "Running MCP integration tests with pytest..."
	cd $(PROJECT_ROOT) && python -m pytest $(TESTS_DIR)/test_integration.py -v

# Help documentation
.PHONY: help
help:
	@echo "Kai MCP Solution Server Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  all            : Build the server"
	@echo "  build          : Build container image with Podman"
	@echo "  push           : Push container image to registry"
	@echo "  deploy         : Deploy to Kubernetes/OpenShift using Ansible"
	@echo "  undeploy       : Remove deployment from Kubernetes/OpenShift"
	@echo "  status         : Check deployment status"
	@echo "  logs           : Show container logs"
	@echo "  clean          : Remove local container images"
	@echo "  port-forward   : Forward port to local machine for testing"
	@echo "  run-local      : Run server locally for testing"
	@echo "  run-podman     : Run server in Podman (uses KAI_DB_DSN)"
	@echo "  podman-postgres: Run server with PostgreSQL via podman-compose"
	@echo "  test-stress    : Run stress test against external server (requires MCP_SERVER_URL)"
	@echo "  test-http      : Test server using HTTP transport (Python client)"
	@echo "  test-http-ts   : Test server using HTTP transport (TypeScript client)"
	@echo "  test-stdio     : Test server using STDIO transport (Python client)"
	@echo "  test-stdio-ts  : Test server using STDIO transport (TypeScript client)"
	@echo "  pytest         : Run pytest integration tests"
	@echo "  run-with-tests : Run server and test client together"
	@echo "  help           : Show this help message"
	@echo ""
	@echo "Configuration options (can be set via environment or command line):"
	@echo "  IMAGE          : Container image (default: quay.io/konveyor/kai-mcp-solution-server:latest)"
	@echo "  NAMESPACE      : Kubernetes namespace (default: konveyor-kai)"
	@echo "  HOST           : Server hostname for HTTP tests (default: localhost)"
	@echo "  PORT           : Server port for HTTP tests (default: 8000)"
	@echo "  BEARER_TOKEN   : Bearer token for HTTP authentication (optional)"
	@echo "  KAI_DB_DSN     : Database connection string for server"
	@echo "  KAI_LLM_PARAMS : LLM configuration as JSON (required)"
	@echo "  NUM_CONCURRENT_CLIENTS : Number of clients for stress testing (default: 30)"
	@echo "  MCP_SERVER_URL : URL of external server for test-stress-external (default: http://localhost:8000)"
	@echo "  EXTRA_VARS     : Any additional variables to pass to Ansible"
	@echo ""
	@echo "Example usage:"
	@echo "  make build IMAGE=quay.io/konveyor/kai-mcp-solution-server:v1.0.0"
	@echo "  make deploy NAMESPACE=my-namespace"
	@echo "  make deploy IMAGE=quay.io/konveyor/kai-mcp-solution-server:v1.0.0"
	@echo "  make deploy EXTRA_VARS='storage_class=gp2 storage_size=5Gi'"
	@echo "  make deploy EXTRA_VARS='route_tls_enabled=false'"
	@echo "  make deploy EXTRA_VARS='route_tls_enabled=true route_tls_termination=edge route_tls_insecure_policy=Allow'"
	@echo "  make run-local"
	@echo "  make test-stdio"
	@echo "  KAI_LLM_PARAMS='{\"model\":\"gpt-4\"}' make podman-postgres"
	@echo "  # Stress test against running server:"
	@echo "  make run-local  # In one terminal"
	@echo "  MCP_SERVER_URL=http://localhost:8000 NUM_CONCURRENT_CLIENTS=100 make test-stress  # In another"
	@echo "  make test-http"
	@echo "  make test-http BEARER_TOKEN='your-jwt-token-here'"
	@echo "  make test-http HOST=api.exayeah, there are a lot of little ones that have been filed. I feel pretty comfortable delaying them to a point releasemple.com PORT=443 BEARER_TOKEN='token'"
	
