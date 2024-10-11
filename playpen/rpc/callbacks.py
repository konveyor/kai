from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, cast

from pydantic import BaseModel, ConfigDict, validate_call

from playpen.rpc.models import (
    JsonRpcError,
    JsonRpcErrorCode,
    JsonRpcRequestResult,
    JsonRpcResult,
)
from playpen.rpc.util import get_logger

if TYPE_CHECKING:
    from playpen.rpc.core import JsonRpcApplication, JsonRpcServer


log = get_logger("jsonrpc")

JsonRpcRequestCallable = Callable[..., JsonRpcRequestResult]
JsonRpcNotifyCallable = Callable[..., None]


class JsonRpcCallback:
    """
    A JsonRpcCallback is a wrapper around a JsonRpcMethodCallable or
    JsonRpcNotifyCallable. It validates the parameters and calls the function.

    We use this class to allow for more flexibility in the parameters that can
    be passed to the function.
    """

    def __init__(
        self,
        func: JsonRpcRequestCallable | JsonRpcNotifyCallable,
        include_server: bool,
        include_app: bool,
        kind: Literal["request", "notify"],
        method: str,
        params_model: type[JsonRpcResult] | None = None,
    ):
        """
        If params_model is not supplied, the schema will be generated from the
        function arguments.
        """

        self.func = func
        self.params_model = params_model
        self.include_server = include_server
        self.include_app = include_app
        self.kind = kind
        self.method = method

        @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
        @functools.wraps(self.func)
        def validate_func_args(
            *args: Any, **kwargs: Any
        ) -> tuple[tuple[Any, ...], dict[str, Any]]:
            return args, kwargs

        self.validate_func_args = validate_func_args

        # TODO: Generate docs
        # See https://github.com/konveyor/kai/blob/d7727a8113f185ee393d368a924da7c9deedd45b/playpen/rpc_server/rpc.py#L354

    def __call__(
        self,
        params: dict[Any, Any] | None,
        server: Optional[JsonRpcServer],
        app: Optional[JsonRpcApplication],
    ) -> tuple[JsonRpcResult | None, JsonRpcError | None] | None:
        if params is None:
            params = {}

        kwargs = {}

        if self.params_model is None:
            kwargs = params.copy()
        elif self.params_model is dict:
            kwargs["params"] = params
        else:
            try:
                kwargs["params"] = cast(
                    type[BaseModel], self.params_model
                ).model_validate(params)
            except Exception as e:
                return None, JsonRpcError(
                    code=JsonRpcErrorCode.InvalidParams,
                    message=f"Invalid parameters: {e}",
                )

        if self.include_server:
            kwargs["server"] = server
        if self.include_app:
            kwargs["app"] = app

        try:
            self.validate_func_args(**kwargs)
            return self.func(**kwargs)
        except Exception as e:
            return None, JsonRpcError(
                code=JsonRpcErrorCode.InvalidParams,
                message=f"Invalid parameters: {e}",
            )
