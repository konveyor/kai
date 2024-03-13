import os
from abc import ABC, abstractmethod
from typing import Iterator

import prompt_builder
from genai import Client, Credentials
from genai.extensions.langchain.chat_llm import LangChainChatInterface
from genai.schema import (
    DecodingMethod,
    ModerationHAP,
    ModerationParameters,
    TextGenerationParameters,
    TextGenerationReturnOptions,
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.messages import (
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI

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
    def get_prompt_builder_config(self) -> prompt_builder.Config:
        pass

    @abstractmethod
    def get_models(self) -> list[str]:
        pass


class IBMGraniteModel(ModelProvider):
    def __init__(self, model_id: str = "ibm/granite-13b-chat-v2") -> None:
        if os.environ.get("GENAI_KEY") is None:
            raise Exception(
                "Must set GENAI_KEY in environment if using IBMGraniteModel"
            )

        self.prompt_builder_config = prompt_builder.CONFIG_IBM_GRANITE
        self.models = [
            # NOTE: These models require some extra "plumbing", unsure how to use
            # "ibm/granite-13b-instruct-v1",
            # "ibm/granite-13b-instruct-v2",
            # "ibm/granite-20b-5lang-instruct-rc",
            # "ibm/granite-20b-code-instruct-v1",
            # "ibm/granite-20b-code-instruct-v1-gptq",
            "ibm/granite-13b-chat-v2",
        ]

        if model_id in self.models:
            self.model_id = model_id
        else:
            self.model_id = "ibm/granite-20b-code-instruct-v1"

        self.llm = LangChainChatInterface(
            client=Client(credentials=Credentials.from_env()),
            model_id=model_id,
            parameters=TextGenerationParameters(
                decoding_method=DecodingMethod.SAMPLE,
                max_new_tokens=4096,
                min_new_tokens=10,
                temperature=0.1,
                top_k=50,
                top_p=1,
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

    def get_prompt_builder_config(self) -> prompt_builder.Config:
        return self.prompt_builder_config

    def get_models(self) -> list[str]:
        return self.models


class IBMLlamaModel(ModelProvider):
    def __init__(
        self,
        model_id: str = "meta-llama/llama-2-13b-chat",
    ) -> None:
        if os.environ.get("GENAI_KEY") is None:
            raise Exception(
                "Must set GENAI_KEY in environment if using IBMGraniteModel"
            )

        self.prompt_builder_config = prompt_builder.CONFIG_IBM_LLAMA
        self.models = [
            # "ibm-mistralai/mixtral-8x7b-instruct-v01-q",
            # "codellama/codellama-34b-instruct",
            # "codellama/codellama-70b-instruct",
            # "mistralai/mistral-7b-instruct-v0-2",
            # "thebloke/mixtral-8x7b-v0-1-gptq",
            "meta-llama/llama-2-13b-chat",
        ]

        if model_id in self.models:
            self.model_id = model_id
        else:
            self.model_id = "meta-llama/llama-2-13b-chat"

        self.llm = LangChainChatInterface(
            client=Client(credentials=Credentials.from_env()),
            model_id=model_id,
            parameters=TextGenerationParameters(
                decoding_method=DecodingMethod.SAMPLE,
                # NOTE: probably have to do some more clever stuff regarding
                # config. max_new_tokens and such varies between models
                # max_new_tokens=4096,
                max_new_tokens=1536,
                min_new_tokens=10,
                temperature=0.1,
                top_k=50,
                top_p=1,
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

    def get_prompt_builder_config(self) -> prompt_builder.Config:
        return self.prompt_builder_config

    def get_models(self) -> list[str]:
        return self.models


# FIXME: Remove for final demo
class OpenAIModel(ModelProvider):
    def __init__(self, model_id: str = "gpt-3.5-turbo"):
        self.prompt_builder_config = prompt_builder.CONFIG_IBM_GRANITE
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
            self.model_id = "gpt-3.5-turbo"

        self.llm = ChatOpenAI(model=self.model_id, streaming=True)

    def invoke(self, prompt: str):
        return self.llm.invoke(prompt)

    def stream(self, prompt: str):
        return self.llm.stream(prompt)

    def get_prompt_builder_config(self) -> prompt_builder.Config:
        return self.prompt_builder_config

    def get_models(self) -> list[str]:
        return self.models
