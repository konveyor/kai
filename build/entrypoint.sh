#!/bin/bash

# If we are using podman or docker compose use the repo config.toml
if [[ -f /podman_compose/kai/config.toml ]]; then
	cp /podman_compose/kai/config.toml /kai/kai/config.toml
	sed -i 's/^host\ =.*/host = "kai_db"/g' /kai/kai/config.toml
	sed -i "s/^database =.*/database = \"${POSTGRES_DB}\"/g" /kai/kai/config.toml
	sed -i "s/^user =.*/user = \"${POSTGRES_USER}\"/g" /kai/kai/config.toml
	sed -i "s/^password =.*/password =\"${POSTGRES_PASSWORD}\"/g" /kai/kai/config.toml
fi

until PGPASSWORD="${POSTGRES_PASSWORD}" pg_isready -q -h kai_db -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
	sleep 1
done

if [[ ${MODE} != "importer" ]]; then
	if [[ ${USE_HUB_IMPORTER} == "False" ]]; then
		TABLE=applications
		SQL_EXISTS=$(printf "\dt %s" "${TABLE}")
		STDERR="Did not find any relation"
		# trunk-ignore(shellcheck/SC2312)
		if PGPASSWORD="${POSTGRES_PASSWORD}" psql -h kai_db -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "${SQL_EXISTS}" 2>&1 | grep -q -v "${STDERR}"; then
			echo "################################################"
			echo "load-data has run already run, starting server.#"
			echo "################################################"
		else
			echo "################################################"
			echo "load-data has never been run.                  #"
			echo "Please wait, this will take a few minutes.     #"
			echo "################################################"
			sleep 5
			cd /kai || exit
			python ./kai/service/incident_store/psql.py --config_filepath ./kai/config.toml --drop_tables False
			echo "################################################"
			echo "load-data has completed, starting server.      #"
			echo "################################################"
			sleep 5
		fi
	fi
	PYTHONPATH="/kai/kai" exec gunicorn --timeout 3600 -w "${NUM_WORKERS}" --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker 'kai.server:app()'
else
	cd /kai || exit
	python ./kai/hub_importer.py --loglevel "${LOGLEVEL}" --config_filepath ./kai/config.toml "${IMPORTER_ARGS}" "${HUB_URL}"
fi
