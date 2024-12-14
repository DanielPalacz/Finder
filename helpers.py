from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from os import getenv
from typing import Generator
from typing import Optional
from typing import TypeAlias

from configuration.config import DB_FILEPATH


LoggerT: TypeAlias = logging.Logger


def configure_logger(logger_name: str) -> LoggerT:
    """Configures logger.

    Uses env variable LOG_LEVEL_NAME:
     - CRITICAL = 50
     - FATAL = 50
     - ERROR = 40
     - WARNING = 30
     - INFO = 20
     - DEBUG = 10

    Args:
        logger_name: Logger name.

    Returns:
        Logger object.
    """
    log_level_matrix = {"CRITICAL": 50, "FATAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10}

    log_level_name = getenv("LOG_LEVEL_NAME") or "DEBUG"
    log_level_value = log_level_matrix[log_level_name]

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level_value)
    logger_handler = RotatingFileHandler(f"logs/{logger_name}.log", maxBytes=100 * 1024 * 1024, backupCount=20)
    logger_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger


def iterate_over_csv_db_file(db_filepath: Optional[str] = None) -> Generator[list[str]]:
    """Iterates line-after-line over content of DB file

    Uses DB with default file name: DB_FILENAME

    Yields:
        list: line content split to list as following:
              [line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address]
    """
    if db_filepath is None:
        db_filepath = DB_FILEPATH

    with open(db_filepath, "r") as companies_file:
        for line in companies_file:
            split_line = line.replace("\n", "").split(";")
            # line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = split_line
            yield split_line
