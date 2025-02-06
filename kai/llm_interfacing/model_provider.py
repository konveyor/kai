from __future__ import annotations

import os
from typing import Any, Optional

from langchain_aws import ChatBedrock
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import ConfigurableField, RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from pydantic.v1.utils import deep_update

from kai.cache import Cache, CachePathResolver, SimplePathResolver
from kai.kai_config import KaiConfigModels
from kai.logging.logging import get_logger

LOG = get_logger(__name__)


class LLMCallBudgetReached(Exception):
    def __init__(
        self, message: str = "The defined LLM call budget has been reached"
    ) -> None:
        super().__init__(message)


class ModelProvider:

    llm_call_budget: int = -1

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
        self.llm_call_budget = config.llm_call_budget

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

    def validate_environment(
        self,
    ) -> None:
        """
        Raises an exception if the environment is not set up correctly for the
        current model provider.
        """

        cpr = SimplePathResolver("validate_environment.json")

        def challenge(k: str) -> BaseMessage:
            return self.invoke("", cpr, configurable_fields={k: 1})

        if isinstance(self.llm, ChatOllama):
            challenge("max_tokens")
        elif isinstance(self.llm, ChatOpenAI):
            challenge("max_tokens")
        elif isinstance(self.llm, ChatBedrock):
            challenge("max_tokens")
        elif isinstance(self.llm, FakeListChatModel):
            pass
        elif isinstance(self.llm, ChatGoogleGenerativeAI):
            challenge("max_output_tokens")
        elif isinstance(self.llm, AzureChatOpenAI):
            challenge("max_tokens")
        elif isinstance(self.llm, ChatDeepSeek):
            challenge("max_tokens")

    def invoke(
        self,
        input: LanguageModelInput,
        cache_path_resolver: Optional[CachePathResolver] = None,
        config: Optional[RunnableConfig] = None,
        *,
        configurable_fields: Optional[dict[str, Any]] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> BaseMessage:
        if self.llm_call_budget == 0:
            raise LLMCallBudgetReached
        # Some fields can only be configured when the model is instantiated.
        # This side-steps that by creating a new instance of the model with the
        # configurable fields set, then invoking that new instance.
        if configurable_fields is not None:
            invoke_llm = self.llm.configurable_fields(
                **{k: ConfigurableField(id=k) for k in configurable_fields}
            ).with_config(
                configurable_fields  # type: ignore[arg-type]
            )
        else:
            invoke_llm = self.llm

        if not (self.cache and cache_path_resolver):
            self.llm_call_budget -= 1
            return invoke_llm.invoke(input, config, stop=stop, **kwargs)

        cache_path = cache_path_resolver.cache_path()
        cache_meta = cache_path_resolver.cache_meta()

        if self.demo_mode:
            cache_entry = self.cache.get(path=cache_path, input=input)

            if cache_entry:
                return cache_entry

        self.llm_call_budget -= 1
        response = invoke_llm.invoke(input, config, stop=stop, **kwargs)

        self.cache.put(
            path=cache_path,
            input=input,
            output=response,
            cache_meta=cache_meta,
        )

        return response
