import sys
from pathlib import Path
from typing import Optional

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


@KAI_RPC_SERVER.add_method(method="shutdown")
def shutdown():
    return {}, None


@KAI_RPC_SERVER.add_method(method="exit")
def exit():
    return {}, None


@KAI_RPC_SERVER.add_method(method="initialize", model=KaiRpcServerConfig)
def initialize(config: KaiRpcServerConfig):
    return {}, None


@KAI_RPC_SERVER.add_method(method="setConfig")
def set_config(config: KaiRpcServerConfig):
    return {}, None


@KAI_RPC_SERVER.add_method(method="getRAGSolution")
def get_rag_solution():
    return {}, None


@KAI_RPC_SERVER.add_method(method="getCodeplanAgentSolution")
def get_codeplan_agent_solution():
    return {}, None
