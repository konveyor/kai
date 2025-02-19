from __future__ import annotations

import os
from typing import Any, Optional, assert_never

from langchain_aws import ChatBedrock
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.language_models.base import BaseLanguageModel, LanguageModelInput
from langchain_core.messages import BaseMessage
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

        model_class: type[BaseLanguageModel[Any]]
        defaults: dict[str, Any]
        model_args: dict[str, Any]
        model_id: str

        # Set the model class, model args, and model id based on the provider
        match config.provider:
            case SupportedModelProviders.CHAT_OLLAMA:
                model_class = ChatOllama

                defaults = {
                    "model": "mistral",
                    "temperature": 0.1,
                    "max_tokens": None,
                    "streaming": True,
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model"]

            case SupportedModelProviders.CHAT_OPENAI:
                model_class = ChatOpenAI

                defaults = {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.1,
                    "streaming": True,
                }

                model_args = deep_update(defaults, config.args)
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

                if not (model_id.startswith("o1") or model_id.startswith("o3")):
                    ChatOpenAI._default_params = _default_params  # type: ignore[method-assign]
                    ChatOpenAI._get_request_payload = _get_request_payload  # type: ignore[method-assign]
                else:
                    if "streaming" in model_args:
                        del model_args["streaming"]
                    if "temperature" in model_args:
                        del model_args["temperature"]

            case SupportedModelProviders.CHAT_BEDROCK:
                model_class = ChatBedrock

                defaults = {
                    "model_id": "meta.llama3-70b-instruct-v1:0",
                }

                model_args = deep_update(defaults, config.args)
                model_id = model_args["model_id"]

            case SupportedModelProviders.FAKE_LIST_CHAT_MODEL:
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

            case SupportedModelProviders.CHAT_GOOGLE_GENERATIVE_AI:
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

            case SupportedModelProviders.AZURE_CHAT_OPENAI:
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

            case SupportedModelProviders.CHAT_DEEP_SEEK:
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
                assert_never(config.provider)
                raise Exception(f"Unrecognized provider '{config.provider}'")

        self.provider_id: str = config.provider
        self.llm: BaseLanguageModel[Any] = model_class(**model_args)
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
            return self.invoke("a", cpr, configurable_fields={k: 1})

        if isinstance(self.llm, ChatOllama):
            challenge("num_predict")
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

    @tracer.start_as_current_span("invoke_llm")
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
        span = trace.get_current_span()
        span.set_attribute("model", self.model_id)
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
            return self.response_to_base_message(
                invoke_llm.invoke(input, config, stop=stop, **kwargs)
            )

        cache_path = cache_path_resolver.cache_path()
        cache_meta = cache_path_resolver.cache_meta()

        if self.demo_mode:
            cache_entry = self.cache.get(path=cache_path, input=input)

            if cache_entry:
                return cache_entry

        response = invoke_llm.invoke(input, config, stop=stop, **kwargs)

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

        return self.response_to_base_message(response)

    def response_to_base_message(self, llm_response: Any) -> BaseMessage:
        if isinstance(llm_response, str):
            return BaseMessage(content=llm_response, type="ai")
        elif isinstance(llm_response, BaseMessage):
            return llm_response

        raise ValueError(f"Unexpected LLM response type: {type(llm_response)}")
