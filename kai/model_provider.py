import os
from abc import ABC, abstractmethod
from typing import Iterator

from genai import Client, Credentials
from genai.extensions.langchain.chat_llm import LangChainChatInterface
from genai.schema import (
    DecodingMethod,
    ModerationHAP,
    ModerationParameters,
    TextGenerationParameters,
    TextGenerationReturnOptions,
)
from langchain_community.chat_models import ChatOllama, ChatOpenAI
from langchain_core.messages import BaseMessage, BaseMessageChunk

from kai import prompt_builder

"""
TODO: Add comments. General idea is that we can use dependency injection to
handle all things related to the llm. Right now, each model should have a
prompt_builder config, and a way to stream the output. It's a simple wrapper
around LangChain, but could get more complicated as the project grows
"""

# from langchain.globals import set_debug
# set_debug(True)


class ModelProvider(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> BaseMessage:
        pass

    @abstractmethod
    def stream(self, prompt: str) -> Iterator[BaseMessageChunk]:
        pass

    @abstractmethod
    def get_prompt_builder_config(self):
        pass

    @abstractmethod
    def get_models(self) -> list[str]:
        pass

    @abstractmethod
    def get_current_model_id(self) -> str:
        pass


class IBMGraniteModel(ModelProvider):
    def __init__(
        self,
        model_id: str = "ibm/granite-13b-chat-v2",
        temperature=0.05,
        top_k=20,
        top_p=0.9,
        max_new_tokens=4096,
        min_new_tokens=10,
        template="",
    ) -> None:
        if os.environ.get("GENAI_KEY") is None:
            raise Exception(
                "Must set GENAI_KEY in environment if using IBMGraniteModel"
            )

        self.template = template

        self.models = [
            # NOTE: Some of these models require some extra "plumbing", unsure how to use
            "ibm/granite-20b-code-instruct-v1",
            "ibm/granite-13b-chat-v1",
            "ibm/granite-13b-chat-v2",
            "ibm/granite-13b-lab-incubation",
            "ibm/granite-20b-code-instruct-v1",
            "ibm/granite-20b-code-instruct-v1-gptq",
            "ibm/granite-20b-multilang-lab-rc",
            "ibm/granite-20b-multilingual",
            "ibm/granite-3b-code-plus-v1",
            "ibm/granite-20b-code-javaenterprise",
        ]

        if model_id in self.models:
            self.model_id = model_id
        else:
            valid_models = "\n\t".join(self.models)
            raise Exception(
                f"Invalid model_id: {model_id}\nValid models: {valid_models}"
            )

        self.llm = LangChainChatInterface(
            client=Client(credentials=Credentials.from_env()),
            model_id=model_id,
            template=template,
            parameters=TextGenerationParameters(
                decoding_method=DecodingMethod.SAMPLE,
                max_new_tokens=max_new_tokens,
                min_new_tokens=min_new_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                return_options=TextGenerationReturnOptions(
                    input_text=False, input_tokens=True
                ),
            ),
            moderations=ModerationParameters(
                # Threshold is set to very low level to flag everything (testing purposes)
                # or set to True to enable HAP with default settings
                hap=ModerationHAP(input=True, output=False, threshold=0.01)
            ),
            streaming=True,
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)

    def stream(self, prompt: str) -> Iterator[BaseMessageChunk]:
        return self.llm.stream(prompt)

    def get_prompt_builder_config(self, query_kind: str, override_template: str = None):
        if override_template is None:
            override_template = self.template

        match (query_kind, override_template):
            case ("single_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE
            case ("multi_file", "preamble_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_ONLY
            case ("multi_file", "preamble_with_analysis_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_WITH_ANALYSIS_ONLY
            case ("multi_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE_MF
            case _:
                raise Exception(f"{query_kind=} {override_template=} not supported.")

    def get_models(self) -> list[str]:
        return self.models

    def get_current_model_id(self) -> str:
        return self.model_id


class IBMOpenSourceModel(ModelProvider):
    def __init__(
        self,
        model_id: str = "meta-llama/llama-2-13b-chat",
        temperature=0.05,
        top_k=20,
        top_p=0.9,
        max_new_tokens=4096,
        min_new_tokens=10,
        template="",
    ) -> None:
        if os.environ.get("GENAI_KEY") is None:
            raise Exception(
                "Must set GENAI_KEY in environment if using IBMGraniteModel"
            )

        self.template = template

        self.models = [
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

        if model_id in self.models:
            self.model_id = model_id
        else:
            valid_models = "\n\t".join(self.models)
            raise Exception(
                f"Invalid model_id: {model_id}\nValid models: {valid_models}"
            )

        self.llm = LangChainChatInterface(
            client=Client(credentials=Credentials.from_env()),
            model_id=model_id,
            template=template,
            parameters=TextGenerationParameters(
                decoding_method=DecodingMethod.SAMPLE,
                # NOTE: probably have to do some more clever stuff regarding
                # config. max_new_tokens and such varies between models
                # max_new_tokens=4096,
                max_new_tokens=max_new_tokens,
                min_new_tokens=min_new_tokens,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                return_options=TextGenerationReturnOptions(
                    input_text=False, input_tokens=True
                ),
            ),
            moderations=ModerationParameters(
                # Threshold is set to very low level to flag everything (testing purposes)
                # or set to True to enable HAP with default settings
                hap=ModerationHAP(input=True, output=False, threshold=0.01)
            ),
            streaming=True,
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)

    def stream(self, prompt: str) -> Iterator[BaseMessageChunk]:
        return self.llm.stream(prompt)

    def get_prompt_builder_config(self, query_kind: str, override_template: str = None):
        if override_template is None:
            override_template = self.template

        match (query_kind, override_template):
            case ("single_file", _):
                return prompt_builder.CONFIG_IBM_LLAMA
            case ("multi_file", "preamble_only"):
                return prompt_builder.CONFIG_IBM_LLAMA_MF_PREAMBLE_ONLY
            case ("multi_file", "preamble_with_analysis_only"):
                return prompt_builder.CONFIG_IBM_LLAMA_MF_PREAMBLE_WITH_ANALYSIS_ONLY
            case ("multi_file", _):
                return prompt_builder.CONFIG_IBM_LLAMA_MF
            case _:
                raise Exception(f"{query_kind=} {override_template=} not supported.")

    def get_models(self) -> list[str]:
        return self.models

    def get_current_model_id(self) -> str:
        return self.model_id


# FIXME: Remove for final demo
class OpenAIModel(ModelProvider):
    def __init__(
        self,
        model_id: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_new_tokens: int = None,
        template: str = "",
    ):
        self.template = template

        self.models = [
            "gpt-4-0125-preview",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-4-vision-preview",
            "gpt-4-1106-vision-preview",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-instruct",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
        ]

        if model_id in self.models:
            self.model_id = model_id
        else:
            valid_models = "\n\t".join(self.models)
            raise Exception(
                f"Invalid model_id: {model_id}\nValid models: {valid_models}"
            )

        self.llm = ChatOpenAI(
            model=self.model_id,
            streaming=True,
            temperature=temperature,
            max_tokens=max_new_tokens,
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)

    def stream(self, prompt: str):
        return self.llm.stream(prompt)

    def get_prompt_builder_config(self, query_kind: str, override_template: str = None):
        if override_template is None:
            override_template = self.template

        match (query_kind, override_template):
            case ("single_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE
            case ("multi_file", "preamble_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_ONLY
            case ("multi_file", "preamble_with_analysis_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_WITH_ANALYSIS_ONLY
            case ("multi_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE_MF
            case _:
                raise Exception(f"{query_kind=} {override_template=} not supported.")

    def get_models(self) -> list[str]:
        return self.models

    def get_current_model_id(self) -> str:
        return self.model_id


class OllamaModel(ModelProvider):
    def __init__(
        self,
        model_id: str = "mistral",
        temperature: float = 0.1,
        max_new_tokens: int = None,
        template: str = "",
    ):
        self.template = template

        self.models = [
            "codellama",
            "llama3",
            "llama2",
            "mistral",
            "mixtral",
            "starcoder2",
            "wizardcoder",
        ]

        if model_id in self.models:
            self.model_id = model_id
        else:
            valid_models = "\n\t".join(self.models)
            raise Exception(
                f"Invalid model_id: {model_id}\nValid models: {valid_models}"
            )

        self.llm = ChatOllama(
            model=self.model_id,
            streaming=True,
            temperature=temperature,
            max_tokens=max_new_tokens,
        )

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)

    def stream(self, prompt: str):
        return self.llm.stream(prompt)

    def get_prompt_builder_config(self, query_kind: str, override_template: str = None):
        if override_template is None:
            override_template = self.template

        match (query_kind, override_template):
            case ("single_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE
            case ("multi_file", "preamble_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_ONLY
            case ("multi_file", "preamble_with_analysis_only"):
                return prompt_builder.CONFIG_IBM_GRANITE_MF_PREAMBLE_WITH_ANALYSIS_ONLY
            case ("multi_file", _):
                return prompt_builder.CONFIG_IBM_GRANITE_MF
            case _:
                raise Exception(f"{query_kind=} {override_template=} not supported.")

    def get_models(self) -> list[str]:
        return self.models

    def get_current_model_id(self) -> str:
        return self.model_id
