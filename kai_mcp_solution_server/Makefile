# Makefile for Kai MCP Solution Server

# Configuration
IMAGE ?= quay.io/konveyor/kai-mcp-solution-server:latest
NAMESPACE ?= konveyor-kai-solution-server

# Directories
PROJECT_ROOT = $(shell pwd)
BUILD_DIR = $(PROJECT_ROOT)/deploy
SCRIPTS_DIR = $(PROJECT_ROOT)/scripts

HOST ?= localhost
PORT ?= 8000

# Default target
.PHONY: all
all: build

# Build the container image with Podman
.PHONY: build
build:
	@echo "Building container image $(IMAGE) with Podman..."
	podman build -t $(IMAGE) -f $(BUILD_DIR)/Containerfile $(PROJECT_ROOT)/..

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
	cd $(PROJECT_ROOT) && python -m main --transport sse --host 0.0.0.0 --port 8000 --log-level info

# Run with Podman for testing
.PHONY: run-podman
run-podman: build
	@echo "Running MCP solution server in Podman..."
	podman run --rm -it -p 8000:8000 --name kai-mcp-solution-server $(IMAGE)

# Test against HTTP server
.PHONY: test-http
test-http:
	@echo "Running MCP test client against HTTP server..."
	@echo "Make sure the server is running with 'make run-local' or 'make run-podman'"
	cd $(PROJECT_ROOT)/.. && python $(SCRIPTS_DIR)/test_client.py --transport http --host $(HOST) --port $(PORT)

# Test using stdio transport
.PHONY: test-stdio
test-stdio:
	@echo "Running MCP test client using stdio transport..."
	cd $(PROJECT_ROOT)/.. && python $(SCRIPTS_DIR)/test_client.py --transport stdio --server-path $(PROJECT_ROOT)

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
	cd $(PROJECT_ROOT)/.. && python $(SCRIPTS_DIR)/test_client.py --transport http --host localhost --port 8000

	@echo "Cleaning up..."
	podman pod rm -f kai-mcp-pod

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
	@echo "  run-podman     : Run server in Podman container for testing"
	@echo "  test-http      : Test server using HTTP transport"
	@echo "  test-stdio     : Test server using STDIO transport"
	@echo "  run-with-tests : Run server and test client together"
	@echo "  help           : Show this help message"
	@echo ""
	@echo "Configuration options (can be set via environment or command line):"
	@echo "  IMAGE          : Container image (default: quay.io/konveyor/kai-mcp-solution-server:latest)"
	@echo "  NAMESPACE      : Kubernetes namespace (default: konveyor-kai)"
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
