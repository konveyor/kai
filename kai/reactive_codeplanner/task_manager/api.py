from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional, Sequence


@dataclass
class RpcClientConfig:
    repo_directory: Path
    analyzer_lsp_server_binary: Path
    rules_directory: Path
    analyzer_lsp_path: Path
    analyzer_java_bundle_path: Path
    label_selector: Optional[str]
    incident_selector: Optional[str]
    included_paths: Optional[list[str]]
    dep_open_source_labels_path: Optional[Path] = None


@dataclass(eq=False, kw_only=True)
class Task:
    priority: int = 10
    depth: int = 0
    parent: Optional["Task"] = None
    children: list["Task"] = field(default_factory=list, compare=False)
    retry_count: int = 0
    max_retries: int = 3
    creation_order: int = field(init=False)
    demo_mode: bool = False

    _creation_counter = 0

    def __post_init__(self) -> None:
        self.creation_order = Task._creation_counter
        Task._creation_counter += 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Task) and self.__dict__ == other.__dict__

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Task):
            raise ValueError(f"Cannot compare Task with {type(other)}")

        # Lower priority number means higher priority
        # For same priority, higher depth means process children first (DFS)
        # For same priority and depth, rely on creation order just to make it deterministic
        return (self.priority, -self.depth, self.creation_order) < (
            other.priority,
            -other.depth,
            other.creation_order,
        )

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self) -> str:
        def truncate(value: str, max_length: int = 30) -> str:
            return (value[:max_length] + "...") if len(value) > max_length else value

        class_name = self.__class__.__name__
        field_strings = []
        for _field in fields(self):
            value = getattr(self, _field.name)
            truncated_value = truncate(str(value))
            field_strings.append(f'{_field.name}="{truncated_value}"')

        return f"{class_name}<" + ", ".join(field_strings) + ">"

    __repr__ = __str__


@dataclass(eq=False, kw_only=True)
class ValidationError(Task):
    file: str
    line: int
    column: int
    message: str
    priority: int = 5

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.file == other.file
            and self.line == other.line
            and self.column == other.column
            and self.message == other.message
        )

    def __hash__(self) -> int:
        return hash((self.file, self.line, self.column, self.message))

    def fuzzy_equals(self, error2: Task, offset: int = 1) -> bool:
        """
        Determines if two ValidationError objects are likely the same error,
        with a fuzzy comparison allowing for a line number offset.

        Args:
        - error1 (ValidationError): First error to compare.
        - error2 (ValidationError): Second error to compare.
        - offset (int): The allowed difference in line numbers for errors to still be considered the same.

        Returns:
        - bool: True if the errors are likely the same, False otherwise.
        """
        if isinstance(error2, ValidationError):
            return (
                self.file == error2.file
                and abs(self.line - error2.line) <= offset
                and self.column == error2.column
                and self.message == error2.message
            )
        return False


# FIXME: Might not need
@dataclass
class TaskResult:
    encountered_errors: list[str]
    modified_files: list[Path]


@dataclass
class ValidationResult:
    passed: bool
    errors: Sequence[ValidationError]


class ValidationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ValidationStep(ABC):
    def __init__(self, RpcClientConfig: RpcClientConfig) -> None:
        self.config = RpcClientConfig

    @abstractmethod
    def run(self) -> ValidationResult:
        pass
