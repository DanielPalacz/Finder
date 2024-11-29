from __future__ import annotations

import os.path

import pytest

from helpers import configure_logger
from helpers import iterate_over_csv_db_file


def test_configure_logger_check_logger_name(timestamp):
    logger_name = f"TestLogger_{timestamp}"
    logger = configure_logger(logger_name)

    assert logger.name == logger_name


def test_configure_logger_check_logger_file(timestamp, logs_directory):
    logger_name = f"TestLogger_{timestamp}"
    logger = configure_logger(logger_name)
    loger_filepath = f"{logs_directory}/{logger_name}.log"
    logger.info("It is test log item.")
    assert os.path.exists(loger_filepath)

    with open(loger_filepath, "r") as f:
        text = f.read()
        assert " - INFO - It is test log item." in repr(text)


def test_iterate_over_csv_db_file(mock_db_filepath):
    for company_data in iterate_over_csv_db_file(mock_db_filepath):
        line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

        assert line_number == "1"
        assert company_name == '"FIRMA 1" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
        assert krs_number == "101"
        assert main_pkd == "['ZARZĄDZANIE NIERUCHOMOŚCIAMI WYKONYWANE NA ZLECENIE', '68', '32', 'Z']"
        assert other_pkd == (
            "[{'opis': 'DZIAŁALNOŚĆ POMOCNICZA ZWIĄZANA Z UTRZYMANIEM PORZĄDKU W BUDYNKACH', "
            "'kodDzial': '81', 'kodKlasa': '10', 'kodPodklasa': 'Z'}]"
        )

        assert email == "brak_email"
        assert www == "http://127.0.0.1:9999/"
        assert voivodeship == "małopolskie"
        assert address == "Borsucza,16,Kraków,30-40-408,Kraków,Polska"


def test_iterate_over_csv_db_file_not_exists_db(mock_db_filepath):
    with pytest.raises(FileNotFoundError):
        for company_data in iterate_over_csv_db_file(f"{mock_db_filepath}-not-exists"):
            line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data
