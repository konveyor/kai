import os
import unittest

from kai.kai_config import KaiConfigModels, SupportedModelProviders
from kai.llm_interfacing.model_provider import ModelProvider


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

    def test_fail_if_improper_config(self) -> None:
        os.environ.clear()

        for provider in SupportedModelProviders:
            with self.subTest(provider=provider):
                print(f"Testing provider: {provider}")

                with self.assertRaises(Exception):  # trunk-ignore(ruff/B017)
                    if provider in [
                        "FakeListChatModel",
                    ]:
                        raise Exception()

                    ModelProvider(
                        KaiConfigModels(
                            provider=provider,
                            args={},
                        ),
                    )
