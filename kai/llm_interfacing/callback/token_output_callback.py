from typing import Any, Optional
from uuid import UUID

import tiktoken
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, get_buffer_string
from langchain_core.outputs.llm_result import LLMResult

from kai.logging.logging import get_logger

LOG = get_logger(__name__)


class TokenOutputCallback(BaseCallbackHandler):

    def __init__(self, llm: BaseChatModel):
        self.model = llm

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> Any:
        llm_token_string = ""  # trunk-ignore(bandit/B105)
        for generation_list in response.generations:
            for generation in generation_list:
                llm_token_string += generation.text
        try:
            tokens = self.model.get_num_tokens(llm_token_string)
            LOG.info("output tokens: %s", tokens)
        except Exception:
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = len(enc.encode(llm_token_string))
            LOG.info("output tokens: %s", tokens)
        return

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        **kwargs: Any
    ) -> None:
        flat_messages = [item for sublist in messages for item in sublist]
        try:
            tokens = self.model.get_num_tokens_from_messages(flat_messages)
            LOG.info("input tokens: %s", tokens)
        except Exception:
            # Here we fall back to a default encoding if no model is found.
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = len(enc.encode(get_buffer_string(flat_messages)))
            LOG.info("input tokens: %s", tokens)
        return
