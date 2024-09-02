#!/bin/bash

printf "Waiting until postgres is ready\n"
# trunk-ignore(shellcheck/SC2312)
until [[ $(PGPASSWORD="${KAI__INCIDENT_STORE__ARGS__PASSWORD}" pg_isready -q -h "${KAI__INCIDENT_STORE__ARGS__HOST}" -U "${KAI__INCIDENT_STORE__ARGS__USER}" -d "${KAI__INCIDENT_STORE__ARGS__DATABASE}") -eq 0 ]]; do
	printf "."
	sleep 1
done

printf "\nPostgres is ready\n"

if [[ ${MODE} != "importer" ]]; then
	if [[ ${USE_HUB_IMPORTER:-False} == "False" ]]; then
		TABLE=applications
		SQL_EXISTS=$(printf "\dt %s" "${TABLE}")
		STDERR="Did not find any relation"
		# trunk-ignore(shellcheck/SC2312)
		if PGPASSWORD="${KAI__INCIDENT_STORE__ARGS__PASSWORD}" psql -h "${KAI__INCIDENT_STORE__ARGS__HOST}" -U "${KAI__INCIDENT_STORE__ARGS__USER}" -d "${KAI__INCIDENT_STORE__ARGS__DATABASE}" -c "${SQL_EXISTS}" 2>&1 | grep -q -v "${STDERR}"; then
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

			if [[ -f /podman_compose/build/config.toml ]]; then
				printf "Using custom config file\n"
				python ./kai/service/incident_store/incident_store.py --config_filepath /podman_compose/build/config.toml --drop_tables False
			else
				python ./kai/service/incident_store/incident_store.py --drop_tables False
			fi
			echo "################################################"
			echo "load-data has completed, starting server.      #"
			echo "################################################"
			sleep 5
		fi
	fi

	printf "Starting Kai server\n"
	if [[ -f /podman_compose/build/config.toml ]]; then
		printf "Using custom config file\n"
		PYTHONPATH="/kai/kai" python /kai/kai/server.py --config_filepath /podman_compose/build/config.toml
	else
		PYTHONPATH="/kai/kai" python /kai/kai/server.py
	fi

else
	cd /kai || exit
	python ./kai/hub_importer.py --loglevel "${KAI__LOG_LEVEL}" "${CUSTOM_CONFIG_FLAG}" "${KAI__HUB_URL}" "${KAI__IMPORTER_ARGS}"
fi
