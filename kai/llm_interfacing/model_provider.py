from __future__ import annotations

import datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Optional

from genai import Client, Credentials
from genai.extensions.langchain.chat_llm import LangChainChatInterface
from genai.schema import DecodingMethod
from langchain_aws import ChatBedrock
from langchain_community.chat_models import ChatOllama
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.load import dumps, loads
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic.v1.utils import deep_update

from kai.logging.logging import get_logger
from kai_solution_server.kai_config import KaiConfigModels

LOG = get_logger(__name__)


class ModelProvider:
    def __init__(
        self,
        config: KaiConfigModels,
        demo_mode: bool = False,
        cache_dir: Path | None = None,
    ):
        self.llm_retries: int = config.llm_retries
        self.llm_retry_delay: float = config.llm_retry_delay
        self.demo_mode: bool = demo_mode
        self.cache_dir = cache_dir
        LOG.info("using cache dir: %s", self.cache_dir)

        model_class: type[BaseChatModel]
        defaults: dict[str, Any]
        model_args: dict[str, Any]
        model_id: str
        # Set the model class, model args, and model id based on the provider
        match config.provider:
            case "ChatOllama":
                model_class = ChatOllama

                defaults = {
                    "model": "mistral",
                    "temperature": 0.1,
                    "max_tokens": None,
                    "streaming": True,
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model"]

            case "ChatOpenAI":
                model_class = ChatOpenAI

                defaults = {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.1,
                    # "model_kwargs": {
                    #     "max_tokens": None,
                    # },
                    "streaming": True,
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model"]

            case "ChatIBMGenAI":
                model_class = LangChainChatInterface
                if get_env_bool("KAI__DEMO_MODE", False):
                    api_key = os.getenv("GENAI_KEY", "dummy_value")
                    api_endpoint = os.getenv("GENAI_API", "")
                    credentials = Credentials(
                        api_key=api_key, api_endpoint=api_endpoint
                    )
                else:
                    credentials = Credentials.from_env()
                defaults = {
                    "client": Client(credentials=credentials),
                    "model_id": "ibm-mistralai/mixtral-8x7b-instruct-v01-q",
                    "parameters": {
                        "decoding_method": DecodingMethod.SAMPLE,
                        # NOTE: probably have to do some more clever stuff regarding
                        # config. max_new_tokens and such varies between models
                        "max_new_tokens": 4096,
                        "min_new_tokens": 10,
                        "temperature": 0.05,
                        "top_k": 20,
                        "top_p": 0.9,
                        "return_options": {"input_text": False, "input_tokens": True},
                    },
                    "moderations": {
                        # Threshold is set to very low level to flag everything
                        # (testing purposes) or set to True to enable HAP with
                        # default settings
                        "hap": {"input": True, "output": False, "threshold": 0.01}
                    },
                    "streaming": True,
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model_id"]

            case "ChatBedrock":
                model_class = ChatBedrock

                defaults = {
                    "model_id": "meta.llama3-70b-instruct-v1:0",
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model_id"]

            case "FakeListChatModel":
                model_class = FakeListChatModel

                defaults = {
                    "responses": [
                        "## Reasoning\n"
                        "\n"
                        "Default reasoning.\n"
                        "\n"
                        "## Updated File\n"
                        "\n"
                        "```\n"
                        "Default updated file.\n"
                        "```\n"
                        "\n"
                        "## Additional Information\n"
                        "\n"
                        "Default additional information.\n"
                        "\n"
                    ],
                    "sleep": None,
                }

                model_args = deep_update(defaults, config.args)
                model_id = "fake-list-chat-model"

            case "ChatGoogleGenerativeAI":
                model_class = ChatGoogleGenerativeAI
                api_key = os.getenv("GOOGLE_API_KEY", "dummy_value")
                defaults = {
                    "model": "gemini-pro",
                    "temperature": 0.7,
                    "streaming": False,
                    "google_api_key": api_key,
                }
                model_args = deep_update(defaults, config.args)
                model_id = model_args["model"]

            case _:
                raise Exception(f"Unrecognized provider '{config.provider}'")

        self.provider_id: str = config.provider
        self.llm: BaseChatModel = model_class(**model_args)
        self.model_id: str = model_id

        if config.template is None:
            self.template = self.model_id
        else:
            self.template = config.template

        if config.llama_header is None:
            self.llama_header = self.model_id in [
                "mistralai/mistral-7b-instruct-v0-2",
                "mistralai/mixtral-8x7b-instruct-v01",
                "codellama/codellama-34b-instruct",
                "codellama/codellama-70b-instruct",
                "deepseek-ai/deepseek-coder-33b-instruct",
                "tiiuae/falcon-180b",
                "tiiuae/falcon-40b",
                "ibm/falcon-40b-8lang-instruct",
                "meta-llama/llama-2-70b-chat",
                "meta-llama/llama-2-13b-chat",
                "meta-llama/llama-2-7b",
                "meta-llama/llama-3-70b-instruct",
                "meta-llama/llama-3-8b-instruct",
            ]
        else:
            self.llama_header = config.llama_header

    def invoke(
        self,
        input: LanguageModelInput,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> BaseMessage:
        if self.demo_mode and self.cache_dir is not None:
            cache_file = self.__get_cache_filename(input)

            LOG.info(f"Using cache file {cache_file}")

            if os.path.exists(cache_file):
                try:
                    LOG.debug(f"Cache exists, loading from {cache_file}")
                    content = ""
                    with open(cache_file, "r") as f:
                        content = f.read()
                    entry: dict[str, Any] = loads(content)
                    cached_res: BaseMessage | None = entry.get("output", None)
                    if cached_res is not None:
                        return cached_res
                except Exception as e:
                    LOG.error(f"Failed retrieving response from cache - {e}")

            response = self.llm.invoke(input, config, stop=stop, **kwargs)
            to_cache = response.model_copy()
            to_cache.response_metadata.get("meta", {}).pop("created_at", None)
            try:
                json_repr = dumps(
                    {
                        "input": input,
                        "output": to_cache,
                    },
                    pretty=True,
                )
                LOG.debug("Storing response to cache")
                with open(cache_file, "w+") as f:
                    f.write(json_repr)
            except Exception as e:
                LOG.error(f"Failed to store response to cache - {e}")
            return response
        return self.llm.invoke(input, config, stop=stop, **kwargs)

    def __get_cache_filename(self, input: LanguageModelInput) -> str:
        if self.cache_dir is None:
            return ""
        param_str = json.dumps(
            {"input": input, "model_id": self.model_id}, sort_keys=True, default=str
        )
        hash_value = hashlib.sha256(param_str.encode()).hexdigest()
        dir = os.path.join(self.cache_dir, self.model_id)
        os.makedirs(dir, exist_ok=True)
        return os.path.join(dir, f"{hash_value}.json")


# TODO(Shawn): Remove when we get to config update that
def str_to_bool(val: str) -> bool:
    """
    Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_env_bool(key: str, default: Optional[bool] = None) -> bool | None:
    """
    Get a boolean value from an environment variable, returning the default if
    the variable is not set.
    """
    val = os.getenv(key)
    if val is None:
        return default
    return str_to_bool(val)


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)
