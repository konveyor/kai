#!/bin/bash

# If a custom config is specified, use it
if [[ -f /podman_compose/build/config.toml ]]; then
	printf "Using custom config.toml\n"
	cp /podman_compose/build/config.toml /kai/kai/config.toml
fi

until PGPASSWORD="${KAI__INCIDENT_STORE__ARGS__PASSWORD}" pg_isready -q -h "${KAI__INCIDENT_STORE__ARGS__HOST}" -U "${KAI__INCIDENT_STORE__ARGS__USER}" -d "${KAI__INCIDENT_STORE__ARGS__DATABASE}"; do
	sleep 1
done

if [[ ${MODE} != "importer" ]]; then
	if [[ ${USE_HUB_IMPORTER} == "False" ]]; then
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
			python ./kai/service/incident_store/psql.py --config_filepath ./kai/config.toml --drop_tables False
			echo "################################################"
			echo "load-data has completed, starting server.      #"
			echo "################################################"
			sleep 5
		fi
	fi
	PYTHONPATH="/kai/kai" python /kai/kai/server.py
else
	cd /kai || exit
	python ./kai/hub_importer.py --loglevel "${KAI__LOG_LEVEL}" --config_filepath ./kai/config.toml "${KAI__HUB_URL}" "${KAI__IMPORTER_ARGS}"
fi
