from abc import ABC, abstractmethod
from typing import Optional

from kai.reactive_codeplanner.agent.reflection_agent import ReflectionTask


class SpawningResult(ABC):
    @abstractmethod
    def to_reflection_task(self) -> Optional[ReflectionTask]:
        pass
