from __future__ import annotations

import os.path

from helpers import configure_logger


def test_configure_logger_check_logger_name(timestamp, removes_log_files):
    logger_name = f"TestLogger_{timestamp}"
    logger = configure_logger(logger_name)

    assert logger.name == logger_name


def test_configure_logger_check_logger_file(timestamp, removes_log_files, logs_directory):
    logger_name = f"TestLogger_{timestamp}"
    logger = configure_logger(logger_name)
    loger_filepath = f"{logs_directory}/{logger_name}.log"
    logger.info("It is test log item.")
    assert os.path.exists(loger_filepath)

    with open(loger_filepath, "r") as f:
        text = f.read()
        assert " - INFO - It is test log item." in repr(text)
