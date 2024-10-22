from dataclasses import dataclass

from kai.reactive_codeplanner.api import ValidationError


@dataclass
class DependencyValidationError(ValidationError):
    pass
