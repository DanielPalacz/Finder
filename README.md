# Finder
#### The goal for that repo-project is to really help me with finding pythons projects / jobs.

#### But, first of all I looked for optimal solution from performance point of view. What did I find?
```
Having 2 Ubuntu setups
1. Home based PC:
 - Medium decent CPU - 4 cores
 - 'slow' bandwith meand less than 100 Mbit/s DL/UL
2. Server based PC:
 - strong optimized server based 1 core CPU
 - super fast bandwith

Having three type of solutions:
 A - synchronous
 B - threading based
 C - multiprocessing based
 D - asyncio based

Results:
2 > 1
C > D ~> B > A

winner C2
second place: C1 and D2
fourth place: B2

Seems that the additional Server based features and bandwith here plays dominant role.
The nature of the tasks is hybrid slightly CPU-bound, but more IO-bound.
```
##### I thought about celery infrastructure, but for this project it will not be beneficial. I want the fastest solution to run search during the night and simply dont have setup to have gains from celery.

#### So, then what next?
```
 - the solution will be multiprocessing-based, but I learn temporarily asyncio now as I want to invest some time for this and it demending a bit more effort. Hovever asyncio solution get well and it is on the branch.
 - time to play with PostgreSQL (this and next week)
 - extending company website database (till eoy)
 - checking if carrer links filter exclude some valid search accross Poland (26-28/11)
 ```
