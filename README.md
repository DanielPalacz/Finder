# Finder
#### The goal for that repo-project is to really help me with finding pythons projects / jobs.

#### I looked for optimal solution from performance point of view. What was I found.
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

Seems that bandwith here plays dominant role. Hovewer
Results:
2 > 1
C > B > A

winner C2
```

#### Next is Asyncio try. Let see.
