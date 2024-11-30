# Finder
#### The goal for that repo-project is to really help me with finding pythons projects / jobs.

#### But, first of all I looked for optimal solution from performance point of view. What did I find?
 - [Which multitasking solution?](https://github.com/DanielPalacz/Finder/blob/master/README__WHICH_MULTITASKING_SOLUTIONS.md)
 - [What about dynamic JS-based content impact?](https://github.com/DanielPalacz/Finder/blob/master/README__DYNAMIC_JS_IMPACT.md)


#### So, then what next?

| Item                                                                             | Status         |
|----------------------------------------------------------------------------------|----------------|
| Which multitasking solution?                                                     | [DONE]         |
| playing with PostgreSQL                                                          | [NOT STARTED]  |
| checking impact of career links filtering                                        | [IN PROGRESS]  |
| limiting impact of dynamic JS content by using requests-html and evaulating cost | [DONE]         |
| robots.txt add to solution relying on website's robots.txt rules                 | [NOT STARTED]  |
| unit-testing (pytest)                                                            | [IN PROGRESS]  |



#### Running solution:
```
Copy company database (CSV) to main directory and save as 'USED_FILE_DB.csv'.

 - create venv: python3 -m venv venv
 - pip install -r requirements.txt
 - python jobs.py
```


#### Running tests:
```
 - PYTHONPATH=. pytest -s -vv tests/
 - PYTHONPATH=. pytest -s -vv --html=report.html --self-contained-html
 ```
