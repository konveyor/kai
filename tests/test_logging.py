import logging
import unittest
from pathlib import Path
from typing import cast

from kai.logging.logging import (
    KaiLogConfig,
    KaiLogger,
    get_logger,
    init_logging_from_log_config,
)


class TestLogging(unittest.TestCase):

    def test_logger_has_default(self) -> None:
        log = get_logger("testing")
        self.assertIsNotNone(log)

        from kai.logging.logging import log as base_logger

        self.assertIsNotNone(base_logger)
        base_logger = cast(KaiLogger, base_logger)

        self.assertEqual(log.getEffectiveLevel(), logging.NOTSET)
        self.assertTrue(isinstance(log, KaiLogger))
        self.assertEqual(log.configLogLevel, logging.NOTSET)
        self.assertEqual(base_logger.filters, log.filters)
        self.assertEqual(base_logger.handlers, log.handlers)

    def test_logger_init_updates_logs(self) -> None:
        config = KaiLogConfig(
            log_level="INFO",
            stderr_log_level="TRACE",
            file_log_level="INFO",
            log_dir_path=Path("./logs"),
            log_file_name="test.log",
        )

        print(config.log_dir_path)

        test_first_log = get_logger("child")

        init_logging_from_log_config(config)

        from kai.logging.logging import log as base_logger

        self.assertIsNotNone(base_logger)
        base_logger = cast(KaiLogger, base_logger)

        self.assertTrue(
            any(
                isinstance(handler, logging.FileHandler)
                for handler in base_logger.handlers
            )
        )
        self.assertTrue(
            any(
                isinstance(handler, logging.StreamHandler)
                for handler in base_logger.handlers
            )
        )

        test_second_log = get_logger("child2")

        self.assertTrue(isinstance(test_first_log, KaiLogger))
        self.assertEqual(test_first_log.level, logging.NOTSET)
        self.assertEqual(test_first_log.configLogLevel, base_logger.level)
        self.assertEqual(len(test_first_log.filters), 0)
        self.assertEqual(len(test_first_log.handlers), 0)
        self.assertTrue(isinstance(test_second_log, KaiLogger))
        self.assertEqual(test_second_log.level, logging.NOTSET)
        self.assertEqual(test_second_log.configLogLevel, base_logger.level)
        self.assertEqual(len(test_second_log.filters), 0)
        self.assertEqual(len(test_second_log.handlers), 0)
