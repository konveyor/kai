#/usr/bin/sh
#

export PYTHONPATH="$(pwd)/kai:${PYTHONPATH}" # trunk-ignore(shellcheck)
python -m unittest -v

##
# Example to run tests in a single test class:
# python -m unittest -v tests.test_incident_store_advanced.TestIncidentStoreAdvanced
# Example to run a single test:
# python -m unittest -v tests.test_incident_store.TestIncidentStore.test_find_solved_issues
