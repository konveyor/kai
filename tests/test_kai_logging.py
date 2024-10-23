import logging
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from kai.kai_config import KaiConfig, KaiConfigIncidentStore, KaiConfigModels
from kai.logging.logging import (
    init_logging,
    init_logging_from_config,
    process_log_dir_replacements,
    setup_console_handler,
    setup_file_handler,
)


class TestLoggingSetup(unittest.TestCase):
    def setUp(self):
        self.test_log_dir = tempfile.mkdtemp()
        self.console_log_level = "INFO"
        self.file_log_level = "DEBUG"
        self.log_file = "kai_server.log"
        self.log_dir_with_placeholder = "$pwd/logs"

        # Mock KaiConfig
        self.config = MagicMock(spec=KaiConfig)
        self.config.log_level = self.console_log_level
        self.config.file_log_level = self.file_log_level
        self.config.log_dir = self.log_dir_with_placeholder
        self.config.incident_store = MagicMock(spec=KaiConfigIncidentStore)
        self.config.models = KaiConfigModels(
            provider="FakeProvider",
            args={},
        )
        self.config.solution_consumers = []

    def tearDown(self):
        shutil.rmtree(self.test_log_dir)

    @patch("os.getcwd")
    def test_process_log_dir_replacements(self, mock_getcwd):
        mock_cwd = os.path.dirname(os.path.abspath(__file__))
        mock_getcwd.return_value = mock_cwd
        actual_log_dir = process_log_dir_replacements(self.config.log_dir)
        expected_log_dir = os.path.abspath(os.path.join(mock_cwd, "logs"))
        self.assertEqual(expected_log_dir, actual_log_dir)

    @patch("logging.StreamHandler")
    def test_setup_console_handler(self, mock_stream_handler):
        logger = logging.getLogger("test_console_logger")
        setup_console_handler(logger, self.console_log_level)
        mock_stream_handler.assert_called_once()
        handler_instance = mock_stream_handler.return_value
        handler_instance.setLevel.assert_called_once_with(self.console_log_level)
        handler_instance.setFormatter.assert_called_once()

    @patch("logging.FileHandler")
    @patch("os.makedirs")
    def test_setup_file_handler(self, mock_makedirs, mock_file_handler):
        logger = logging.getLogger("test_file_logger")
        setup_file_handler(
            logger, self.log_file, self.log_dir_with_placeholder, self.file_log_level
        )
        expected_log_dir = process_log_dir_replacements(self.log_dir_with_placeholder)
        mock_makedirs.assert_called_once_with(expected_log_dir, exist_ok=True)
        expected_log_file_path = os.path.join(expected_log_dir, self.log_file)
        mock_file_handler.assert_called_once_with(expected_log_file_path)
        handler_instance = mock_file_handler.return_value
        handler_instance.setLevel.assert_called_once_with(self.file_log_level)
        handler_instance.setFormatter.assert_called_once()

    def test_init_logging(self):
        init_logging(
            self.console_log_level,
            self.file_log_level,
            self.test_log_dir,
            self.log_file,
        )
        logger = logging.getLogger("kai")
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(
            any(
                isinstance(handler, logging.StreamHandler)
                for handler in logger.handlers
            )
        )
        self.assertTrue(
            any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)
        )

    @patch("os.makedirs")
    @patch("os.getcwd")
    def test_init_logging_from_config(self, mock_getcwd, mock_makedirs):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mock_getcwd.return_value = base_dir
        expected_log_dir = os.path.join(base_dir, "logs")
        init_logging_from_config(self.config)

        mock_makedirs.assert_called_once_with(expected_log_dir, exist_ok=True)

        logger = logging.getLogger("kai")
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(
            any(
                isinstance(handler, logging.StreamHandler)
                for handler in logger.handlers
            )
        )
        self.assertTrue(
            any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)
        )


if __name__ == "__main__":
    unittest.main()
