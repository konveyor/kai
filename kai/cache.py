import re
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from langchain_core.language_models import LanguageModelInput
from langchain_core.load import dumps, loads
from langchain_core.messages import BaseMessage

from kai.jsonrpc.util import AutoAbsPath
from kai.logging.logging import TRACE, get_logger
from kai.reactive_codeplanner.task_manager.api import Task, ValidationError

LOG = get_logger(__name__)


class CachePathResolver(ABC):
    """Class that dynamically generates a path to store cache and unique
    human-readable metadata that provides more info about the cache
    """

    @abstractmethod
    def cache_path(self) -> Path: ...

    @abstractmethod
    def cache_meta(self) -> dict[str, str]: ...


class Cache(ABC):
    @abstractmethod
    def get(
        self,
        path: Path,
        input: LanguageModelInput,
    ) -> Optional[BaseMessage]: ...

    @abstractmethod
    def put(
        self,
        path: Path,
        input: LanguageModelInput,
        output: BaseMessage,
        cache_meta: dict[str, str],
    ) -> None: ...


class BadCacheError(ValueError): ...


class JSONCacheWithTrace(Cache):
    """This is a simple file based JSON cache that uses Langchain's dump / load api
    In addition to caching, also supports generating traces of cache in a separate dir
    """

    def __init__(
        self,
        model_id: str,
        cache_dir: AutoAbsPath,
        enable_trace: bool = False,
        trace_dir: Optional[Path] = None,
        fail_on_cache_mismatch: bool = False,
    ):
        """
        Args:
            model_id (str): Name of the model to separate cache by models
            cache_dir (Path): Base dir where cache will be generated
            enable_trace (bool, optional): Whether or not to copy responses as traces to a separate dir
            trace_dir (Optional[Path], optional): Path where traces will be copied into
            fail_on_cache_mismatch (bool, optional): Fail when there is a mismatch in contents of cache
        """
        self.model_id = model_id
        self.cache_dir = cache_dir
        self.trace_dir = trace_dir
        self.enable_trace = enable_trace
        self.fail_on_cache_mismatch = fail_on_cache_mismatch
        LOG.info("Using cache dir: %s", self.cache_dir)

    def _trace(self, cache_file: Path) -> None:
        if not self.enable_trace or self.trace_dir is None:
            return None
        dest_path = self.trace_dir / cache_file.relative_to(self.cache_dir)
        if dest_path.exists():
            return None
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(cache_file, dest_path, follow_symlinks=False)
        except Exception as e:
            LOG.log(TRACE, f"Failed to generate cache trace {e}")

    def get(
        self,
        path: Path,
        input: LanguageModelInput,
    ) -> Optional[BaseMessage]:
        if not self.cache_dir.exists():
            return None

        cache_file = self.cache_dir / self.model_id / path

        LOG.info(f"Looking for cache file {cache_file}")

        try:
            if cache_file.exists():
                LOG.debug(f"Cache exists, loading from {cache_file}")
                self._trace(cache_file)
                content = cache_file.read_text()
                cache_entry: dict[str, Any] = loads(content)
                cached_input: Optional[LanguageModelInput] = cache_entry.get(
                    "input", None
                )
                if cached_input != input:
                    LOG.debug("Cache miss, cached input does not match given input")
                    LOG.debug(f"Cached input: {cached_input}")
                    LOG.debug(f"Given input: {input}")
                    if self.fail_on_cache_mismatch:
                        raise BadCacheError("Cache file content mismatch")
                cached_res: Optional[BaseMessage] = cache_entry.get("output", None)
                if cached_res is not None:
                    return cached_res
                else:
                    LOG.log(
                        TRACE, f"Cache miss despite file exists, bad file {cache_file}"
                    )
            else:
                LOG.log(TRACE, f"Cache miss, expected file path {cache_file}")
                return None
        except BadCacheError as e:
            raise e
        except Exception as e:
            LOG.error(f"Failed to read from cache {e}")
        return None

    def put(
        self,
        path: Path,
        input: LanguageModelInput,
        output: BaseMessage,
        cache_meta: Optional[dict[str, str]] = None,
    ) -> None:
        if not self.cache_dir.exists():
            LOG.log(TRACE, f"Creating cache dir {self.cache_dir}")
            self.cache_dir.mkdir(exist_ok=True)

        cache_file = self.cache_dir / self.model_id / path

        LOG.debug(f"Storing cache in {cache_file}")

        cache_file.parent.mkdir(parents=True, exist_ok=True)

        to_cache = output.model_copy()
        to_cache.response_metadata.get("meta", {}).pop("created_at", None)
        try:
            cache_entry: dict[str, Any] = {
                "input": input,
                "output": to_cache,
            }
            if cache_meta is not None:
                cache_entry["meta"] = cache_meta
            json_repr = dumps(
                cache_entry,
                pretty=True,
            )
            cache_file.touch()
            cache_file.write_text(json_repr)
            self._trace(cache_file)
        except Exception as e:
            LOG.error(f"Failed to store response to cache - {e}")


class TaskBasedPathResolver(CachePathResolver):
    """Generates cache paths unique to each Task in reactive codeplanner.
    The generated path mimics the original spawn hierarchy of the task.
    """

    def __init__(self, task: Task, request_type: str = "llm_request"):
        self.task = task
        self.request_type = request_type
        self._req_count = 0

    def _dfs(self, task: Optional[Task]) -> Path:
        if not task:
            return Path(".")
        if isinstance(task, ValidationError):
            filename = re.sub(r"[\\/:\.]", "_", task.file)
            filename = re.sub(r"\_+", "_", filename)
            segments = filename.split("_")
            filename = "_".join(segments[-min(3, len(segments)) :])
            filename = filename[-min(50, len(filename)) :]
            return (
                self._dfs(task.parent)
                / task.__class__.__name__
                / filename
                / f"line_{task.line}"
            )
        else:
            return (
                self._dfs(task.parent)
                / task.__class__.__name__
                / f"prio_{task.priority}_depth_{task.depth}"
            )

    def cache_meta(self) -> dict[str, str]:
        meta = {
            "taskType": self.task.__class__.__name__,
            "taskString": str(self.task),
        }
        if isinstance(self.task, ValidationError):
            meta["file"] = self.task.file
            meta["message"] = self.task.message
        return meta

    def cache_path(self) -> Path:
        path = self._dfs(self.task) / f"{self._req_count}_{self.request_type}.json"
        self._req_count += 1
        return path
