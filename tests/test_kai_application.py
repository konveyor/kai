import unittest
from unittest.mock import MagicMock, patch

import aiohttp.web as web

from kai.server.service.incident_store.sql_types import SQLIncident
from kai.server.service.kai_application.kai_application import (
    KaiApplication,
    UpdatedFileContent,
)
from kai.shared.models.kai_config import KaiConfig
from kai.shared.models.report_types import ExtendedIncident


class TestKaiApplication(unittest.TestCase):

    @patch(
        "kai.server.service.kai_application.kai_application.incident_store_backend_factory"
    )
    @patch(
        "kai.server.service.kai_application.kai_application.solution_detection_factory"
    )
    @patch(
        "kai.server.service.kai_application.kai_application.solution_producer_factory"
    )
    @patch(
        "kai.server.service.kai_application.kai_application.solution_consumer_factory"
    )
    @patch("kai.server.service.kai_application.kai_application.ModelProvider")
    def setUp(
        self,
        MockModelProvider,
        mock_solution_consumer_factory,
        mock_solution_producer_factory,
        mock_solution_detection_factory,
        mock_incident_store_backend_factory,
    ):
        self.mock_model_provider = MockModelProvider.return_value
        self.mock_incident_store_backend = (
            mock_incident_store_backend_factory.return_value
        )
        self.mock_solution_detector = mock_solution_detection_factory.return_value
        self.mock_solution_producer = mock_solution_producer_factory.return_value
        self.mock_solution_consumer = mock_solution_consumer_factory.return_value

        self.config = KaiConfig.model_construct(
            log_level="info",
            trace_enabled=False,
            demo_mode=False,
            models=MagicMock(),
            incident_store=MagicMock(),
            solution_consumers=MagicMock(),
        )
        self.app = KaiApplication(self.config)
        self.app.incident_store.backend.json_exactly_equal.return_value = (
            SQLIncident.solution_id.isnot(None)
        )

    @patch(
        "kai.server.service.kai_application.kai_application.UpdatedFileContent",
        wraps=UpdatedFileContent.model_construct,
    )
    @patch("kai.server.service.kai_application.kai_application.guess_language")
    @patch("kai.server.service.kai_application.kai_application.batch_incidents")
    @patch("kai.server.service.kai_application.kai_application.get_prompt")
    @patch("kai.server.service.kai_application.kai_application.playback_if_demo_mode")
    @patch(
        "kai.server.service.kai_application.kai_application.parse_file_solution_content"
    )
    def test_get_incident_solutions_for_file(
        self,
        mock_parse_file_solution_content,
        mock_playback_if_demo_mode,
        mock_get_prompt,
        mock_batch_incidents,
        mock_guess_language,
        mock_updated_file_content,
    ):
        mock_guess_language.return_value = "python"
        mock_batch_incidents.return_value = [(None, [MagicMock()])]
        mock_get_prompt.return_value = "mock_prompt"
        mock_parse_file_solution_content.return_value = MagicMock(
            updated_file="mock_updated_file",
            reasoning="mock_reasoning",
            additional_info="mock_additional_info",
        )

        file_name = "test.py"
        file_contents = 'print("Hello, world!")'
        application_name = "test_app"
        incidents = [
            ExtendedIncident(
                uri="uri",
                message="message",
                ruleset_name="ruleset_name",
                violation_name="violation_name",
            )
        ]
        result = self.app.get_incident_solutions_for_file(
            file_name, file_contents, application_name, incidents
        )

        self.assertIsInstance(result, UpdatedFileContent)
        self.assertEqual(result.updated_file, "mock_updated_file")
        self.assertEqual(result.total_reasoning, ["mock_reasoning"])
        self.assertEqual(result.additional_information, ["mock_additional_info"])
        self.assertEqual(result.used_prompts, ["mock_prompt"])

    @patch(
        "kai.server.service.kai_application.kai_application.UpdatedFileContent",
        wraps=UpdatedFileContent.model_construct,
    )
    @patch("kai.server.service.kai_application.kai_application.guess_language")
    @patch("kai.server.service.kai_application.kai_application.batch_incidents")
    @patch("kai.server.service.kai_application.kai_application.get_prompt")
    @patch("kai.server.service.kai_application.kai_application.playback_if_demo_mode")
    @patch(
        "kai.server.service.kai_application.kai_application.parse_file_solution_content"
    )
    def test_get_incident_solutions_for_file_with_llm_failure(
        self,
        mock_parse_file_solution_content,
        mock_playback_if_demo_mode,
        mock_get_prompt,
        mock_batch_incidents,
        mock_guess_language,
        mock_updated_file_content,
    ):
        mock_guess_language.return_value = "python"
        mock_batch_incidents.return_value = [(None, [MagicMock()])]
        mock_get_prompt.return_value = "mock_prompt"
        mock_parse_file_solution_content.side_effect = Exception("LLM error")

        file_name = "test.py"
        file_contents = 'print("Hello, world!")'
        application_name = "test_app"
        incidents = [
            ExtendedIncident(
                uri="uri",
                message="message",
                ruleset_name="ruleset_name",
                violation_name="violation_name",
            )
        ]

        with self.assertRaises(web.HTTPInternalServerError):
            self.app.get_incident_solutions_for_file(
                file_name, file_contents, application_name, incidents
            )


if __name__ == "__main__":
    unittest.main()

"""
import unittest
from unittest.mock import patch

PKG = "kai.server.service.kai_application.kai_application"

class TestKaiApplicationMocked(unittest.TestCase):
    
    def add_mock(self, target: str):
        patcher = patch(target)
        self.addCleanup(patcher.stop)
        return patcher.start()
    
    def setUp(self):
        self.config = MagicMock(spec=KaiConfig)
        self.config.log_level = "DEBUG"
        self.config.trace_enabled = True
        self.config.demo_mode = False
        self.config.models = MagicMock()
        self.config.incident_store = MagicMock()
        self.config.solution_consumers = MagicMock()
    
        self.mock_model_provider = self.add_mock(f"{PKG}.ModelProvider")
        
        self.mock_incident_store_backend_factory = self.add_mock(f"{PKG}.incident_store_backend_factory")
        self.mock_solution_detection_factory = self.add_mock(f"{PKG}.solution_detection_factory")
        self.mock_solution_producer_factory = self.add_mock(f"{PKG}.solution_producer_factory")
        
        self.mock_solution_consumer_factory = self.add_mock(f"{PKG}.solution_consumer_factory")

        self.app = KaiApplication(self.config)

        print(self.app.incident_store.backend)

    @patch('kai.server.service.kai_application.kai_application.UpdatedFileContent')
    @patch('kai.server.service.kai_application.kai_application.ModelProvider')
    @patch('kai.server.service.kai_application.kai_application.guess_language', return_value='python')
    @patch('kai.server.service.kai_application.kai_application.parse_file_solution_content')
    @patch('kai.server.service.kai_application.kai_application.get_prompt', return_value='mock_prompt')
    @patch('kai.server.service.kai_application.kai_application.batch_incidents', return_value=[({}, [ExtendedIncident(uri="uri", message="message", ruleset_name="ruleset_name", violation_name="violation_name")])])
    @patch('kai.server.service.kai_application.kai_application.playback_if_demo_mode')
    def test_get_incident_solutions_for_file(
        self,
        mock_playback_if_demo_mode,
        mock_batch_incidents,
        mock_get_prompt,
        mock_parse_file_solution_content,
        mock_guess_language,
        mock_model_provider,
        mock_updated_file_content,
    ):
        mock_llm_result = MagicMock()
        mock_llm_result.content = 'mock_llm_result_content'
        
        self.app.model_provider.llm = MagicMock()
        self.app.model_provider.llm.invoke.return_value = mock_llm_result
        
        mock_parse_file_solution_content.return_value = MagicMock(updated_file='updated_file_content', reasoning='reasoning', additional_info='additional_info')

        incidents = [ExtendedIncident(
            uri="uri",
            message="message",
            ruleset_name="ruleset_name",
            violation_name="violation_name"
        )]
        result = self.app.get_incident_solutions_for_file(
            file_name='test_file.py',
            file_contents='print("Hello, world!")',
            application_name='test_app',
            incidents=incidents
        )

        self.assertEqual(result.updated_file, 'updated_file_content')
        self.assertEqual(result.total_reasoning, ['reasoning'])
        self.assertEqual(result.used_prompts, ['mock_prompt'])
        self.assertEqual(result.additional_information, ['additional_info'])
        self.assertEqual(result.llm_results, [])

        mock_guess_language.assert_called_once_with('print("Hello, world!")', filename='test_file.py')
        mock_get_prompt.assert_called_once()
        mock_playback_if_demo_mode.assert_called_once()
        self.app.model_provider.llm.invoke.assert_called_once_with('mock_prompt')



# @unittest.skip("Skip until tests are verified")
class TestKaiApplication(unittest.TestCase):

    def setUp(self):
        self.config = MagicMock(spec=KaiConfig)
        self.config.log_level = 'DEBUG'
        self.config.trace_enabled = False
        self.config.demo_mode = False
        self.config.models = MagicMock()
        self.config.incident_store = MagicMock()
        self.config.solution_consumers = MagicMock()
        
        self.app = KaiApplication(self.config)
    


    @patch('kai.server.service.kai_application.kai_application.ModelProvider')
    @patch('kai.server.service.kai_application.kai_application.guess_language', return_value='python')
    @patch('kai.server.service.kai_application.kai_application.parse_file_solution_content')
    @patch('kai.server.service.kai_application.kai_application.get_prompt', return_value='mock_prompt')
    @patch('kai.server.service.kai_application.kai_application.batch_incidents', return_value=[({}, [ExtendedIncident(uri="uri", message="message", ruleset_name="ruleset_name", violation_name="violation_name")])])
    @patch('kai.server.service.kai_application.kai_application.playback_if_demo_mode')
    def test_get_incident_solutions_for_file(
        self,
        mock_playback_if_demo_mode,
        mock_batch_incidents,
        mock_get_prompt,
        mock_parse_file_solution_content,
        mock_guess_language,
        mock_model_provider
    ):
        mock_llm_result = MagicMock()
        mock_llm_result.content = 'mock_llm_result_content'
        self.app.model_provider.llm = MagicMock()
        self.app.model_provider.llm.invoke.return_value = mock_llm_result
        mock_parse_file_solution_content.return_value = MagicMock(updated_file='updated_file_content', reasoning='reasoning', additional_info='additional_info')

        incidents = [ExtendedIncident()]
        result = self.app.get_incident_solutions_for_file(
            file_name='test_file.py',
            file_contents='print("Hello, world!")',
            application_name='test_app',
            incidents=incidents
        )

        self.assertEqual(result.updated_file, 'updated_file_content')
        self.assertEqual(result.total_reasoning, ['reasoning'])
        self.assertEqual(result.used_prompts, ['mock_prompt'])
        self.assertEqual(result.additional_information, ['additional_info'])
        self.assertEqual(result.llm_results, [])

        mock_guess_language.assert_called_once_with('print("Hello, world!")', filename='test_file.py')
        mock_get_prompt.assert_called_once()
        mock_playback_if_demo_mode.assert_called_once()
        self.app.model_provider.llm.invoke.assert_called_once_with('mock_prompt')

    @patch('kai.server.service.kai_application.kai_application.solution_detection_factory')
    @patch('kai.server.service.kai_application.kai_application.solution_consumer_factory')
    def test_kai_application_initialization(self, mock_solution_consumer_factory, mock_solution_detection_factory):
        config = KaiConfig(
            log_level='DEBUG',
            trace_enabled=True,
            demo_mode=False,
            models=MagicMock(),
            incident_store=MagicMock(),
            solution_consumers=MagicMock(),
        )
        app = KaiApplication(config)
        self.assertEqual(app.config, config)
        self.assertIsInstance(app.model_provider, MagicMock)
        self.assertIsInstance(app.incident_store, MagicMock)
        self.assertIsInstance(app.solution_consumer, MagicMock)

    @patch('kai.server.service.kai_application.kai_application.time.sleep', return_value=None)
    @patch('kai.server.service.kai_application.kai_application.KAI_LOG.error')
    def test_get_incident_solutions_for_file_retry_failure(self, mock_log_error, mock_time_sleep):
        self.app.model_provider.llm.invoke.side_effect = Exception("LLM Error")

        with self.assertRaises(web.HTTPInternalServerError):
            self.app.get_incident_solutions_for_file(
                file_name='test_file.py',
                file_contents='print("Hello, world!")',
                application_name='test_app',
                incidents=[ExtendedIncident()]
            )

        mock_log_error.assert_called_once()
        self.assertEqual(self.app.model_provider.llm.invoke.call_count, self.app.model_provider.llm_retries)

    @patch('kai.server.service.kai_application.kai_application.KAI_LOG.debug')
    @patch('kai.server.service.kai_application.kai_application.KAI_LOG.warn')
    def test_get_incident_solutions_for_file_retry_success(self, mock_log_warn, mock_log_debug):
        mock_llm_result = MagicMock()
        mock_llm_result.content = 'mock_llm_result_content'
        self.app.model_provider.llm.invoke.side_effect = [Exception("LLM Error"), mock_llm_result]

        result = self.app.get_incident_solutions_for_file(
            file_name='test_file.py',
            file_contents='print("Hello, world!")',
            application_name='test_app',
            incidents=[ExtendedIncident()]
        )

        self.assertEqual(result.updated_file, 'mock_llm_result_content')
        self.assertEqual(self.app.model_provider.llm.invoke.call_count, 2)
        mock_log_warn.assert_called_once()
        mock_log_debug.assert_called()

if __name__ == '__main__':
    unittest.main()
"""
