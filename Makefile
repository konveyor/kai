CONTAINER_RUNTIME = podman

CWD := $(shell pwd)
POSTGRES_RUN_ARGS ?=

.PHONY: help test typecheck lint fmt run-postgres build-kai-analyzer get-analyzer-deps get-rulesets

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-20s %s\n", $$1, $$2}'

test: ## Run MCP solution server tests
	cd kai_mcp_solution_server && ./run_tests.sh

typecheck: ## Run mypy type checking on MCP solution server
	cd kai_mcp_solution_server && ./run_mypy.sh

lint: ## Run trunk linter checks
	trunk check

fmt: ## Format code with trunk
	trunk fmt

run-postgres: ## Start a local PostgreSQL container for development
	$(CONTAINER_RUNTIME) run -it $(POSTGRES_RUN_ARGS) -v data:/var/lib/postgresql/data -e POSTGRES_USER=kai -e POSTGRES_PASSWORD=dog8code -e POSTGRES_DB=kai -p 5432:5432 docker.io/library/postgres:16.3

build-kai-analyzer: ## Build the kai-analyzer-rpc binary
	cd kai_analyzer_rpc && go build -o kai-analyzer main.go

get-analyzer-deps: ## Download Java analysis dependencies
	${CONTAINER_RUNTIME} run -d --name=bundle quay.io/konveyor/jdtls-server-base:latest &&\
    ${CONTAINER_RUNTIME} cp bundle:/usr/local/etc/maven.default.index ./example/analysis &&\
    ${CONTAINER_RUNTIME} cp bundle:/jdtls ./example/analysis &&\
    ${CONTAINER_RUNTIME} cp bundle:/jdtls/java-analyzer-bundle/java-analyzer-bundle.core/target/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar ./example/analysis/bundle.jar &&\
	${CONTAINER_RUNTIME} stop bundle &&\
	${CONTAINER_RUNTIME} rm bundle

get-rulesets: ## Download rulesets for the analyzer
	(cd example/analysis && rm -rf rulesets && git clone --depth 1 --branch v0.6.0 https://github.com/konveyor/rulesets); rm -rf example/analysis/rulesets/preview
