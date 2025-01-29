import os
from pathlib import Path
from typing import Any, Callable, Optional

import requests
from lxml import etree  # trunk-ignore(bandit/B410)

from kai.reactive_codeplanner.agent.dependency_agent.api import (
    FindInPomResponse,
    FQDNResponse,
)


def search_fqdn_query(query: str) -> Optional[FQDNResponse] | list[FQDNResponse]:
    # Not trusting the session, because proxy/ssl configuration
    # From the session is meant for the LLM.
    session = requests.Session()
    session.trust_env = False
    resp = session.get(
        f"https://search.maven.org/solrsearch/select?q={query}", timeout=10
    )
    if resp.status_code != 200:
        return None
    output = resp.json()
    docs = output["response"]["docs"]
    if not docs:
        return None
    if len(docs) > 1:
        ### Here, I think we need to have a specific return, that then asks the LLM to chose which one based on the
        ### context.
        all_found_deps = []
        for d in docs:
            if "latestVersion" in d:
                all_found_deps.append(
                    FQDNResponse(
                        artifact_id=d["a"], group_id=d["g"], version=d["latestVersion"]
                    )
                )
        return all_found_deps if all_found_deps else None
    else:
        doc = docs[0]

        if "latestVersion" in doc:

            return FQDNResponse(
                artifact_id=doc["a"], group_id=doc["g"], version=doc["latestVersion"]
            )

        return None


def search_fqdn(code: str) -> Optional[FQDNResponse] | list[FQDNResponse]:
    query = get_maven_query_from_code(code)
    return search_fqdn_query(query)


def get_maven_query(**kwargs: Any) -> str:
    query = []
    if "artifact_id" in kwargs:
        query.append("a:" + kwargs["artifact_id"])
    if "group_id" in kwargs:
        query.append("g:" + kwargs["group_id"])
    if "version" in kwargs:
        query.append("v:" + kwargs["version"])
    return " AND ".join(query)
    # fmt: on


def get_maven_query_from_code(code: str) -> str:
    # We need to remove the function call information from the code.
    start_i = code.index("(")
    end_i = code.index(")")

    # Need to remove the not needed chars, whitespace and '"' and ()
    args = code[start_i:end_i].strip()

    parts = args.split(",")
    kwargs = {}

    for p in parts:
        arg = p.split("=")
        kwargs[arg[0].strip().strip('""()')] = (  # trunk-ignore(ruff/B005)
            arg[1].strip().strip('""')  # trunk-ignore(ruff/B005)
        )
    return get_maven_query(**kwargs)


def find_in_pom(path: Path) -> Callable[[str], FindInPomResponse]:
    ## Open XML file
    ## parse XML, find the dependency node if we have group and artifact we will return start_line and end_line for the full node
    ## If we don't have group and artifact, but we have dependencies, then we will find the start of the dependecies node. start_line and end_line will be the same. The start of the dependencies.
    tag_to_kwargs = {
        "{http://maven.apache.org/POM/4.0.0}artifactId": "artifactId",
        "{http://maven.apache.org/POM/4.0.0}groupId": "groupId",
        "{http://maven.apache.org/POM/4.0.0}version": "version",
    }

    def f(code: str) -> FindInPomResponse:
        tree = etree.parse(os.path.join(path, "pom.xml"))  # trunk-ignore(bandit/B320)
        root = tree.getroot()
        deps = root.findall("*//{http://maven.apache.org/POM/4.0.0}dependency")
        index = code.index("keywords")
        # Remove 8 chars to get ride of keyword=
        code_string = code[index + 9 :].strip("(){}")
        ## We know when it is just an add operation, that the LLM gives us just the word dependencies
        if "dependencies" in code_string:
            return FindInPomResponse(override=False)

        parts = code_string.split(",")
        kwargs = {}
        for p in parts:
            arg = p.split(":")
            if len(arg) != 2:
                return FindInPomResponse(override=False)
            kwargs[arg[0].strip(' ""')] = (  # trunk-ignore(ruff/B005)
                arg[1].strip(' ""').strip()  # trunk-ignore(ruff/B005)
            )

        for dep in deps:
            found = []
            dep_dic: dict[str, str] = {}
            for child in dep:
                key = tag_to_kwargs.get(child.tag)
                if not key:
                    continue
                if isinstance(child.text, str):
                    dep_dic[key] = child.text

            for name, value in kwargs.items():
                if name in dep_dic and dep_dic[name] == value:
                    found.append(True)
            if len(found) == 2:
                return FindInPomResponse(
                    override=True,
                    artifact_id=dep_dic.get("artifactId"),
                    group_id=dep_dic.get("groupId"),
                    version=dep_dic.get("version"),
                )
        return FindInPomResponse(override=False)

    return f
