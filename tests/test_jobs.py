from __future__ import annotations

from os.path import dirname
from time import sleep

import pytest
import requests

from jobs import JobScanner


def test_job_scanner_initiate_object():
    assert JobScanner()


def test_job_scanner_run(monkeypatch, mock_db_filepath, setup_www_page, removes_result_test_files):
    monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (python)"])
    monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    assert JobScanner().run() is None
    sleep(1)  # this is tricky case, from some reason without that - requests are failing (threading ..)

    result_file = dirname(__file__) + "/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv"

    with open(result_file, "r") as file_result:
        result_content = file_result.read()
        assert result_content == (
            '"FIRMA 1" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ;101;brak_email;'
            "http://127.0.0.1:9999/;małopolskie;Borsucza,16,Kraków,30-40-408,Kraków,Polska;"
            "http://127.0.0.1:9999/\n"
        )


def test_job_scanner_run_not_found_job(monkeypatch, mock_db_filepath, setup_www_page):
    monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (unknown)"])
    monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    assert JobScanner().run() is None
    sleep(1)  # this is tricky case, from some reason without that - requests are failing (threading ..)

    result_file = dirname(__file__) + "/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv"

    with pytest.raises(FileNotFoundError):
        with open(result_file, "r"):
            pass


def test_job_scanner_career_keywords():
    assert JobScanner.CAREER_KEYWORDS == [
        "career",
        "careers",
        "jobs",
        "job",
        "work-with-us",
        "join-us",
        "recruitment",
        "about/careers",
        "team",
        "opportunities",
        "vacancies",
        "openings",
        "positions",
        "talent",
        "join-our-team",
        "apply",
        "hiring",
        "internships",
        "engineering-jobs",
        "kariera",
        "praca",
        "oferty-pracy",
        "rekrutacja",
        "dolacz-do-nas",
        "aplikuj",
        "praktyki",
        "praca-w-it",
        "poznaj-nas",
        "vacancy",
        "praca",
        "staz",
        "pracy",
        "ogłoszenia",
        "ogloszenia",
    ]


def test_job_scanner_fetch(monkeypatch, mock_db_filepath, setup_www_page):
    monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (python)"])
    monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    assert isinstance(www_response, requests.models.Response)
    assert www_response.status_code == 200

    #
    # with open(mock_db_filepath, "r") as file_result:
    #     result_content = file_result.read()

    assert "Firma XYZ to lider w dostarczaniu innowacyjnych" in www_response.text
