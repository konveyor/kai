from __future__ import annotations

import datetime
import json
import os
from typing import Any, Optional

from langchain_aws import ChatBedrock
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic.v1.utils import deep_update

from kai.cache import Cache, CachePathResolver
from kai.kai_config import KaiConfigModels
from kai.logging.logging import get_logger

LOG = get_logger(__name__)


class ModelProvider:
    def __init__(
        self,
        config: KaiConfigModels,
        demo_mode: bool = False,
        cache: Optional[Cache] = None,
    ):
        self.llm_retries: int = config.llm_retries
        self.llm_retry_delay: float = config.llm_retry_delay
        self.demo_mode: bool = demo_mode
        self.cache = cache

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

            case "AzureChatOpenAI":
                model_class = AzureChatOpenAI

                defaults = {
                    "azure_deployment": "gpt-35-turbo",
                    "api_version": "2023-06-01-preview",
                    "temperature": 0.1,
                    "max_tokens": None,
                    "timeout": None,
                    "max_retries": 2,
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["azure_deployment"]

            case "ChatDeepSeek":
                model_class = ChatDeepSeek

                defaults = {
                    "model": "deepseek-chat",
                    "temperature": 0,
                    "max_tokens": None,
                    "timeout": None,
                    "max_retries": 2,
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
        cache_path_resolver: CachePathResolver,
        config: Optional[RunnableConfig] = None,
        *,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> BaseMessage:
        cache_path = cache_path_resolver.cache_path()
        cache_meta = cache_path_resolver.cache_meta()

        if self.demo_mode and self.cache:
            cache_entry = self.cache.get(path=cache_path, input=input)

            if cache_entry:
                return cache_entry

        response = self.llm.invoke(input, config, stop=stop, **kwargs)

        if self.cache:
            self.cache.put(
                path=cache_path,
                input=input,
                output=response,
                cache_meta=cache_meta,
            )

        return response


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
