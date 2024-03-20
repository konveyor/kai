CONTAINER_RUNTIME = podman

CWD := $(shell pwd)
KAI_PYTHON_PATH="$(CWD)/kai:$(PYTHONPATH)"

run-postgres:
	$(CONTAINER_RUNTIME) run -it -v data:/var/lib/postgresql/data -e POSTGRES_USER=kai -e POSTGRES_PASSWORD=dog8code -e POSTGRES_DB=kai -p 5432:5432 docker.io/pgvector/pgvector:pg15

run-server:
	PYTHONPATH=$(KAI_PYTHON_PATH) python ./kai/server.py

load-data:
	PYTHONPATH=$(KAI_PYTHON_PATH) python ./kai/incident_store_advanced.py --config_filepath ./kai/database.ini
