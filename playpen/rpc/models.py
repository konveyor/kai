from enum import IntEnum
from typing import Any, Optional

from pydantic import BaseModel


class JsonRpcErrorCode(IntEnum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    ServerErrorStart = -32099
    ServerErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001


JsonRpcId = Optional[str | int]

# NOTE: dict must come before BaseModel in the union, otherwise Pydantic breaks
# when calling model_validate on JsonRpcResponse.
JsonRpcResult = dict | BaseModel  # type: ignore[type-arg]


class JsonRpcError(BaseModel):
    code: JsonRpcErrorCode | int
    message: str
    data: Optional[Any] = None


class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[JsonRpcResult] = None
    error: Optional[JsonRpcError | str] = None
    id: JsonRpcId = None


class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[dict[str, Any]] = None
    id: JsonRpcId = None


# JsonRpcRequestResult = tuple[JsonRpcResult | None, JsonRpcError | None]
