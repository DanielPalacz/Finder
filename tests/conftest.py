from __future__ import annotations

import os
import tempfile
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
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


# @pytest.fixture(autouse=True)
# def removes_log_files():
#     """Removes all log files"""
#
#     yield
#
#     directory = Path("logs")
#     log_files = [f for f in directory.iterdir() if f.is_file()]
#     for log_file in log_files:
#         log_file.unlink()


@pytest.fixture
def removes_result_test_files():
    """Removes all log files"""

    yield

    result_file = Path("tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")
    result_file.unlink()


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


@pytest.fixture()
def mock_db_filepath():
    """Creates log file if not exists"""
    return abspath((dirname(__file__))) + "/fixtures/MOCK_DB.csv"


@pytest.fixture()
def mock_company_html():
    """Provides mocked content of company html"""
    mocked_company_website_path = abspath((dirname(__file__))) + "/fixtures/MOCK_COMPANY_WEBSITE.html"
    with open(mocked_company_website_path, "r") as file:
        return file.read()


@pytest.fixture()
def setup_www_page(mock_company_html):
    """Maintains simple www server"""

    # Define a simple request handler class
    class WebRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Send a response header
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Send some content
            self.wfile.write(mock_company_html.encode())

    # Start server in a separate thread
    def start_server(server_http):
        # print("Server is running...")
        server_http.serve_forever()

    # Create and start the HTTPServer
    def run_server():
        server_object = HTTPServer(("0.0.0.0", 9999), WebRequestHandler)

        # Create a thread to run the server
        server_thread_object = threading.Thread(target=start_server, args=(server_object,), daemon=True)
        server_thread_object.start()

        return server_object, server_thread_object

    def stop_server(server_http):
        # print("Shutting down the server...")
        server_http.shutdown()
        server_http.server_close()

    server, server_thread = run_server()

    yield

    stop_server(server)
