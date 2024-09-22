CONTAINER_RUNTIME = podman

CWD := $(shell pwd)
KAI_PYTHON_PATH="$(CWD)/kai:$(PYTHONPATH)"
LOGLEVEL ?= info
NUM_WORKERS ?= 8
KAI__DEMO_MODE ?= False
DROP_TABLES ?= False
HUB_URL ?= ""
IMPORTER_ARGS ?= ""
POSTGRES_RUN_ARGS ?= 

run-postgres:
	$(CONTAINER_RUNTIME) run -it $(POSTGRES_RUN_ARGS) -v data:/var/lib/postgresql/data -e POSTGRES_USER=kai -e POSTGRES_PASSWORD=dog8code -e POSTGRES_DB=kai -p 5432:5432 docker.io/library/postgres:16.3

# ## Note: MacOS workaround is required, see https://github.com/konveyor/kai/issues/374
run-server:
	bash -c 'set -m; _trap () { kill -15 $$PID; } ; trap _trap SIGINT ;\
	if [[ "$$(uname)" -eq "Darwin" ]] ; then export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES ; fi ;\
	PYTHONPATH=$(KAI_PYTHON_PATH) python kai/server.py & export PID=$$! ;\
	while kill -0 $$PID > /dev/null 2>&1; do wait $$PID; done'

run-konveyor-importer:
	PYTHONPATH=$(KAI_PYTHON_PATH) python kai/hub_importer.py --loglevel ${LOGLEVEL} --config_filepath ./kai/config.toml ${IMPORTER_ARGS} ${HUB_URL}

load-data:
	PYTHONPATH=$(KAI_PYTHON_PATH) python kai/service/incident_store/incident_store.py  --config_filepath ./kai/config.toml --drop_tables $(DROP_TABLES)
