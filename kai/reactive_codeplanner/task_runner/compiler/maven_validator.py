#!/usr/bin/env python

import re
import subprocess  # trunk-ignore(bandit/B404)
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence, Type

from kai.logging.logging import get_logger
from kai.reactive_codeplanner.task_manager.api import (
    ValidationError,
    ValidationResult,
    ValidationStep,
)

logger = get_logger(__name__)


class MavenCompileStep(ValidationStep):

    def run(self) -> ValidationResult:
        maven_output = run_maven(self.config.repo_directory)
        errors: Sequence[ValidationError] = parse_maven_output(maven_output)
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
        line_number = int(match.group(2))
        column_number = int(match.group(3))
        message = match.group(4).strip()
        return cls(
            file=file_path,
            line=line_number,
            column=column_number,
            message=message,
            details=details.copy(),
        )


# Subclasses for specific error categories
@dataclass(eq=False)
class SymbolNotFoundError(MavenCompilerError):
    missing_symbol: Optional[str] = None
    symbol_location: Optional[str] = None
    priority: int = 2


@dataclass(eq=False)
class PackageDoesNotExistError(MavenCompilerError):
    priority: int = 1
    missing_package: Optional[str] = None


@dataclass(eq=False)
class SyntaxError(MavenCompilerError):
    priority: int = 2


@dataclass(eq=False)
class TypeMismatchError(MavenCompilerError):
    expected_type: Optional[str] = None
    found_type: Optional[str] = None


@dataclass(eq=False)
class AnnotationError(MavenCompilerError):
    pass


@dataclass(eq=False)
class AccessControlError(MavenCompilerError):
    inaccessible_class: Optional[str] = None


@dataclass(eq=False)
class OtherError(MavenCompilerError):
    priority: int = 6


def run_maven(source_directory: Path = Path(".")) -> str:
    """
    Runs 'mvn compile' and returns the combined stdout and stderr output.
    """
    cmd = ["mvn", "compile"]
    #  trunk-ignore-begin(bandit/B603)
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            cwd=source_directory,
        )
        return process.stdout
    #  trunk-ignore-end(bandit/B603)
    except FileNotFoundError:
        logger.info("Maven is not installed or not found in the system PATH.")
        return ""


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


def parse_maven_output(output: str) -> Sequence[MavenCompilerError]:
    """
    Parses the Maven output and returns a list of MavenCompilerError instances.
    """
    errors: list[MavenCompilerError] = []
    lines = output.splitlines()
    in_compilation_error_section = False
    error_pattern = re.compile(r"\[ERROR\] (.+?):\[(\d+),(\d+)\] (.+)")
    current_error: MavenCompilerError

    acc = []
    for i, line in enumerate(lines):
        if "[ERROR] COMPILATION ERROR :" in line:
            in_compilation_error_section = True
            continue
        if in_compilation_error_section:
            if line.startswith("[INFO] BUILD FAILURE"):
                in_compilation_error_section = False
                continue
            if (
                line.startswith("[INFO]")
                or line.startswith("[WARNING]")
                or line.strip() == ""
            ):
                # TODO what to do with these?
                continue
            # Match error lines with file path, line, column, and message
            match = error_pattern.match(line)
            if match:
                acc.append(line)
                error_class = classify_error(match.group(4))
                current_error = error_class.from_match(match, [])

                # Look ahead for details
                details = []
                j = i + 1
                while j < len(lines) and lines[j].startswith("  "):
                    acc.append(lines[j])
                    detail_line = lines[j].replace("[ERROR] ", "", -1).strip()
                    details.append(detail_line)
                    j += 1

                current_error.details.extend(details)
                # Extract additional information based on error type
                if isinstance(current_error, SymbolNotFoundError):
                    for detail in current_error.details:
                        if "symbol:" in detail:
                            current_error.missing_symbol = detail.split("symbol:")[
                                -1
                            ].strip()
                        if "location:" in detail:
                            current_error.symbol_location = detail.split("location:")[
                                -1
                            ].strip()
                elif isinstance(current_error, PackageDoesNotExistError):
                    current_error.missing_package = (
                        current_error.message.split("package")[-1]
                        .split("does not exist")[0]
                        .strip()
                    )
                elif isinstance(current_error, TypeMismatchError):
                    for detail in current_error.details:
                        if "required:" in detail:
                            current_error.expected_type = detail.split("required:")[
                                -1
                            ].strip()
                        if "found:" in detail:
                            current_error.found_type = detail.split("found:")[
                                -1
                            ].strip()
                elif isinstance(current_error, AccessControlError):
                    current_error.inaccessible_class = current_error.message.split(
                        "cannot access"
                    )[-1].strip()

                current_error.parse_lines = "\n".join(acc)
                errors.append(current_error)
                acc = []
            else:
                continue  # Line does not match error pattern
    return errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Maven compile in a specified source directory."
    )
    parser.add_argument(
        "source_directory", help="The directory where 'mvn compile' should be run."
    )
    args = parser.parse_args()
    maven_output = run_maven(Path(args.source_directory))

    results: dict[str, list[MavenCompilerError]] = {}
    for error in parse_maven_output(maven_output):
        if not results.get(error.file):
            results[error.file] = [error]
        else:
            results[error.file].append(error)
    for file, errors in results.items():
        errs_line = f"| Errors for file: {file} |"
        print(errs_line)
        print("-" * len(errs_line))
        for error in errors:
            # print(f"File: {error.file}")
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
