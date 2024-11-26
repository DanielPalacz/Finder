from __future__ import annotations

import multiprocessing
import threading
from os.path import dirname
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from helpers import configure_logger
from helpers import iterate_over_csv_db_file


CRAWLED_JOBS_OUTPUT_FILE = dirname(__file__) + "/CRAWLED_JOBS_OUTPUT_FILE.csv"
JOB_ROLES = ["python engineer", "python software engineer"]


class JobScanner:
    """Class scanning company websites for dedicated job roles."""

    CAREER_KEYWORDS = [
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

    def __init__(self):
        self.logger = configure_logger("JobScanner")

    def _fetch(self, url) -> Optional[requests.models.Response]:
        """Fetches link (http request execution).

        Args:
            url: website url link

        Returns:
            Response object or None in case of issues
        """
        self.logger.info(f"Fetching the given url: {url}")

        try:
            response = requests.get(url, allow_redirects=True, timeout=5)
            if response.ok:
                self.logger.debug(f"Successfully fetched the given url: {url}")
                return response
            else:
                self.logger.error(
                    f"Returning None, because something went wrong with request execution ({url}). "
                    f"Returned status code: {response.status_code}"
                )
                return None

        except requests.RequestException as e:
            self.logger.error(
                f"Returning None, because something went wrong with request execution ({url}). Details: {e}"
            )
            return None

        except Exception as e:
            self.logger.error(
                f"Returning None, because something went wrong with request execution ({url}). Details: {e}"
            )
            return None

    def _extract_links(self, baseurl: str, website_html_text: str) -> list[str]:
        """Extracts all a-tags links from html text.

        Args:
            baseurl: base part of url
            website_html_text: website html text

        Returns:
            List with links.
        """
        self.logger.debug(f"Extracting links from the given url: {baseurl}")
        soup = BeautifulSoup(website_html_text, "html.parser")
        links = soup.find_all("a")
        hrefs = [link.get("href") for link in links]
        links_results = [urljoin(baseurl, link) for link in hrefs]
        return links_results

    def _filter_potential_career_related_links(self, links: list, baseurl: str) -> list:
        """Filters for potential career related links from list of the links.

        Args:
            baseurl: base part of url
            links: list with links.

        Returns:
            List with potential career related links.
        """
        self.logger.debug(f"Filtering links from the given url: {baseurl} to have only potential career links.")
        potential_career_links = []
        for link in links:
            career_keyword_check = [career_keyword for career_keyword in self.CAREER_KEYWORDS if career_keyword in link]
            if career_keyword_check:
                potential_career_links.append(link)

        return potential_career_links

    def _get_career_related_links(self, url) -> list:
        """Extracts career related links for the given url.

        Args:
            url: url to be scanned for career related links

        Returns:
            List with career links. In case of issues empty list is returned.
        """
        response_url = self._fetch(url)
        if response_url is None:
            return []
        links = self._extract_links(response_url.url, response_url.text)
        potential_career_links = self._filter_potential_career_related_links(links, url)
        return potential_career_links

    def _run_www_check_for_the_needed_jobs(self, www, job_phrases: list[str], company_data: list[str]) -> None:
        """Runs www check for the needed job search.

        Args:
            www: url to be checked for the searched jobs
            job_phrases: url to be checked for the searched jobs

        Returns:
            List with career links. In case of issues empty list is returned.
        """
        line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data
        self.logger.info(f"Processing line number: {line_number}, {company_name}")

        career_links = [www] + list(set(self._get_career_related_links(www)))
        for link in career_links:
            if self.may_company_have_the_needed_jobs(link, job_phrases):
                with open(CRAWLED_JOBS_OUTPUT_FILE, "a+") as jobs_file:
                    jobs_file.write(f"{company_name};{krs_number};{email};{www};{voivodeship};{address};{link}\n")
                    self.logger.info(f"Found potential job, so breaking loop iteration [{company_name}, {link}].")
                break

    def may_company_have_the_needed_jobs(self, url, job_phrases: list) -> bool:
        """Checks if the given link www may contain jobs that are searched.

        Args:
            url: url link to be checked for job search
            job_phrases: roles to be checked for job search

        Returns:
            Boolean value describing probability that link contains jobs that are searched.
        """
        self.logger.debug(f"Checking if the given link: {url} may may contain jobs that are searched ({job_phrases}).")
        response_url = self._fetch(url)

        if response_url is None:
            return False
        website_text = repr(response_url.text.lower())
        for job_role in job_phrases:
            job_role = job_role.lower()
            if job_role in website_text:
                return True

        return False

    def run_synchronously(self, start_line_number: int = 0) -> None:
        """Runs job search.

        Args:
            start_line_number: number of line in file db to start processing

        Returns:
            None, but save job directly to output file
        """
        for company_data in iterate_over_csv_db_file():
            line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

            if start_line_number and start_line_number > int(line_number):
                continue

            if www == "brak_www":
                continue

            self._run_www_check_for_the_needed_jobs(www, JOB_ROLES, company_data)

            if not int(line_number) % 11:
                self.logger.info(f"Finished all 11-like iteration [line:{line_number}].")

    def run_with_threading(self, start_line_number: int = 0) -> None:
        """Runs job search.

        Args:
            start_line_number: number of line in file db to start processing

        Returns:
            None, but save job directly to output file
        """
        running_threads = []

        for company_data in iterate_over_csv_db_file():
            line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

            if start_line_number and start_line_number > int(line_number):
                continue

            if www == "brak_www":
                continue

            thread = threading.Thread(
                target=self._run_www_check_for_the_needed_jobs, args=(www, JOB_ROLES, company_data)
            )

            thread.start()
            running_threads.append(thread)

            # self._run_www_check_for_the_needed_jobs(www, JOB_ROLES, company_data)

            if not int(line_number) % 11:
                for t in running_threads:
                    t.join()
                else:
                    self.logger.info(f"Finished all thread tasks in the iteration [line:{line_number}].")
                    running_threads.clear()

    def run_with_multiprocessing(self, start_line_number: int = 0) -> None:
        """Runs job search.

        Args:
            start_line_number: number of line in file db to start processing

        Returns:
            None, but save job directly to output file
        """
        running_processes = []

        for company_data in iterate_over_csv_db_file():
            line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

            if start_line_number and start_line_number > int(line_number):
                continue

            if www == "brak_www":
                continue

            process = multiprocessing.Process(
                target=self._run_www_check_for_the_needed_jobs, args=(www, JOB_ROLES, company_data)
            )

            process.start()
            running_processes.append(process)

            # self._run_www_check_for_the_needed_jobs(www, JOB_ROLES, company_data)

            if not int(line_number) % 12:
                for p in running_processes:
                    p.join()
                else:
                    self.logger.info(f"Finished all 12-processes-based tasks iteration [line:{line_number}].")
                    running_processes.clear()


if __name__ == "__main__":
    scanner = JobScanner()
    scanner.run_with_multiprocessing()
