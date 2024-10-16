# trunk-ignore-begin(ruff/E402)
import sys

sys.modules["_elementtree"] = None  # type: ignore[assignment]

import os
import xml.etree.ElementTree as ET  # trunk-ignore(bandit/B405)
from pathlib import Path
from typing import Callable, Optional

import requests

from kai.repo_level_awareness.agent.dependency_agent.api import (
    FindInPomResponse,
    FQDNResponse,
)
from kai.repo_level_awareness.utils.xml import LineNumberingParser

# trunk-ignore-end(ruff/E402)


def search_fqdn_query(query: str) -> Optional[FQDNResponse] | list[FQDNResponse]:
    resp = requests.get(
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
            all_found_deps.append(
                FQDNResponse(
                    artifact_id=d["a"], group_id=d["g"], version=d["latestVersion"]
                )
            )
        return all_found_deps
    else:
        doc = docs[0]
        return FQDNResponse(
            artifact_id=doc["a"], group_id=doc["g"], version=doc["latestVersion"]
        )


def search_fqdn(code: str) -> Optional[FQDNResponse] | list[FQDNResponse]:
    query = get_maven_query_from_code(code)
    return search_fqdn_query(query)


def get_maven_query(**kwargs) -> str:
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


def find_in_pom(path: Path) -> Callable:
    ## Open XML file
    ## parse XML, find the dependency node if we have group and artifact we will return start_line and end_line for the full node
    ## If we don't have group and artifact, but we have dependencies, then we will find the start of the dependecies node. start_line and end_line will be the same. The start of the dependencies.
    tagToKwargs = {
        "{http://maven.apache.org/POM/4.0.0}artifactId": "artifactId",
        "{http://maven.apache.org/POM/4.0.0}groupId": "groupId",
    }

    def f(code: str) -> FindInPomResponse:
        tree = ET.parse(  # trunk-ignore(bandit/B314)
            os.path.join(path, "pom.xml"), parser=LineNumberingParser()
        )
        root = tree.getroot()
        dependencies = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
        deps = root.findall("*//{http://maven.apache.org/POM/4.0.0}dependency")
        index = code.index("keywords")
        # Remove 8 chars to get ride of keyword=
        code_string = code[index + 9 :].strip("(){}")
        ## We know when it is just an add operation, that the LLM gives us just the word dependencies
        if "dependencies" in code_string:
            return FindInPomResponse(
                dependencies._start_line_number, dependencies._start_line_number
            )

        parts = code_string.split(",")
        kwargs = {}
        for p in parts:
            arg = p.split(":")
            kwargs[arg[0].strip(' ""')] = (  # trunk-ignore(ruff/B005)
                arg[1].strip(' ""').strip()  # trunk-ignore(ruff/B005)
            )

        for dep in deps:
            found = []
            for child in dep:
                key = tagToKwargs.get(child.tag)
                if not key:
                    continue
                value = kwargs[key]
                if child.text == value:
                    found.append(True)
            if len(found) == 2:
                return FindInPomResponse(dep._start_line_number, dep._end_line_number)
        return FindInPomResponse(
            dependencies._start_line_number, dependencies._start_line_number
        )

    return f
