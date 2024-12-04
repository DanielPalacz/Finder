from os.path import dirname

from flask import Flask

from config import CRAWLED_JOBS_OUTPUT_FILE

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




app.add_url_rule("/", view_func=home, methods=("GET",))
app.add_url_rule("/logs", view_func=logs, methods=("GET",))
app.add_url_rule("/results", view_func=results, methods=("GET",))

if __name__ == "__main__":
    pass
    # app.run(debug=True, use_reloader=True, host='0.0.0.0', port=7777)
    # app.run(debug=True, use_reloader=True, host='0.0.0.0', port=7777)
