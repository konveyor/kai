from dataclasses import dataclass

from kai.reactive_codeplanner.task_manager.api import ValidationError


@dataclass
class DependencyValidationError(ValidationError):
    pass
