# frozendict

Welcome, fellow programmer!

`frozendict` is a simple immutable dictionary. Unlike other similar 
implementations, immutability is guaranteed: you can't change the internal 
variables of the class, and they are all immutable objects.  Reinvoking 
`__init__` does not alter the object.

The API is the same as `dict`, without methods that can change the immutability. 
So it supports also `fromkeys`, unlike other implementations. Furthermore it 
can be `pickle`d, un`pickle`d and have an hash, if all values are hashable.

Examples:

```python
from frozendict import frozendict

fd = frozendict({"Sulla": "Marco", "Hicks": "Bill"})

print(fd)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})

print(fd["Sulla"])
# Marco

fd["God"]
# KeyError: 'God'

len(fd)
# 2

"Sulla" in fd
# True

"Sulla" not in fd
# False

"God" in fd
# False

hash(fd)
# 5833699487320513741

fd_unhashable = frozendict({1: []})
hash(fd_unhashable)
# TypeError: Not all values are hashable.

fd2 = fd.copy()
fd2 == fd
# True

fd3 = frozendict(fd)
fd3 == fd
# True

fd4 = frozendict({"Hicks": "Bill", "Sulla": "Marco"})

print(fd4)
# frozendict({'Hicks': 'Bill', 'Sulla': 'Marco'})

fd4 == fd
# True

import pickle
fd_unpickled = pickle.loads(pickle.dumps(fd))
print(fd_unpickled)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})
fd_unpickled == fd
# True

frozendict(Sulla="Marco", Hicks="Bill")
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'}

frozendict((("Sulla", "Marco"), ("Hicks", "Bill")))
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})

fd.get("Sulla")
# 'Marco'

print(fd.get("God"))
# None

tuple(fd.keys())
# ('Sulla', 'Hicks')

tuple(fd.values())
# ('Marco', 'Bill')

tuple(fd.items())
# (('Sulla', 'Marco'), ('Hicks', 'Bill'))

frozendict.fromkeys(["Marco", "Giulia"], "Sulla")
# frozendict({'Marco': 'Sulla', 'Giulia': 'Sulla'})

iter(fd)
# <dict_keyiterator object at 0x7feb75c49188>

fd["Sulla"] = "Silla"
# TypeError: 'frozendict' object doesn't support item assignment
```

# Benchmarks

Some benchmarks between `dict` and `frozendict`[1]:

```
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: str; Type:       dict; Time: 1.72e-07; Sigma: 4e-09
Name: `constructor(d)`;         Size:    5; Keys: str; Type: frozendict; Time: 1.28e-07; Sigma: 6e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: int; Type:       dict; Time: 1.80e-07; Sigma: 5e-09
Name: `constructor(d)`;         Size:    5; Keys: int; Type: frozendict; Time: 1.23e-07; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:       dict; Time: 2.62e-05; Sigma: 8e-07
Name: `constructor(d)`;         Size: 1000; Keys: str; Type: frozendict; Time: 1.22e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:       dict; Time: 1.97e-05; Sigma: 3e-07
Name: `constructor(d)`;         Size: 1000; Keys: int; Type: frozendict; Time: 6.63e-06; Sigma: 2e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:       dict; Time: 3.75e-07; Sigma: 3e-08
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type: frozendict; Time: 4.06e-07; Sigma: 6e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:       dict; Time: 7.13e-05; Sigma: 2e-06
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type: frozendict; Time: 5.72e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:       dict; Time: 2.41e-07; Sigma: 1e-08
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type: frozendict; Time: 2.49e-07; Sigma: 8e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:       dict; Time: 2.57e-07; Sigma: 4e-09
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type: frozendict; Time: 2.56e-07; Sigma: 2e-08
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:       dict; Time: 4.49e-05; Sigma: 2e-06
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type: frozendict; Time: 3.41e-05; Sigma: 7e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:       dict; Time: 3.21e-05; Sigma: 5e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type: frozendict; Time: 3.03e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: str; Type:       dict; Time: 1.71e-07; Sigma: 1e-08
Name: `constructor(o)`;         Size:    5; Keys: str; Type: frozendict; Time: 1.55e-07; Sigma: 1e-06
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: int; Type:       dict; Time: 1.79e-07; Sigma: 7e-09
Name: `constructor(o)`;         Size:    5; Keys: int; Type: frozendict; Time: 1.56e-07; Sigma: 1e-06
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:       dict; Time: 2.62e-05; Sigma: 2e-06
Name: `constructor(o)`;         Size: 1000; Keys: str; Type: frozendict; Time: 1.52e-07; Sigma: 8e-06
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:       dict; Time: 1.96e-05; Sigma: 3e-06
Name: `constructor(o)`;         Size: 1000; Keys: int; Type: frozendict; Time: 1.51e-07; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: str; Type:       dict; Time: 7.30e-08; Sigma: 6e-09
Name: `o.copy()`;               Size:    5; Keys: str; Type: frozendict; Time: 3.32e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: int; Type:       dict; Time: 7.68e-08; Sigma: 3e-09
Name: `o.copy()`;               Size:    5; Keys: int; Type: frozendict; Time: 3.21e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: str; Type:       dict; Time: 6.08e-06; Sigma: 4e-07
Name: `o.copy()`;               Size: 1000; Keys: str; Type: frozendict; Time: 3.20e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.45e-06; Sigma: 1e-07
Name: `o.copy()`;               Size: 1000; Keys: int; Type: frozendict; Time: 3.19e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: str; Type:       dict; Time: 7.81e-08; Sigma: 6e-09
Name: `o == o`;                 Size:    5; Keys: str; Type: frozendict; Time: 2.55e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: int; Type:       dict; Time: 8.05e-08; Sigma: 1e-09
Name: `o == o`;                 Size:    5; Keys: int; Type: frozendict; Time: 2.58e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.40e-05; Sigma: 5e-07
Name: `o == o`;                 Size: 1000; Keys: str; Type: frozendict; Time: 2.58e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.07e-05; Sigma: 2e-07
Name: `o == o`;                 Size: 1000; Keys: int; Type: frozendict; Time: 2.58e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: str; Type:       dict; Time: 7.79e-08; Sigma: 3e-09
Name: `for x in o`;             Size:    5; Keys: str; Type: frozendict; Time: 6.96e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: int; Type:       dict; Time: 7.76e-08; Sigma: 4e-09
Name: `for x in o`;             Size:    5; Keys: int; Type: frozendict; Time: 6.88e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: str; Type:       dict; Time: 9.29e-06; Sigma: 9e-08
Name: `for x in o`;             Size: 1000; Keys: str; Type: frozendict; Time: 7.74e-06; Sigma: 6e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: int; Type:       dict; Time: 8.99e-06; Sigma: 5e-08
Name: `for x in o`;             Size: 1000; Keys: int; Type: frozendict; Time: 7.28e-06; Sigma: 6e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:       dict; Time: 7.96e-08; Sigma: 2e-09
Name: `for x in o.values()`;    Size:    5; Keys: str; Type: frozendict; Time: 6.87e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:       dict; Time: 7.99e-08; Sigma: 3e-09
Name: `for x in o.values()`;    Size:    5; Keys: int; Type: frozendict; Time: 6.85e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:       dict; Time: 9.95e-06; Sigma: 8e-08
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type: frozendict; Time: 7.11e-06; Sigma: 6e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:       dict; Time: 9.83e-06; Sigma: 9e-08
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type: frozendict; Time: 6.96e-06; Sigma: 5e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:       dict; Time: 1.31e-07; Sigma: 4e-09
Name: `for x in o.items()`;     Size:    5; Keys: str; Type: frozendict; Time: 1.24e-07; Sigma: 6e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:       dict; Time: 1.30e-07; Sigma: 5e-09
Name: `for x in o.items()`;     Size:    5; Keys: int; Type: frozendict; Time: 1.25e-07; Sigma: 6e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:       dict; Time: 1.82e-05; Sigma: 8e-07
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type: frozendict; Time: 1.68e-05; Sigma: 3e-07
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:       dict; Time: 1.92e-05; Sigma: 5e-07
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type: frozendict; Time: 1.71e-05; Sigma: 3e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:       dict; Time: 6.68e-07; Sigma: 6e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type: frozendict; Time: 2.52e-06; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:       dict; Time: 4.71e-07; Sigma: 3e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type: frozendict; Time: 2.36e-06; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:       dict; Time: 1.30e-04; Sigma: 3e-06
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type: frozendict; Time: 2.02e-04; Sigma: 9e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:       dict; Time: 2.83e-05; Sigma: 1e-06
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type: frozendict; Time: 7.47e-05; Sigma: 2e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:       dict; Time: 9.30e-07; Sigma: 1e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type: frozendict; Time: 1.81e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:       dict; Time: 4.56e-07; Sigma: 1e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type: frozendict; Time: 1.32e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:       dict; Time: 1.69e-04; Sigma: 6e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type: frozendict; Time: 1.85e-04; Sigma: 1e-05
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:       dict; Time: 6.17e-05; Sigma: 9e-07
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type: frozendict; Time: 7.11e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:       dict; Time: 2.23e-07; Sigma: 2e-08
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type: frozendict; Time: 4.61e-07; Sigma: 2e-08
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:       dict; Time: 2.40e-07; Sigma: 5e-09
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type: frozendict; Time: 4.83e-07; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:       dict; Time: 4.18e-05; Sigma: 1e-06
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type: frozendict; Time: 5.49e-05; Sigma: 4e-03
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:       dict; Time: 3.03e-05; Sigma: 2e-06
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type: frozendict; Time: 5.29e-05; Sigma: 1e-02
################################################################################
```

[1] Benchmarks done under Linux 64 bit, Python 3.9, using the C Extension.
    Note that in Python 3.10 `dict` is faster in creation from another `dict`
    without "holes" (no pop, del and popitem).
