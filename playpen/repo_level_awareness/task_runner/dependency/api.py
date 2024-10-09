from dataclasses import dataclass

from playpen.repo_level_awareness.api import ValidationError


@dataclass
class DependencyValidationError(ValidationError):
    pass
