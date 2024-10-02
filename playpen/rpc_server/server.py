import sys
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock

from pydantic import BaseModel

from kai.service.llm_interfacing.model_provider import ModelProvider
from playpen.rpc_server.rpc import JsonRpcServer, LspStyleStream

KAI_RPC_SERVER = JsonRpcServer(
    LspStyleStream(sys.stdin.buffer, sys.stdout.buffer),
)


class KaiRpcServerConfig(BaseModel):
    processId: Optional[int]

    rootUri: str
    kantraUri: str
    modelProvider: ModelProvider
    kaiBackendUrl: str

    logLevel: Optional[str] = None
    fileLogLevel: Optional[str] = None
    logDirUri: Optional[Path] = None


class CodeplanState:
    def __init__(self):
        self.initialized = False
        self.config: Optional[KaiRpcServerConfig] = None


@KAI_RPC_SERVER.add_method(method="initialize", model=KaiRpcServerConfig)
def initialize(config: KaiRpcServerConfig):
    return {}, None
