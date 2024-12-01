from __future__ import annotations

from os.path import dirname
from time import sleep

import pytest
import requests

from jobs import JobScanner


def test_job_scanner_initiate_object():
    assert JobScanner()
    assert JobScanner().logger.name == "JobScanner"


def test_job_scanner_run_www_check_for_the_needed_jobs(
    monkeypatch, mock_db_filepath, setup_www_page, removes_result_test_files
):
    monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (python)"])
    monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    url_fixture_link = "http://127.0.0.1:9999/"

    company_data = [
        "1",
        '"FIRMA 1" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
        "101",
        "['ZARZĄDZANIE NIERUCHOMOŚCIAMI WYKONYWANE NA ZLECENIE', '68', '32', 'Z']",
        "[{'opis': 'DZIAŁALNOŚĆ POMOCNICZA ZWIĄZANA Z UTRZYMANIEM PORZĄDKU W BUDYNKACH', "
        "'kodDzial': '81', 'kodKlasa': '10', 'kodPodklasa': 'Z'}]",
        "brak_email",
        "http://127.0.0.1:9999/",
        "małopolskie",
        "Borsucza,16,Kraków,30-40-408,Kraków,Polska",
    ]

    JobScanner()._run_www_check_for_the_needed_jobs(url_fixture_link, ["python"], company_data)
    result_file = dirname(__file__) + "/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv"

    with open(result_file, "r") as file_result:
        result_content = file_result.read()
        assert result_content == (
            '"FIRMA 1" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ;101;brak_email;'
            "http://127.0.0.1:9999/;małopolskie;Borsucza,16,Kraków,30-40-408,Kraków,Polska;"
            "http://127.0.0.1:9999/#careers\n"
        )


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
            "http://127.0.0.1:9999/#careers\n"
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


def test_job_scanner_fetch_non_existing_www(monkeypatch, mock_db_filepath):
    monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (python)"])
    monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    assert www_response is None


def test_job_scanner_fetch_ssl_issue_www(monkeypatch, mock_db_filepath, logs_directory):
    def get_raising_ssl_error(url, allow_redirects=True, timeout=5):
        raise requests.exceptions.SSLError("There is SSL issue.")

    monkeypatch.setattr("jobs.requests.get", get_raising_ssl_error)

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    assert www_response is None

    with open(f"{logs_directory}/{job_scanner.logger.name}.log", "r") as log_file:
        for log_line in log_file:
            pass
        else:
            if (
                "ERROR - Returning None, because something went wrong with request execution (http://127.0.0.1:9999/). "
                "Details: SSLError('There is SSL issue.') [backup http flow]"
            ) in log_line:
                return None
        raise AssertionError("Incorrect log text. It should confirm that SSL issue was handled with backup http flow.")


def test_job_scanner_fetch_value_error_www(monkeypatch, mock_db_filepath):
    def get_raising_ssl_error(url, allow_redirects=True, timeout=5):
        raise ValueError("There is strange value error issue.")

    monkeypatch.setattr("jobs.requests.get", get_raising_ssl_error)

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    assert www_response is None


def test_job_scanner_extract_links(monkeypatch, mock_db_filepath, setup_www_page):
    # monkeypatch.setattr("helpers.DB_FILEPATH", mock_db_filepath)
    # monkeypatch.setattr("jobs.JOB_ROLES", ["Software developer (python)"])
    # monkeypatch.setattr("jobs.CRAWLED_JOBS_OUTPUT_FILE", "tests/TEST_RESULT_CRAWLED_JOBS_OUTPUT_FILE.csv")

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    links = job_scanner._extract_links("http://127.0.0.1:9999/", www_response.text)

    assert links == [
        "http://127.0.0.1:9999/#about",
        "http://127.0.0.1:9999/#services",
        "http://127.0.0.1:9999/#contact",
        "http://127.0.0.1:9999/#careers",
        "mailto:contact@xyz.com",
    ]


def test_job_scanner_filter_potential_career_related_links(monkeypatch, mock_db_filepath, setup_www_page):

    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"

    www_response = job_scanner._fetch(url_fixture_link)
    links = job_scanner._extract_links(url_fixture_link, www_response.text)
    filtered_links = job_scanner._filter_potential_career_related_links(links, url_fixture_link)

    assert filtered_links == ["http://127.0.0.1:9999/#careers"]


def test_job_scanner_get_career_related_links(monkeypatch, mock_db_filepath, setup_www_page):
    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"
    links = job_scanner._get_career_related_links(url_fixture_link)

    assert links == ["http://127.0.0.1:9999/#careers"]


def test_job_scanner_may_company_have_the_needed_jobs(monkeypatch, mock_db_filepath, setup_www_page):
    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"
    does_have_the_needed_job = job_scanner.may_company_have_the_needed_jobs(url_fixture_link, ["tester oprogramowania"])

    assert does_have_the_needed_job


def test_job_scanner_may_company_have_the_needed_jobs_not_have(monkeypatch, mock_db_filepath, setup_www_page):
    job_scanner = JobScanner()
    url_fixture_link = "http://127.0.0.1:9999/"
    does_have_the_needed_job = job_scanner.may_company_have_the_needed_jobs(url_fixture_link, ["devops"])

    assert not does_have_the_needed_job
