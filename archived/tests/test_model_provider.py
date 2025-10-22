import os
import unittest

from kai.kai_config import KaiConfigModels, SupportedModelProviders
from kai.llm_interfacing.model_provider import ModelProvider


class TestModelProvider(unittest.IsolatedAsyncioTestCase):
    async def test_fake_model_provider(self) -> None:
        responses: list[str] = [
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
            provider=SupportedModelProviders.FAKE_LIST_CHAT_MODEL,
            args={
                "responses": responses,
                "sleep": 0.0,
            },
        )

        model_provider = ModelProvider.from_config(config)

        for x in responses:
            result = model_provider.llm.invoke("test").content
            print(f"{result} == {x}")
            assert result == x

    async def test_fail_if_improper_config(self) -> None:
        async def blank_provider(provider: str) -> ModelProvider:
            config = KaiConfigModels(
                provider=provider,  # type: ignore[arg-type]
                args={},
            )

            model = ModelProvider.from_config(config)
            await model.validate_environment()

            return model

        os.environ.clear()

        for provider in SupportedModelProviders:
            with self.subTest(provider=provider):
                print(f"Testing provider: {provider}")

                with self.assertRaises(Exception):  # trunk-ignore(ruff/B017)
                    if provider in [
                        "FakeListChatModel",
                    ]:
                        raise Exception()

                    await blank_provider(provider)

        os.environ["OPENAI_API_KEY"] = "obviously_fake"
        with self.assertRaises(Exception):  # trunk-ignore(ruff/B017)
            await blank_provider("ChatOpenAI")
        os.environ.clear()

        os.environ["AWS_SECRET_ACCESS_KEY"] = (  # trunk-ignore(bandit/B105)
            "obviously_fake"
        )
        os.environ["AWS_ACCESS_KEY_ID"] = "obviously_fake"
        with self.assertRaises(Exception):  # trunk-ignore(ruff/B017)
            await blank_provider("ChatBedrock")
        os.environ.clear()

        os.environ["GOOGLE_API_KEY"] = "obviously_fake"
        with self.assertRaises(Exception):  # trunk-ignore(ruff/B017)
            await blank_provider("ChatGoogleGenerativeAI")
        os.environ.clear()
