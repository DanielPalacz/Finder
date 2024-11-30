
### MULTITASKING SOLUTIONS CHECKS

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
##### I thought about celery infrastructure, but for this project it will not be beneficial.
 - I want the fastest solution to run search during the night and simply dont have setup to have gains from celery.


### The solution will be multiprocessing-based.
