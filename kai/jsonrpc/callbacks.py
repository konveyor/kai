from __future__ import annotations

import functools
import inspect
import traceback
from typing import TYPE_CHECKING, Any, Callable, Literal, get_origin

from pydantic import BaseModel, ConfigDict, validate_call

from kai.jsonrpc.models import JsonRpcError, JsonRpcErrorCode, JsonRpcRequest
from kai.logging.logging import TRACE, get_logger

if TYPE_CHECKING:
    from kai.jsonrpc.core import JsonRpcApplication, JsonRpcServer


log = get_logger("jsonrpc")

# JsonRpcCallable = Callable[[JsonRpcApplication, JsonRpcServer, JsonRpcId, JsonRpcRequestParams], None]
JsonRpcCallable = Callable[..., None]


class JsonRpcCallback:
    """
    A JsonRpcCallback is a wrapper around a JsonRpcMethodCallable or
    JsonRpcNotifyCallable. It validates the parameters and calls the function.

    We use this class to allow for more flexibility in the parameters that can
    be passed to the function.
    """

    def __init__(
        self,
        func: JsonRpcCallable,
        kind: Literal["request", "notify"],
        method: str,
    ):
        self.func = func
        self.kind = kind
        self.method = method

        @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
        @functools.wraps(self.func)
        def validate_func_args(
            *args: Any, **kwargs: Any
        ) -> tuple[tuple[Any, ...], dict[str, Any]]:
            return args, kwargs

        self.validate_func_args = validate_func_args

        sig = inspect.signature(func)
        self.params_model: type[dict[str, Any]] | type[BaseModel] | None = [
            get_origin(p.annotation) for p in sig.parameters.values()
        ][3]

    def __call__(
        self,
        app: JsonRpcApplication,
        server: JsonRpcServer,
        request: JsonRpcRequest,
    ) -> None:
        try:
            log.log(TRACE, f"{self.func.__name__} called with {request}")
            log.log(
                TRACE,
                f"{[(p.annotation) for p in inspect.signature(self.func).parameters.values()]}",
            )

            validated_params: BaseModel | dict[str, Any] | None

            if request.params is None:
                if self.params_model is not None:
                    raise ValueError("Expected params to be present")
                else:
                    validated_params = None
            elif isinstance(request.params, dict):
                if self.params_model is None:
                    raise ValueError("Expected params to be None")
                elif self.params_model is dict:
                    validated_params = request.params
                elif issubclass(self.params_model, BaseModel):
                    validated_params = self.params_model.model_validate(request.params)
                else:
                    raise ValueError(
                        f"params_model should be dict | BaseModel | None, got {self.params_model}"
                    )
            else:
                raise ValueError(
                    f"Expected params to be a dict or None, got {type(request.params)}"
                )

            log.log(TRACE, f"Validated params: {validated_params}")
            self.validate_func_args(app, server, request.id, validated_params)

            log.log(TRACE, f"Calling function: {self.func.__name__}")
            self.func(app, server, request.id, validated_params)
        except Exception:
            server.send_response(
                id=request.id,
                error=JsonRpcError(
                    code=JsonRpcErrorCode.InternalError,
                    message=traceback.format_exc(),
                ),
            )
