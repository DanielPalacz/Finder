from __future__ import annotations

import requests


def test_flask_api_endpoints_home(setup_flask_api):
    flask_api_www = setup_flask_api
    assert requests.get(flask_api_www).status_code == 200


def test_flask_api_endpoints_logs(setup_flask_api):
    flask_api_www = setup_flask_api + "logs"
    assert requests.get(flask_api_www).status_code == 200


def test_flask_api_endpoints_results(setup_flask_api):
    flask_api_www = setup_flask_api + "results"
    assert requests.get(flask_api_www).status_code == 200


def test_flask_api_endpoints_jobs_definition(setup_flask_api):
    flask_api_www = setup_flask_api + "jobs_definition"
    assert requests.get(flask_api_www).status_code == 200


def test_flask_api_endpoints_home_content(setup_flask_api):
    flask_api_www = setup_flask_api
    assert (
        requests.get(flask_api_www).text
        == """
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
    )
