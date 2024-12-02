from __future__ import annotations

import multiprocessing
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config import CRAWLED_JOBS_OUTPUT_FILE
from config import JOB_ROLES
from helpers import configure_logger
from helpers import iterate_over_csv_db_file
from helpers import LoggerT


class UrlFetcher:
    """Implements url html content fetching.

    Usage:
        www_html_text = UrlFetcher().fetch(url)
        if www_html_text is None:
            print("Url fetching failed")

    Args:
        logger (LoggerT): logger object

    Attributes:
        logger (LoggerT): logger object
    """

    def __init__(self, logger: LoggerT):
        self.logger = logger

    def fetch(self, url: str) -> Optional[str]:
        """Fetches link (http request execution).

        Args:
            url: website url link

        Returns:
            Text with website content or None in case of issues
        """
        self.logger.info(f"Fetching the given url: {url}")

        try:
            response = requests.get(url, allow_redirects=True, timeout=5)
            if response.ok:
                self.logger.debug(f"Successfully fetched the given url: {url}")
                return response.text
            else:
                self.logger.error(
                    f"Returning None, because something went wrong with request execution ({url}). "
                    f"Returned status code: {response.status_code}"
                )
                return None

        except requests.exceptions.SSLError:
            if url.startswith("https://"):
                url = url.replace("https://", "http://")
            try:
                response_backup = requests.get(url, allow_redirects=True, timeout=5)
                if response_backup.ok:
                    self.logger.debug(f"Successfully fetched the given url: {url} [backup http flow].")
                    return response_backup.text
                else:
                    self.logger.error(
                        f"Returning None, because something went wrong with request execution ({url}). "
                        f"Returned status code: {response_backup.status_code} [backup http flow]."
                    )
                    return None

            except Exception as e:
                self.logger.error(
                    f"Returning None, because something went wrong with request execution ({url}). "
                    f"Details: {e!r} [backup http flow]"
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


class LinksExtractor:
    """Extracts a-tag links from fetched html website content.

    Usage:
        links = LinkExtractor().extract_links(url)

    Args:
        logger (LoggerT): logger object

    Attributes:
        logger (LoggerT): logger object
    """

    def __init__(self, logger):
        self.logger = logger

    def extract_links(self, baseurl: str, website_html_text: str) -> list[str]:
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


class CareerLinksFetcher(LinksExtractor):
    """Extracts a-tag career related links from provided list of links.

    Usage:
        career_links = CareerLinksExtractor().get_career_links(url)

    Args:
        logger (LoggerT): logger object

    Attributes:
        CAREER_KEYWORDS (list): list with career related keywords
        logger (LoggerT): logger object
    """

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
        "employment",
        "employment-opportunities",
        "work-with-us",
        "join-our-team",
        "career-opportunities",
        "job-openings",
        "full-time-jobs",
        "part-time-jobs",
        "remote-jobs",
        "work-from-home",
        "job-listings",
        "vacancy",
        "talent-acquisition",
        "job-board",
        "staff-recruitment",
        "job-application",
        "praca-zdalna",
        "praca-online",
        "rekrutacja-online",
        "oferty-zatrudnienia",
        "rekrutacja-praca",
        "zatrudnienie",
        "team",
        "nasz-zespół",
        "praca-dla-ciebie",
        "oferty-stazowe",
        "zatrudnimy",
        "praca-w-zespole",
        "dołącz-do-nas",
        "internships",
        "freelance-jobs",
        "career-path",
        "praca-it",
        "kariera-it",
    ]

    def __init__(self, logger):
        super().__init__(logger)

    def get_career_links(self, baseurl: str) -> list:
        """Filters for potential career related links from list of the links.

        Args:
            baseurl: base part of url

        Returns:
            List with potential career related links.
        """
        website_html_text = UrlFetcher(self.logger).fetch(baseurl)

        if website_html_text is None:
            self.logger.debug(f"Http request failed, so returning empty list of career links [{baseurl}].")
            return []

        links = self.extract_links(baseurl, website_html_text)
        if not links:
            self.logger.debug(f"There was not links at all, so returning empty list of career links [{baseurl}].")
            return []

        self.logger.debug(f"Filtering links from the given url: {baseurl} to have only potential career links.")
        potential_career_links = []
        for link in links:
            career_keyword_check = [career_keyword for career_keyword in self.CAREER_KEYWORDS if career_keyword in link]
            if career_keyword_check:
                potential_career_links.append(link)

        return potential_career_links


class JobsChecker:
    """Provides interface for checking if then given link contains searched jobs.

    Usage:
        has_needed_jobs = JobsChecker().may_company_have_the_needed_jobs(url)

    Args:
        logger (LoggerT): logger object

    Attributes:
        logger (LoggerT): logger object
    """

    def __init__(self, logger: LoggerT):
        self.logger = logger

    def may_company_have_the_needed_jobs(self, url) -> bool:
        """Checks if the given link www may contain jobs that are searched.

        Args:
            url: www link to be checked for jobs search

        Returns:
            Boolean value describing probability that link contains jobs that are searched.
        """
        job_phrases = JOB_ROLES
        self.logger.debug(f"Checking if the given link: {url} contains jobs that are searched ({job_phrases}).")

        website_text = UrlFetcher(self.logger).fetch(url)

        if website_text is None:
            return False
        else:
            website_text = website_text.lower()

        for job_role in job_phrases:
            job_role = job_role.lower()
            if job_role in website_text:
                return True

        return False


class JobsFileSaver:
    """Saves to file company data.

    Usage:
        CompanyDataFileSaver.save()

    Args:
        logger (LoggerT): logger object

    Attributes:
        logger (LoggerT): logger object
    """

    def __init__(self, logger: LoggerT):
        self.logger = logger
        self.__filepath = CRAWLED_JOBS_OUTPUT_FILE

    def save(self, company_data: list[str], link: str) -> None:
        """Runs www check for the needed job search.

        Args:
            company_data: list of strings with company data
            link: url link for which searched job was found

        Returns:
            None
        """
        line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

        with open(CRAWLED_JOBS_OUTPUT_FILE, "a+") as jobs_file:
            jobs_file.write(f"{company_name};{krs_number};{email};{www};{voivodeship};{address};{link}\n")
            self.logger.info(f"Found potential job, so breaking loop iteration [{company_name}, {link}].")


class JobScanner:
    """Class scanning company websites for dedicated job roles.

    Usage:
        jobs_scanner = JobScanner()
        jobs_scanner.run()

    Attributes:
        logger (LoggerT): logger object
        __career_links_fetcher (CareerLinksFetcher): career links fetcher object
        __jobs_checker (JobsChecker): jobs checker object
        __jobs_file_saver (JobsFileSaver): jobs file saver object
    """

    def __init__(self):
        self.logger = configure_logger("JobScanner")
        self.__career_links_fetcher = CareerLinksFetcher(self.logger)
        self.__jobs_checker = JobsChecker(self.logger)
        self.__jobs_file_saver = JobsFileSaver(self.logger)

    def run(self, start_line_number: int = 0) -> None:
        """Runs job search.

        Args:
            start_line_number: number of line in file db to start processing

        Returns:
            None, but save job/company data directly to output file
        """
        running_processes = []
        lock = multiprocessing.Lock()

        for company_data in iterate_over_csv_db_file():
            line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data

            if start_line_number and start_line_number > int(line_number):
                continue

            if www == "brak_www":
                continue

            process = multiprocessing.Process(
                target=self.__run_www_check_for_the_needed_jobs, args=(www, company_data, lock)
            )

            process.start()
            running_processes.append(process)

            if not int(line_number) % 12:
                for p in running_processes:
                    p.join()
                else:
                    self.logger.info(f"Finished all 12-processes-based tasks iteration [line:{line_number}].")
                    running_processes.clear()

    def __run_www_check_for_the_needed_jobs(self, www, company_data: list[str], lock: multiprocessing.Lock) -> None:
        """Runs www check for the needed job search.

        Args:
            www: url to be checked for the searched jobs
            company_data: list of strings with company data
            lock: lock object for writing to file

        Returns:
            None, but save job/company data directly to output file
        """
        line_number, company_name, krs_number, main_pkd, other_pkd, email, www, voivodeship, address = company_data
        self.logger.info(f"Processing line number: {line_number}, {company_name}")

        career_links = list(set(self.__career_links_fetcher.get_career_links(www)))
        career_links_unique = list(set(career_links))

        for link in career_links_unique:
            if self.__jobs_checker.may_company_have_the_needed_jobs(link):
                with lock:
                    self.__jobs_file_saver.save(company_data, link)
                break


if __name__ == "__main__":
    scanner = JobScanner()
    scanner.run()
