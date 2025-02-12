import functools
import logging
import uuid
from contextvars import ContextVar
from enum import StrEnum
from typing import Any, Union, cast

from pydantic import ValidationInfo, field_validator

from kai.jsonrpc.core import JsonRpcServer
from kai.jsonrpc.util import CamelCaseBaseModel
from kai.logging.logging import KaiLogger


class SimpleChatMessage(CamelCaseBaseModel):
    message: str


class MarkdownChatMessage(CamelCaseBaseModel):
    message: str


class ChatMessageKind(StrEnum):
    SIMPLE_CHAT_MESSAGE = "SimpleChatMessage"
    MARKDOWN_CHAT_MESSAGE = "MarkdownChatMessage"
    JSON_CHAT_MESSAGE = "JsonChatMessage"


ChatMessageValue = Union[SimpleChatMessage, MarkdownChatMessage, dict[str, Any]]


class ChatMessage(CamelCaseBaseModel):
    kind: ChatMessageKind
    value: ChatMessageValue

    # The id for the current chat
    chat_token: str

    # The id for the message. The idea is that the client can use this to update the
    # message later, ex. for streaming.
    message_token: str

    @field_validator("value", mode="plain")
    def set_value_validation_model(
        v: Any, validation_info: ValidationInfo
    ) -> SimpleChatMessage | MarkdownChatMessage | dict[str, Any]:
        vals = validation_info.data
        if vals["kind"] == ChatMessageKind.SIMPLE_CHAT_MESSAGE:
            return SimpleChatMessage.model_validate(v)
        elif vals["kind"] == ChatMessageKind.MARKDOWN_CHAT_MESSAGE:
            return MarkdownChatMessage.model_validate(v)
        elif vals["kind"] == ChatMessageKind.JSON_CHAT_MESSAGE:
            if not isinstance(v, dict):
                raise ValueError("JSON_CHAT_MESSAGE value must be a dictionary")
            return v
        else:
            raise ValueError(f"Unknown ChatMessageKind: {vals['kind']}")


class Chatter:
    def __init__(
        self,
        server: JsonRpcServer | None = None,
        method: str | None = None,
        chat_token: str | None = None,
    ) -> None:
        self.server = server
        self.method = method

        self._last_chat_token = chat_token or ""

    @property
    def last_chat_token(self) -> str:
        return self._last_chat_token

    def chat(
        self,
        kind: ChatMessageKind,
        value: ChatMessageValue,
        chat_token: str | None = None,
        message_token: str | None = None,
        log: KaiLogger | None = None,
        log_level: str | int = "INFO",
    ) -> ChatMessage:
        if chat_token is None:
            chat_token = self._last_chat_token
        if message_token is None:
            message_token = str(uuid.uuid4())
        if isinstance(log_level, str):
            log_level = logging.getLevelNamesMapping()[log_level]

        message = ChatMessage(
            kind=kind,
            value=value,
            chat_token=chat_token,
            message_token=message_token,
        )

        if log is not None:
            log.log(log_level, f"chat: {message}")

        if self.server is not None and self.method is not None:
            self.server.send_notification(
                method=self.method,
                params=message.model_dump(),
            )

        return message

    def chat_simple(
        self,
        message: str,
        chat_token: str | None = None,
        message_token: str | None = None,
        log: KaiLogger | None = None,
        log_level: str | int = "INFO",
    ) -> ChatMessage:
        msg = self.chat(
            kind=ChatMessageKind.SIMPLE_CHAT_MESSAGE,
            value=SimpleChatMessage(message=message),
            chat_token=chat_token,
            message_token=message_token,
        )

        msg.value = cast(SimpleChatMessage, msg.value)

        if isinstance(log_level, str):
            log_level = logging.getLevelNamesMapping()[log_level]
        if log is not None:
            log.log(log_level, f"{msg.value.message}")

        return msg

    def chat_markdown(
        self,
        message: str,
        chat_token: str | None = None,
        message_token: str | None = None,
        log: KaiLogger | None = None,
        log_level: str | int = "INFO",
    ) -> ChatMessage:
        msg = self.chat(
            # FIXME: Change once markdown is supported
            # kind=ChatMessageKind.MARKDOWN_CHAT_MESSAGE,
            # value=MarkdownChatMessage(message=message),
            kind=ChatMessageKind.SIMPLE_CHAT_MESSAGE,
            value=SimpleChatMessage(message=message),
            chat_token=chat_token,
            message_token=message_token,
        )

        msg.value = cast(MarkdownChatMessage, msg.value)

        if isinstance(log_level, str):
            log_level = logging.getLevelNamesMapping()[log_level]
        if log is not None:
            log.log(log_level, f"{msg.value.message}")

        return msg

    def chat_json(
        self,
        message: dict[str, Any],
        chat_token: str | None = None,
        message_token: str | None = None,
        log: KaiLogger | None = None,
        log_level: str | int = "INFO",
    ) -> ChatMessage:
        msg = self.chat(
            kind=ChatMessageKind.JSON_CHAT_MESSAGE,
            value=message,
            chat_token=chat_token,
            message_token=message_token,
        )

        msg.value = cast(dict[str, Any], msg.value)

        if isinstance(log_level, str):
            log_level = logging.getLevelNamesMapping()[log_level]
        if log is not None:
            log.log(log_level, f"{msg.value}")

        return msg


@functools.cache
def get_chatter_contextvar() -> ContextVar[Chatter]:
    """
    Returns a ContextVar for the current Chatter object. Using contextvars to support
    the eventual migration to asyncio.

    NOTE: A ContextVar uses shallow copies, so any modifications of an object in one
    context bleed over into the other. For example, this will fail:

    ```python
    chatter = get_chatter()

    async def foo(level: str) -> None:
        chatter.get().log_level = level
        await asyncio.sleep(1)
        assert chatter.get().log_level == level

    async def main() -> None:
        get_chatter().set(Chatter(...))
        await asyncio.gather(foo("DEBUG"), foo("INFO"))

    asyncio.run(main())
    ```
    """
    return ContextVar("chatter", default=Chatter())
