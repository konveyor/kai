# Makefile for Kai MCP Solution Server

# Configuration
IMAGE_NAME ?= quay.io/konveyor/kai-mcp-solution-server
IMAGE_TAG ?= latest
CONTEXT ?= $(shell kubectl config current-context)

# Directories
PROJECT_ROOT = $(shell pwd)
BUILD_DIR = $(PROJECT_ROOT)/deploy
SCRIPTS_DIR = $(PROJECT_ROOT)/scripts

# Default target
.PHONY: all
all: build

# Build the container image with Podman
.PHONY: build
build:
	@echo "Building container image $(IMAGE_NAME):$(IMAGE_TAG) with Podman..."
	podman build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(BUILD_DIR)/Containerfile $(PROJECT_ROOT)/..

# Push the container image to the registry
.PHONY: push
push:
	@echo "Pushing container image $(IMAGE_NAME):$(IMAGE_TAG)..."
	podman push $(IMAGE_NAME):$(IMAGE_TAG)

# Clean up local resources
.PHONY: clean
clean:
	@echo "Cleaning local resources..."
	-podman rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true

# Run locally for testing
.PHONY: run-local
run-local:
	@echo "Running MCP solution server locally..."
	cd $(PROJECT_ROOT) && python -m main --transport sse --host 0.0.0.0 --port 8000 --log-level info

# Run with Podman for testing
.PHONY: run-podman
run-podman: build
	@echo "Running MCP solution server in Podman..."
	podman run --rm -it -p 8000:8000 --name kai-mcp-solution-server $(IMAGE_NAME):$(IMAGE_TAG)

# Test against HTTP server
.PHONY: test-http
test-http:
	@echo "Running MCP test client against HTTP server..."
	@echo "Make sure the server is running with 'make run-local' or 'make run-podman'"
	cd $(PROJECT_ROOT)/.. && python $(SCRIPTS_DIR)/test_client.py --transport http --host localhost --port 8000

# Test using stdio transport
.PHONY: test-stdio
test-stdio:
	@echo "Running MCP test client using stdio transport..."
	cd $(PROJECT_ROOT)/.. && python $(SCRIPTS_DIR)/test_client.py --transport stdio --server-path $(PROJECT_ROOT)
