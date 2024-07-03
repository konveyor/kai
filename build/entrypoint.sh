#!/bin/bash

# If we are using compose.yml use the repo config.toml
if [ -f /podman_compose/kai/config.toml ]; then
	cp /podman_compose/kai/config.toml /kai/kai/config.toml
	sed -i 's/^host\ =.*/host = "kai_db"/g' /kai/kai/config.toml
	sed -i "s/^database =.*/database = \"$POSTGRES_DB\"/g" /kai/kai/config.toml
	sed -i "s/^user =.*/user = \"$POSTGRES_USER\"/g" /kai/kai/config.toml
	sed -i "s/^password =.*/password =\"$POSTGRES_PASSWORD\"/g" /kai/kai/config.toml
fi

# Wait for the database to be ready
export POSTGRES_HOST=${POSTGRES_HOST:=kai_db}
export POSTGRES_PORT=${POSTGRES_PORT:=5432}
if [[ -n ${POSTGRES_HOST} ]] && [[ -n ${POSTGRES_PORT} ]]; then
	/usr/local/bin/wait-for-it.sh "${POSTGRES_HOST}:${POSTGRES_PORT}" --strict --timeout=300
fi

TABLE=applications
SQL_EXISTS=$(printf '\dt "%s"' "$TABLE")
if [[ $(PGPASSWORD="$POSTGRES_PASSWORD" psql -h "kai_db" -U $POSTGRES_USER -d $POSTGRES_DB -c "$SQL_EXISTS") ]]; then
	echo "load-data has run already"
else
	echo "load-data has not run yet, starting ..."
	echo "Fetching examples"
	cd /kai/samples
	./fetch_apps.py
	cd /kai
	# Quieting logging from loading data to only errors
	LOGLEVEL=error python ./kai/service/incident_store/psql.py --config_filepath ./kai/config.toml --drop_tables False
fi

PYTHONPATH="/kai/kai" exec gunicorn --timeout 3600 -w $NUM_WORKERS --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker 'kai.server:app()'
