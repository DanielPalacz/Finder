from __future__ import annotations

import functools
import os
import signal
import threading
from os.path import dirname

from flask import Flask

from config import CRAWLED_JOBS_OUTPUT_FILE
from config import JOB_ROLES

app = Flask(__name__)


def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Flask App</title>
        </head>
        <body>
            <h1>Hello!</h1>
            <p>This simple Web app allow you to use following two endpoints:</>
            <ul>
                <li><a href="/logs">/logs</a> - displaying latest logs</li>
                <li><a href="/results">/results</a> - displaying all results collected till now</li>
                <li><a href="/jobs_definition">/jobs_definition</a> - displaying job keywords used for Job Search</li>
            </ul>
        </body>
    </html>
    """


def tail(file_path, lines=10):
    with open(file_path, "rb") as file:
        file.seek(0, 2)  # Go to the end of the file
        file_size = file.tell()  # Get the file size

        buffer_size = 1024
        buffer = b""
        line_count = 0

        while file_size > 0 and line_count < lines:
            read_size = min(buffer_size, file_size)  # Read in chunks
            file_size -= read_size
            file.seek(file_size)
            buffer = file.read(read_size) + buffer

            # Count the number of newlines in the buffer
            line_count = buffer.count(b"\n")

        # Decode the buffer and split it into lines
        all_lines = buffer.decode(errors="ignore").splitlines()

        # Return the last `lines` lines
        return all_lines[-lines:]


def logs():
    try:
        log_filepath = dirname(__file__) + "/logs/JobScanner.log"
        tailed_lines = tail(log_filepath)
    except FileNotFoundError:
        return "There is no logs."
    tailed_lines_str = "\n".join(tailed_lines)
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Flask App</title>
        </head>
        <body>
            <pre>{tailed_lines_str}</pre>
        </body>
    </html>
    """


def results():
    try:
        output_str = ""
        line_counter = 0
        with open(CRAWLED_JOBS_OUTPUT_FILE, "r") as output_file:
            for line in output_file:
                line_counter += 1
                output_str += f"line{line_counter};{line}"
    except FileNotFoundError:
        return "There is no output file."

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Flask App</title>
        </head>
        <body>
            <pre>{output_str}</pre>
        </body>
    </html>
    """


def jobs_definition():
    output_str = "List of job definitions keywords / rules used for job search:"
    line_counter = 0
    for job_def in JOB_ROLES:
        line_counter += 1
        output_str += f"\n - {job_def}"
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Flask App</title>
        </head>
        <body>
            <pre>{output_str}</pre>
        </body>
    </html>
    """


app.add_url_rule("/", view_func=home, methods=("GET",))
app.add_url_rule("/logs", view_func=logs, methods=("GET",))
app.add_url_rule("/results", view_func=results, methods=("GET",))
app.add_url_rule("/jobs_definition", view_func=jobs_definition, methods=("GET",))


def run_flask_monitoring_api(f):
    """Decorator function running flask api during other function execution"""

    @functools.wraps(f)
    def function_wrapper(*args, **kwargs):
        # Create a flask api separate thread
        flask_thread_object = threading.Thread(  # nosec
            target=app.run,  # nosec
            kwargs={"debug": False, "use_reloader": False, "host": "0.0.0.0", "port": 7777},  # nosec
            daemon=True,  # nosec
        )
        flask_thread_object.start()

        results_f = f(*args, **kwargs)

        def signal_handler(sig, frame):
            print("\nCTRL+C caught in signal handler!")
            os._exit(0)  # Exit the program

        # Register the signal handler for SIGINT
        signal.signal(signal.SIGINT, signal_handler)
        os.kill(os.getpid(), signal.SIGINT)

        return results_f

    return function_wrapper


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=7777)  # nosec
    # app.run(debug=True, use_reloader=True, host='0.0.0.0', port=7777)
