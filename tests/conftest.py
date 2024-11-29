from __future__ import annotations

import os
import tempfile
from datetime import datetime
from os.path import abspath
from os.path import dirname
from pathlib import Path

import pytest


@pytest.fixture
def t_file():
    """Create a temporary file"""

    db_fd, db_path = tempfile.mkstemp()

    yield db_path

    # close and remove the temporary file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def timestamp():
    """Provides timestamp text"""
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M%S")
    return year + month + day + "_" + time


@pytest.fixture
def removes_log_files():
    """Removes all log files"""

    yield

    directory = Path("logs")
    log_files = [f for f in directory.iterdir() if f.is_file()]
    for log_file in log_files:
        log_file.unlink()


@pytest.fixture()
def logs_directory():
    """Creates log file if not exists"""
    return abspath(dirname(dirname(__file__))) + "/logs"


@pytest.fixture(autouse=True)
def check_if_logs_directory_exists(logs_directory):
    """Creates log file if not exists"""
    try:
        os.mkdir(logs_directory)
    except FileExistsError:
        pass
