from __future__ import annotations

from os.path import dirname


DB_FILEPATH = dirname(__file__) + "/USED_FILE_DB.csv"
CRAWLED_JOBS_OUTPUT_FILE = dirname(__file__) + "/CRAWLED_JOBS_OUTPUT_FILE.csv"

with open("JOB_ROLES_DEFINITIONS.txt", "r") as job_defs:
    job_definitions = [job_def.strip() for job_def in job_defs.readlines()]


JOB_ROLES = job_definitions or ["python"]
