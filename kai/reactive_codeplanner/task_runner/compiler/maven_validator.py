#!/usr/bin/env python

import re
import subprocess  # trunk-ignore(bandit/B404)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from shutil import which
from typing import Optional, Type

from opentelemetry import trace

from kai.constants import ENV
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.task_manager.api import (
    RpcClientConfig,
    Task,
    ValidationError,
    ValidationResult,
    ValidationStep,
)

logger = get_logger(__name__)

tracer = trace.get_tracer("maven_validator")

BUILD_ERROR_PATTERN = re.compile(
    r"\s*\[(ERROR|FATAL)\]\s*(.+?) @ line (\d+), column (\d+)"
)


class MavenCompileStep(ValidationStep):

    def __init__(self, config: RpcClientConfig) -> None:
        super().__init__(config)
        self.last_compilation_errors: list[MavenCompilerError] = []

    @tracer.start_as_current_span("maven_run_validator")
    def run(self, scoped_paths: Optional[list[Path]] = None) -> ValidationResult:
        rc, maven_output, pom_file_path = run_maven(self.config.repo_directory)
        build_errors, dependency_errors, compilation_errors, catchall_errors = (
            parse_maven_output(maven_output, rc, str(pom_file_path))
        )
        # Build/dependency/other errors prevent the compilation errors from being reported
        # But we still want to return them so they aren't mistakenly marked as solved.
        logger.debug(
            f"determining whether maven cache should be set: build_errors: {bool(build_errors)}, dependency_errors: {bool(dependency_errors)}, catchall_errors: {bool(catchall_errors)}, compilation_errors: {bool(compilation_errors)}, cond: {(build_errors or dependency_errors or catchall_errors) and not compilation_errors}"
        )
        if (
            build_errors or dependency_errors or catchall_errors
        ) and not compilation_errors:
            compilation_errors = self.last_compilation_errors
            logger.info(
                f"Returning {len(self.last_compilation_errors)} cached compilation errors until the POM is valid"
            )
        else:
            self.last_compilation_errors = compilation_errors
            logger.debug(
                f"Setting the maven cache with {len(self.last_compilation_errors)} compilation errors"
            )
        errors = build_errors + dependency_errors + compilation_errors + catchall_errors
        return ValidationResult(passed=not errors, errors=errors)


@dataclass(eq=False)
class MavenCompilerError(ValidationError):
    details: list[str] = field(default_factory=list)
    parse_lines: Optional[str] = None
    priority = 1

    @classmethod
    def from_match(
        cls, match: re.Match[str], details: list[str]
    ) -> "MavenCompilerError":
        """
        Factory method to create an instance from a regex match.
        """
        file_path = match.group(1).strip()
        line_number = int(match.group(2)) if match.group(2) else -1
        column_number = int(match.group(3)) if match.group(3) else -1
        message = match.group(4).strip()
        return cls(
            file=file_path,
            line=line_number,
            column=column_number,
            message=message,
            details=details.copy(),
        )

    def compiler_error_message(self) -> str:
        return self.message


class CollapsedMavenCompilerError(ABC, MavenCompilerError):
    lines: list[int] | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if not super().__eq__(other):
            return False
        if self.error_lines and other.error_lines:
            return self.error_lines == other.error_lines
        return False

    def __hash__(self) -> int:
        if self.error_lines:
            return hash((super().__hash__(), tuple(self.error_lines)))
        return super().__hash__()

    def fuzzy_equals(self, error2: Task, offset: int = 1) -> bool:
        if not isinstance(error2, self.__class__):
            return False
        if not super().__eq__(error2):
            return False
        # if both errors don't have error lines and super()
        # is equal, then these must be equal
        if not self.error_lines and not error2.error_lines:
            return True
        if not self.error_lines or not error2.error_lines:
            return False
        matching_lines: list[int] = []
        for line in self.error_lines:
            for error2_line in error2.error_lines:
                if line == error2_line:
                    matching_lines.append(line)

        # All the errors from this are still in the error, this makes them equal
        if len(matching_lines) == len(self.error_lines):
            return True

        # we didn't find any matches, so error2 is a wholly new set of issues
        if len(matching_lines) == 0:
            return False

        # Now, we have some errors that have not be resolved and some that have, We will continue to process this task
        # in the future we should have a way of creating a new task, with the same priority as this one
        # that makes it so we take all the problems
        return True

    @cached_property
    def error_lines(self) -> list[int] | None:
        if self.lines:
            self.lines.sort()
        return self.lines

    @abstractmethod
    def get_collapsable_key(self) -> str:
        pass


# Subclasses for specific error categories
@dataclass(eq=False)
class BuildError(MavenCompilerError):
    priority: int = 1


@dataclass(eq=False)
class DependencyResolutionError(MavenCompilerError):
    priority: int = 1
    project: str = ""
    goal: str = ""

    def compiler_error_message(self) -> str:
        return self.message


@dataclass(eq=False)
class SymbolNotFoundError(CollapsedMavenCompilerError):
    missing_symbol: Optional[str] = None
    symbol_location: Optional[str] = None
    priority: int = 2

    def compiler_error_message(self) -> str:
        if self.missing_symbol and self.symbol_location:
            return f"{self.message}: {self.missing_symbol} at {self.symbol_location}"
        if self.missing_symbol:
            return f"{self.message}: {self.missing_symbol}"
        return self.message

    def get_collapsable_key(self) -> str:
        return f"{self.file}-{self.__class__}-{self.missing_symbol}"


@dataclass(eq=False)
class PackageDoesNotExistError(CollapsedMavenCompilerError):
    priority: int = 1
    missing_package: Optional[str] = None

    def compiler_error_message(self) -> str:
        if self.missing_package:
            return f"{self.message}: {self.missing_package}"
        else:
            return self.message

    # This does not have to be for file, because the package not existing is at the project level
    def get_collapsable_key(self) -> str:
        return f"{self.__class__}-{self.missing_package}"


@dataclass(eq=False)
class SyntaxError(MavenCompilerError):
    priority: int = 2


@dataclass(eq=False)
class TypeMismatchError(MavenCompilerError):
    expected_type: Optional[str] = None
    found_type: Optional[str] = None

    def compiler_error_message(self) -> str:
        if self.expected_type and self.found_type:
            return f"{self.message}\nexpected type: {self.expected_type}\nfound type: {self.found_type}"
        else:
            return self.message


@dataclass(eq=False)
class AnnotationError(MavenCompilerError):
    pass


@dataclass(eq=False)
class AccessControlError(MavenCompilerError):
    inaccessible_class: Optional[str] = None


@dataclass(eq=False)
class OtherError(MavenCompilerError):
    priority: int = 6


def run_maven(source_directory: Path = Path(".")) -> tuple[int, str, Optional[Path]]:
    """
    Runs 'mvn compile' and returns the combined stdout and stderr output.
    Also returns the path to the pom.xml file.
    """
    mavenPath = which("mvn") or "mvn"
    cmd = [mavenPath, "clean", "compile"]
    #  trunk-ignore-begin(bandit/B603)
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            cwd=source_directory,
            env=ENV,
        )
        pom_file_path = source_directory / "pom.xml"
        logger.log(TRACE, "running maven process: %s", process)
        return (process.returncode, process.stdout, pom_file_path)
    #  trunk-ignore-end(bandit/B603)
    except FileNotFoundError:
        logger.info("Maven is not installed or not found in the system PATH.")
        return -1, "", None


def classify_error(message: str) -> Type[MavenCompilerError]:
    """
    Classifies an error message and returns the corresponding error class.
    """
    message_lower = message.lower()
    if "cannot find symbol" in message_lower:
        return SymbolNotFoundError
    elif message_lower.startswith("package ") and message_lower.endswith(
        " does not exist"
    ):
        return PackageDoesNotExistError
    elif "class, interface, or enum expected" in message_lower:
        return SyntaxError
    elif "incompatible types" in message_lower:
        return TypeMismatchError
    elif (
        "method does not override or implement a method from a supertype"
        in message_lower
    ):
        return AnnotationError
    elif "cannot access" in message_lower:
        return AccessControlError
    else:
        return OtherError


def parse_maven_output(
    output: str, rc: int, pom_file_path: Optional[str] = None
) -> tuple[
    list[MavenCompilerError],
    list[MavenCompilerError],
    list[MavenCompilerError],
    list[OtherError],
]:
    """
    Parses the Maven output and returns a list of MavenCompilerError instances.
    """
    lines = output.splitlines()
    i = 0
    build_errors = []
    dependency_errors = []
    compilation_errors = []
    catchall_errors = []
    while i < len(lines):
        line = lines[i]
        if "[ERROR] Some problems were encountered while processing the POMs:" in line:
            i, new_build_errors = parse_build_errors(lines, i + 1, pom_file_path)
            build_errors.extend(new_build_errors)
            continue
        elif "[ERROR] COMPILATION ERROR :" in line:
            i, new_compilation_errors = parse_compilation_errors(lines, i)
            compilation_errors.extend(new_compilation_errors)
            continue
        elif "[ERROR] Failed to execute goal" in line:
            error, new_index = parse_dependency_resolution_error(
                lines, i, pom_file_path
            )
            if error:
                dependency_errors.append(error)
                i = new_index
                continue
            else:
                i += 1
        else:
            i += 1
    if rc != 0 and not any([build_errors, dependency_errors, compilation_errors]):
        catchall_error = catchall(output)
        if catchall_error:
            catchall_errors.append(catchall_error)

    return (
        deduplicate_errors(build_errors),
        deduplicate_errors(dependency_errors),
        deduplicate_errors(compilation_errors),
        catchall_errors,
    )


def parse_build_errors(
    lines: list[str], start_index: int, pom_file_path: Optional[str]
) -> tuple[int, list[MavenCompilerError]]:
    """
    Parses the build error section and returns a list of BuildError instances.
    """
    errors = []
    i = start_index
    file_path = pom_file_path or "pom.xml"
    matched_project = False

    while i < len(lines):
        line = lines[i]
        if is_section_end(line):
            break

        # Match project line to get file path
        project_match = re.match(
            r"\[ERROR\]\s+The project\s*(?:.+?)?\s*\((.+pom\.xml)\) has \d+ error", line
        )
        if project_match:
            file_path = project_match.group(1).strip()
            matched_project = True
            i += 1
            continue

        if matched_project:
            # Only parse build errors after matching a project line
            build_error = match_build_error(line, file_path)
            if build_error:
                error = build_error
                # Collect details if any
                details = []
                i += 1
                while (
                    i < len(lines)
                    and lines[i].startswith("[ERROR]     ")
                    and not BUILD_ERROR_PATTERN.match(lines[i])
                ):
                    detail_line = lines[i].replace("[ERROR]     ", "", 1).strip()
                    details.append(detail_line)
                    i += 1
                error.details.extend(details)
                errors.append(error)
                continue
            else:
                i += 1
        else:
            # Skip lines until we match a project line
            i += 1

    return i, errors


def parse_dependency_resolution_error(
    lines: list[str], index: int, pom_file_path: Optional[str]
) -> tuple[Optional[MavenCompilerError], int]:
    """
    Parses a dependency resolution error starting from the given index.
    """
    line = lines[index]
    pattern = re.compile(
        r"\[ERROR\] Failed to execute goal(?: (.+?))? on project ([^:]+): (.+)"
    )
    match = pattern.match(line.strip())
    if match:
        goal = match.group(1).strip() if match.group(1) else ""
        project = match.group(2).strip()
        message = match.group(3).strip()
        if "could not resolve dependencies" in message.lower():
            # Collect details from subsequent [ERROR] lines
            details = []
            i = index + 1
            while i < len(lines) and lines[i].strip().startswith("[ERROR]"):
                detail_line = lines[i].strip()[8:].strip()
                details.append(detail_line)
                i += 1
            error = DependencyResolutionError(
                file=pom_file_path or "pom.xml",
                line=-1,
                column=-1,
                message=message,
                details=details,
                parse_lines="\n".join(lines[index:i]),
                project=project,
                goal=goal,
            )
            return error, i
    return None, index + 1


def parse_compilation_errors(
    lines: list[str], start_index: int
) -> tuple[int, list[MavenCompilerError]]:
    """
    Parses the compilation error section and returns a list of MavenCompilerError instances.
    """
    errors = []
    i = start_index
    while i < len(lines):
        line = lines[i]
        if is_section_end(line):
            break

        # Ignore non-error lines
        if (
            line.startswith("[INFO]")
            or line.startswith("[WARNING]")
            or line.strip() == ""
        ):
            i += 1
            continue

        match = re.match(r"\[ERROR\] (.+?):(?:\[(\d+),(\d+)\])? (.+)", line)
        if match:
            error, i = parse_error_line(lines, i, match)
            errors.append(error)
        else:
            i += 1
    return i, errors


def is_section_end(line: str) -> bool:
    """
    Determines if the current line indicates the end of an error section.
    """
    return line.startswith("[INFO] BUILD FAILURE") or line.startswith(
        "[ERROR] BUILD FAILURE"
    )


def match_build_error(line: str, file_path: str) -> Optional[MavenCompilerError]:
    """
    Matches a build error line and returns a BuildError instance.
    """
    match = BUILD_ERROR_PATTERN.match(line)
    if match:
        message = match.group(2).strip()
        line_number = int(match.group(3))
        column_number = int(match.group(4))
        # Try to extract file path from message
        file_path_match = re.search(r"Non-parseable POM (.+?):", message)
        if file_path_match:
            file_path = file_path_match.group(1).strip()
        error = BuildError(
            file=file_path,
            line=line_number,
            column=column_number,
            message=message,
            details=[],
        )
        return error
    return None


def parse_error_line(
    lines: list[str], index: int, match: re.Match[str]
) -> tuple[MavenCompilerError, int]:
    """
    Parses an error line and returns a MavenCompilerError instance and the next index.
    """
    acc = [lines[index]]
    file_path = match.group(1).strip()
    line_number = int(match.group(2)) if match.group(2) else -1
    column_number = int(match.group(3)) if match.group(3) else -1
    message = match.group(4).strip()

    error_class = classify_error(message)
    error = error_class(
        file=file_path,
        line=line_number,
        column=column_number,
        message=message,
        details=[],
    )

    # Look ahead for details
    details, next_index = extract_error_details(lines, index + 1)
    error.details.extend(details)

    # Extract additional information based on error type
    extract_additional_info(error)

    error.parse_lines = "\n".join(acc + details)
    return error, next_index


def extract_error_details(lines: list[str], start_index: int) -> tuple[list[str], int]:
    """
    Extracts detail lines following an error line.
    """
    details = []
    i = start_index
    while i < len(lines) and lines[i].startswith("  "):
        detail_line = lines[i].strip()
        details.append(detail_line)
        i += 1
    return details, i


def extract_additional_info(error: MavenCompilerError) -> None:
    """
    Extracts additional information based on error type.
    """
    if isinstance(error, SymbolNotFoundError):
        for detail in error.details:
            if "symbol:" in detail:
                error.missing_symbol = detail.split("symbol:")[-1].strip()
            if "location:" in detail:
                error.symbol_location = detail.split("location:")[-1].strip()
    elif isinstance(error, PackageDoesNotExistError):
        error.missing_package = (
            error.message.split("package")[-1].split("does not exist")[0].strip()
        )
    elif isinstance(error, TypeMismatchError):
        for detail in error.details:
            if "required:" in detail:
                error.expected_type = detail.split("required:")[-1].strip()
            if "found:" in detail:
                error.found_type = detail.split("found:")[-1].strip()
    elif isinstance(error, AccessControlError):
        error.inaccessible_class = error.message.split("cannot access")[-1].strip()


def catchall(output: str) -> OtherError:
    """
    Failsafe mechanism when rc != 0 and no errors are found.
    """
    file_path_pattern = re.compile(r"(/[^:\s]+)")
    file_path_matches = file_path_pattern.findall(output)
    file_path = file_path_matches[0] if file_path_matches else "unknown file"
    return OtherError(
        file=file_path,
        line=-1,
        column=-1,
        message="Unknown error occurred during Maven build.",
        details=[output],
        parse_lines=output,
    )


def deduplicate_errors(errors: list[MavenCompilerError]) -> list[MavenCompilerError]:
    """
    Deduplicates errors based on file, line, column, and message.
    """
    file_type_to_collapsable_error: dict[str, CollapsedMavenCompilerError] = {}
    unique_errors = []
    seen_errors = set()
    for error in errors:
        error_id = (error.file, error.line, error.column, error.message)
        if error_id not in seen_errors:
            seen_errors.add(error_id)
            if isinstance(error, CollapsedMavenCompilerError):
                dict_key = error.get_collapsable_key()
                if dict_key in file_type_to_collapsable_error.keys():
                    new_error = file_type_to_collapsable_error.get(dict_key)
                    if not new_error:
                        continue
                    if not new_error.lines:
                        new_error.lines = [new_error.line]
                        ## Setting this, because we don't want these collapsed errors
                        ## to ever skip fuzzy matching, which not matching line numbers will do
                        new_error.line = 0
                    new_error.lines.append(error.line)
                else:
                    file_type_to_collapsable_error[dict_key] = error
            else:
                unique_errors.append(error)

    for file_path_type, collapsed_error in file_type_to_collapsable_error.items():
        logger.debug(
            "adding collapsed_error: %s-lines:%s -- for key: %s",
            collapsed_error,
            collapsed_error.error_lines,
            file_path_type,
        )
        if not isinstance(collapsed_error, MavenCompilerError):
            logger.debug(
                "something went wrong, invalid error in collapsable: %s",
                collapsed_error,
            )
            continue
        unique_errors.append(collapsed_error)

    return unique_errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Maven compile in a specified source directory."
    )
    parser.add_argument(
        "source_directory", help="The directory where 'mvn compile' should be run."
    )
    args = parser.parse_args()
    rc, maven_output, pom_file_path = run_maven(Path(args.source_directory))

    results: dict[str, list[MavenCompilerError]] = {}
    build_errors, dependency_errors, compilation_errors, catchall_errors = (
        parse_maven_output(maven_output, rc, str(pom_file_path))
    )
    errors = build_errors + dependency_errors + compilation_errors + catchall_errors
    for error in errors:
        if not results.get(error.file):
            results[error.file] = [error]
        else:
            results[error.file].append(error)
    for file, errors in results.items():
        errs_line = f"| Errors for file: {file} |"
        print(errs_line)
        print("-" * len(errs_line))
        for error in errors:
            print(f"Line: {error.line}, Column: {error.column}")
            print(f"Type: {type(error).__name__}")
            print(f"Message: {error.message}")
            if isinstance(error, SymbolNotFoundError):
                print(f"Missing Symbol: {error.missing_symbol}")
                print(f"Symbol Location: {error.symbol_location}")
            elif isinstance(error, PackageDoesNotExistError):
                print(f"Missing Package: {error.missing_package}")
            elif isinstance(error, TypeMismatchError):
                print(f"Expected Type: {error.expected_type}")
                print(f"Found Type: {error.found_type}")
            elif isinstance(error, AccessControlError):
                print(f"Inaccessible Class: {error.inaccessible_class}")
            if error.details:
                print("Details:")
                for detail in error.details:
                    print(f"  {detail}")
            print("Source lines:")
            print(error.parse_lines)
            print("-" * 40)
