# Finder
#### The goal for that repo-project is to really help me with finding pythons projects / jobs.

#### But, first of all I looked for optimal solution from performance point of view. What did I find?
 - [Which multitasking solution?](https://github.com/DanielPalacz/Finder/blob/master/_notes/README__WHICH_MULTITASKING_SOLUTIONS.md)
 - [What about dynamic JS-based content impact?](https://github.com/DanielPalacz/Finder/blob/master/_notes/README__DYNAMIC_JS_IMPACT.md)
 - [SOLID thoughts?](https://github.com/DanielPalacz/Finder/blob/master/_notes/README__SOLID_THOUGHTS.md)


#### So, then what next?

| Item                                                             | Status        |
|------------------------------------------------------------------|---------------|
| Which multitasking solution?                                     | [DONE]        |
| playing with PostgreSQL                                          | [NOT STARTED] |
| checking impact of career links filtering                        | [DONE]        |
| limiting JS-impact  (by using requests-html and judging cost)    | [DONE]        |
| robots.txt add to solution relying on website's robots.txt rules | [NOT STARTED] |
| unit-testing (pytest)                                            | [DONE]        |
| dockerize solution                                               | [DONE]        |
| adding lock for saving results to file                           | [DONE]        |
| refactoring to follow SOLID rules                                | [DONE]        |
| small separate thread based Flask api for monitoring execution   | [DONE]        |
| mypy setup, fixing several 'mypy-related' typing issues          | [DONE]        |
| integrating coverage package for test coverage metrics           | [DONE]        |
| creating GitHub Actions CI pipeline for automation tests         | [DONE]        |



# Running solution:
```
Copy company database (CSV) to main directory and save as 'USED_FILE_DB.csv'.
 - create venv: python3 -m venv venv
 - pip install -r requirements.txt
 - python jobs.py
```

# Monitoring execution:
```
For that reasons, small Flask api is setup for time of 'python jobs.py' execution:
 - http://127.0.0.1:7777
 - http://127.0.0.1:7777/logs
 - http://127.0.0.1:7777/results

Or if 'python jobs.py' execution ended then small Flask api can be run this way:
 - python flask_api.py
```


#### Running tests:
```
 - PYTHONPATH=. pytest -vv tests/
 - PYTHONPATH=. pytest -s -vv tests/
 - PYTHONPATH=. pytest -vv --html=TestExecutionReport.html --self-contained-html
 - PYTHONPATH=. pytest -vv --cov-report=html:TestCoverageReport tests/
```

#### Dockerizing solution:
```
From main directory, build docker image:
 - docker build -t my_scraper_app .

Now, prepare
 - CSV_DB_FILEPATH - Db should exist there.
 - OUTPUT_JOB_SEARCH_FILEPATH - Empty file dedicated for output results should exist there

Start container:
 - docker run -d --rm -v <CSV_DB_FILEPATH>:/app/USED_FILE_DB.csv -v <OUTPUT_JOB_SEARCH_FILEPATH>:/app/CRAWLED_JOBS_OUTPUT_FILE.csv -p <PORT_IN_OS>:<PORT_INSIDE_CONTAINER> my_scraper_app

Now, look what happens inside container:
 - docker exec -it container_name bash

Simple API is also provided for that reasons:
 - http://127.0.0.1:<PORT_IN_OS>/
 - http://127.0.0.1:<PORT_IN_OS>/logs
 - http://127.0.0.1:<PORT_IN_OS>/results
```
