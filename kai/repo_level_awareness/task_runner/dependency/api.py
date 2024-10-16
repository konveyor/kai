from dataclasses import dataclass

from kai.repo_level_awareness.api import ValidationError


@dataclass
class DependencyValidationError(ValidationError):
    pass
