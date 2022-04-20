#!/usr/bin/env python3

import resource
import frozendict

print("frozendict version:", frozendict.__version__)
print()

c = 0

while True:
    fz = frozendict.frozendict({i: i for i in range(1000)})
    hash(fz)
    
    if (c % 10000) == 0:
        max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"iteration: {c}, max rss: {max_rss} kb")
    
    c += 1
