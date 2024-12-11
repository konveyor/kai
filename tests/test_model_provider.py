import unittest

from kai.llm_interfacing.model_provider import ModelProvider
from kai_solution_server.kai_config import KaiConfigModels


class TestModelProvider(unittest.TestCase):
    def test_fake_model_provider(self):
        responses = [
            "alfa",
            "beta",
            "charlie",
            "delta",
            "echo",
            "foxtrot",
            "golf",
            "hotel",
            "india",
        ]

        config = KaiConfigModels(
            provider="FakeListChatModel",
            args={
                "responses": responses,
                "sleep": 0.0,
            },
        )

        model_provider = ModelProvider(config)

        for x in responses:
            result = model_provider.llm.invoke("test").content
            print(f"{result} == {x}")
            assert result == x
