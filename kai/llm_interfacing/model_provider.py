from __future__ import annotations

import os
from abc import abstractmethod
from typing import Any, Iterator, Optional, Sequence, assert_never, cast, override

from langchain_aws import ChatBedrock
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
)
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import ConfigurableField, RunnableConfig
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from opentelemetry import trace
from pydantic.v1.utils import deep_update

from kai.cache import Cache, CachePathResolver, SimplePathResolver
from kai.kai_config import KaiConfigModels, SupportedModelProviders
from kai.logging.logging import get_logger

LOG = get_logger(__name__)
tracer = trace.get_tracer("model_provider")


class ModelProvider:
    @staticmethod
    def from_config(
        config: KaiConfigModels,
        demo_mode: bool = False,
        cache: Cache | None = None,
    ) -> "ModelProvider":
        match config.provider:
            case SupportedModelProviders.CHAT_OLLAMA:
                return ModelProviderChatOllama(config, demo_mode, cache)
            case SupportedModelProviders.CHAT_OPENAI:
                return ModelProviderChatOpenAI(config, demo_mode, cache)
            case SupportedModelProviders.CHAT_BEDROCK:
                return ModelProviderChatBedrock(config, demo_mode, cache)
            case SupportedModelProviders.FAKE_LIST_CHAT_MODEL:
                return ModelProviderFakeListChatModel(config, demo_mode, cache)
            case SupportedModelProviders.CHAT_GOOGLE_GENERATIVE_AI:
                return ModelProviderChatGoogleGenerativeAI(config, demo_mode, cache)
            case SupportedModelProviders.AZURE_CHAT_OPENAI:
                return ModelProviderAzureChatOpenAI(config, demo_mode, cache)
            case SupportedModelProviders.CHAT_DEEP_SEEK:
                return ModelProviderChatDeepSeek(config, demo_mode, cache)
            case _:
                assert_never(config.provider)

    def __init__(
        self,
        config: KaiConfigModels,
        demo_mode: bool,
        cache: Cache | None,
        model_class: type[BaseChatModel],
        defaults: dict[str, Any],
    ) -> None:
        self.llm_retries = config.llm_retries
        self.llm_retry_delay = config.llm_retry_delay
        self.demo_mode = demo_mode
        self.cache = cache
        self.provider_id = config.provider
        self.model_class = model_class
        self.validate_environment_resolver = SimplePathResolver(
            "validate_environment.json"
        )

        self.model_args, self.model_id = self.prepare_model_args(defaults, config.args)
        self.llm: BaseChatModel = self.model_class(**self.model_args)

    @abstractmethod
    def prepare_model_args(
        self, defaults: dict[str, Any], config_args: dict[str, Any]
    ) -> tuple[dict[str, Any], str]:
        """
        Do any necessary clever cleanup of the model args. Returns the model args and
        the model id.
        """
        ...

        # I'd like to do something like the following, but it didn't work when I tried it:

        # for attr in ["model", "model_name", "model_id", "azure_deployment"]:
        #     if hasattr(self.model_class, attr):
        #         return deep_update(defaults, config_args), config_args[attr]

        # raise Exception(f"Could not get model id for {self.model_class}. {dir(self.model_class)=}")

    def default_challenge(self, k: str) -> BaseMessage:
        return self.invoke(
            "a",
            self.validate_environment_resolver,
            configurable_fields={k: 1},
            do_continuation=False,
        )

    @abstractmethod
    def validate_environment(self) -> None:
        """
        Raises an exception if the environment is not set up correctly for the
        current model provider.
        """
        ...

    def configurable_llm(
        self,
        configurable_fields: dict[str, Any] | None = None,
    ) -> BaseChatModel:
        """
        Some fields can only be configured when the model is instantiated. This
        side-steps that by creating a new instance of the model with the configurable
        fields set, then invoking that new instance.
        """
        if configurable_fields is not None:
            result = self.llm.configurable_fields(
                **{k: ConfigurableField(id=k) for k in configurable_fields}
            ).with_config(
                configurable_fields  # type: ignore[arg-type]
            )
            return cast(BaseChatModel, result)  # TODO: Check if this cast is ok
        else:
            return self.llm

    def invoke_llm(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        configurable_fields: dict[str, Any] | None = None,
        stop: list[str] | None = None,
        do_continuation: bool = True,  # model must support it
        **kwargs: Any,
    ) -> BaseMessage:
        """
        Method to invoke the actual LLM. This can be overridden by subclasses to
        provide additional functionality.
        """
        return self.configurable_llm(configurable_fields).invoke(
            input, config, stop=stop, **kwargs
        )

    def stream_llm(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        configurable_fields: dict[str, Any] | None = None,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> Iterator[BaseMessageChunk]:
        return self.configurable_llm(configurable_fields).stream(
            input, config, stop=stop, **kwargs
        )

    @tracer.start_as_current_span("invoke_llm")
    def invoke(
        self,
        input: LanguageModelInput,
        cache_path_resolver: Optional[CachePathResolver] = None,
        config: Optional[RunnableConfig] = None,
        *,
        configurable_fields: Optional[dict[str, Any]] = None,
        stop: Optional[list[str]] = None,
        do_continuation: bool = True,
        **kwargs: Any,
    ) -> BaseMessage:
        """
        Method that invokes the LLM and caches the result if necessary.
        """
        span = trace.get_current_span()
        span.set_attribute("model", self.model_id)

        if not (self.cache and cache_path_resolver):
            return self.invoke_llm(
                input, config, configurable_fields, stop, do_continuation, **kwargs
            )

        cache_path = cache_path_resolver.cache_path()
        cache_meta = cache_path_resolver.cache_meta()

        if self.demo_mode:
            cache_entry = self.cache.get(path=cache_path, input=input)

            if cache_entry:
                return cache_entry

        response = self.invoke_llm(
            input, config, configurable_fields, stop, do_continuation, **kwargs
        )

        try:
            self.cache.put(
                path=cache_path,
                input=input,
                output=response,
                cache_meta=cache_meta,
            )
        except Exception as e:
            # only raise an exception when we are in demo mode
            if self.demo_mode:
                raise e
        return response

    @tracer.start_as_current_span("stream_llm")
    def stream(
        self,
        input: LanguageModelInput,
        cache_path_resolver: Optional[CachePathResolver] = None,
        config: Optional[RunnableConfig] = None,
        *,
        configurable_fields: Optional[dict[str, Any]] = None,
        stop: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> Iterator[BaseMessageChunk]:
        """
        Method that streams the LLM and caches the result if necessary.
        """
        # FIXME: Not caching the stream results currently
        yield from self.stream_llm(input, config, stop=stop, **kwargs)


class ModelProviderChatOllama(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=ChatOllama,
            defaults={
                "model": "mistral",
                "temperature": 0.1,
                "max_tokens": None,
                "streaming": True,
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("num_predict")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), config_args["model"]


class ModelProviderChatOpenAI(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=ChatOpenAI,
            defaults={
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "streaming": True,
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("max_tokens")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        model_args = deep_update(defaults, config_args)
        model_id = model_args["model"]

        # NOTE(JonahSussman): This is a hack to prevent `max_tokens`
        # from getting converted to `max_completion_tokens` for every
        # model, except for the o1 and o3 family of models.

        @property  # type: ignore[misc]
        def _default_params(self: ChatOpenAI) -> dict[str, Any]:
            return super(ChatOpenAI, self)._default_params

        def _get_request_payload(
            self: ChatOpenAI,
            input_: LanguageModelInput,
            *,
            stop: list[str] | None = None,
            **kwargs: Any,
        ) -> dict:  # type: ignore[type-arg]
            return super(ChatOpenAI, self)._get_request_payload(
                input_, stop=stop, **kwargs
            )

        if not (
            model_args["model"].startswith("o1") or model_args["model"].startswith("o3")
        ):
            ChatOpenAI._default_params = _default_params  # type: ignore[method-assign]
            ChatOpenAI._get_request_payload = _get_request_payload  # type: ignore[method-assign]
        else:
            if "streaming" in model_args:
                del model_args["streaming"]
            if "temperature" in model_args:
                del model_args["temperature"]

        return model_args, model_id


class ModelProviderChatBedrock(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=ChatBedrock,
            defaults={
                "model_id": "meta.llama3-70b-instruct-v1:0",
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("max_tokens")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), config_args["model_id"]

    # NOTE: Should we override `invoke` instead of `invoke_llm`?
    @override
    def invoke_llm(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        configurable_fields: dict[str, Any] | None = None,
        stop: list[str] | None = None,
        do_continuation: bool = True,
        **kwargs: Any,
    ) -> BaseMessage:
        if not do_continuation:
            return self.configurable_llm(configurable_fields).invoke(
                input, config, stop=stop, **kwargs
            )

        invoke_llm = self.configurable_llm(configurable_fields)

        messages: list[BaseMessage] = []
        continuation = False

        if isinstance(input, str):
            messages = [HumanMessage(input)]
        elif isinstance(input, PromptValue):
            messages = [HumanMessage(input.to_string())]
        elif isinstance(input, Sequence):
            messages = list(input)  # type: ignore[arg-type]
        else:
            assert_never(input)

        while True:
            message = invoke_llm.invoke(messages, config, stop=stop, **kwargs)

            if continuation:
                # TODO: Figure out if message.content is ever anything but a string
                messages[-1] = AIMessage(
                    (str(messages[-1].content) + str(message.content)).strip()
                )
            else:
                messages.append(AIMessage(str(message.content).strip()))
                continuation = True

            if (
                message.response_metadata.get("stop_reason") == "max_tokens"
                or message.additional_kwargs.get("stop_reason") == "max_tokens"
            ):
                LOG.info("Message did not fit in max tokens. Continuing...")
                continue

            break

        return messages[-1]


class ModelProviderFakeListChatModel(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=FakeListChatModel,
            defaults={
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
            },
        )

    def validate_environment(self) -> None:
        return

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), "fake-list-chat-model"


class ModelProviderChatGoogleGenerativeAI(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=ChatGoogleGenerativeAI,
            defaults={
                "model": "gemini-pro",
                "temperature": 0.7,
                "streaming": False,
                "google_api_key": os.getenv("GOOGLE_API_KEY", "dummy_value"),
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("max_output_tokens")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), config_args["model"]


class ModelProviderAzureChatOpenAI(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=AzureChatOpenAI,
            defaults={
                "azure_deployment": "gpt-35-turbo",
                "api_version": "2023-06-01-preview",
                "temperature": 0.1,
                "max_tokens": None,
                "timeout": None,
                "max_retries": 2,
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("max_tokens")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), config_args["azure_deployment"]


class ModelProviderChatDeepSeek(ModelProvider):
    def __init__(self, config: KaiConfigModels, demo_mode: bool, cache: Cache | None):
        super().__init__(
            config=config,
            demo_mode=demo_mode,
            cache=cache,
            model_class=ChatDeepSeek,
            defaults={
                "model": "deepseek-chat",
                "temperature": 0,
                "max_tokens": None,
                "timeout": None,
                "max_retries": 2,
            },
        )

    def validate_environment(self) -> None:
        self.default_challenge("max_tokens")

    def prepare_model_args(
        self,
        defaults: dict[str, Any],
        config_args: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        return deep_update(defaults, config_args), config_args["model"]
