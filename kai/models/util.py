# These prefixes are sometimes in front of the paths, strip them.
# Also strip leading slashes since os.path.join can't join two absolute paths
KNOWN_PREFIXES = (
    "/opt/input/source/",
    # trunk-ignore(bandit/B108)
    "/tmp/source-code/",
    "/addon/source/",
    "/",
)


# These are known unique variables that can be included by incidents
# They would prevent matches that we actually want, so we filter them
# before adding to the database or searching
FILTERED_INCIDENT_VARS = ("file", "package")


def remove_known_prefixes(path: str) -> str:
    for prefix in KNOWN_PREFIXES:
        if path.startswith(prefix):
            return path.removeprefix(prefix)
    return path


def filter_incident_vars(incident_vars: dict):
    for v in FILTERED_INCIDENT_VARS:
        incident_vars.pop(v, None)
    return incident_vars
