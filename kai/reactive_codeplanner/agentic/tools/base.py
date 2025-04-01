from abc import ABC

from langchain_core.messages import AIMessage, AnyMessage
from langchain_core.tools.base import BaseTool


class ToolError(Exception):
    pass


class ToolIdNotFound(ToolError):
    pass

    def __init__(self, user_message: str, message: AnyMessage):
        super().__init__(user_message)
        self.message = message


class KaiBaseTool(BaseTool):

    def get_tool_id(self, messages: list[AnyMessage]) -> str:
        currentMessage = messages[-1]
        if isinstance(currentMessage, AIMessage):
            for t in currentMessage.tool_calls:
                if t["name"] and t["name"] == str(self.__class__.__name__) and t["id"]:
                    return t["id"]
            raise ToolIdNotFound("could not find id", currentMessage)
        else:
            raise ToolIdNotFound("current message is not an AI Message", currentMessage)
