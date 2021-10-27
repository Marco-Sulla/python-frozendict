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

Some benchmarks between `dict` and `coold`, a C-only extended and experimental version of frozendict[1]:

```
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: str; Type:       dict; Time: 7.68e-08; Sigma: 1e-09
Name: `constructor(d)`;         Size:    5; Keys: str; Type:      coold; Time: 3.24e-07; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: int; Type:       dict; Time: 7.77e-08; Sigma: 3e-09
Name: `constructor(d)`;         Size:    5; Keys: int; Type:      coold; Time: 3.21e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:       dict; Time: 6.13e-06; Sigma: 3e-07
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:      coold; Time: 5.28e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.63e-06; Sigma: 2e-07
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:      coold; Time: 4.22e-05; Sigma: 3e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:       dict; Time: 2.60e-07; Sigma: 4e-09
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:      coold; Time: 2.36e-07; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:       dict; Time: 4.83e-05; Sigma: 3e-06
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:      coold; Time: 2.91e-05; Sigma: 7e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:       dict; Time: 1.75e-07; Sigma: 8e-09
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:      coold; Time: 2.44e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:       dict; Time: 1.78e-07; Sigma: 6e-09
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:      coold; Time: 2.55e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:       dict; Time: 3.38e-05; Sigma: 7e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:      coold; Time: 4.04e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:       dict; Time: 2.43e-05; Sigma: 7e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:      coold; Time: 2.98e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: str; Type:       dict; Time: 7.69e-08; Sigma: 1e-09
Name: `constructor(o)`;         Size:    5; Keys: str; Type:      coold; Time: 2.58e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: int; Type:       dict; Time: 7.78e-08; Sigma: 2e-09
Name: `constructor(o)`;         Size:    5; Keys: int; Type:      coold; Time: 2.58e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:       dict; Time: 6.02e-06; Sigma: 4e-07
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:      coold; Time: 2.58e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.64e-06; Sigma: 2e-07
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:      coold; Time: 2.58e-08; Sigma: 8e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: str; Type:       dict; Time: 7.02e-08; Sigma: 3e-09
Name: `o.copy()`;               Size:    5; Keys: str; Type:      coold; Time: 3.21e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: int; Type:       dict; Time: 7.03e-08; Sigma: 3e-09
Name: `o.copy()`;               Size:    5; Keys: int; Type:      coold; Time: 3.21e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: str; Type:       dict; Time: 6.01e-06; Sigma: 4e-07
Name: `o.copy()`;               Size: 1000; Keys: str; Type:      coold; Time: 3.21e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.62e-06; Sigma: 2e-07
Name: `o.copy()`;               Size: 1000; Keys: int; Type:      coold; Time: 3.58e-08; Sigma: 3e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: str; Type:       dict; Time: 7.77e-08; Sigma: 3e-10
Name: `o == o`;                 Size:    5; Keys: str; Type:      coold; Time: 2.69e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: int; Type:       dict; Time: 7.52e-08; Sigma: 9e-09
Name: `o == o`;                 Size:    5; Keys: int; Type:      coold; Time: 2.69e-08; Sigma: 7e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.35e-05; Sigma: 2e-07
Name: `o == o`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.72e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.01e-05; Sigma: 9e-08
Name: `o == o`;                 Size: 1000; Keys: int; Type:      coold; Time: 2.66e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: str; Type:       dict; Time: 8.29e-08; Sigma: 2e-09
Name: `for x in o`;             Size:    5; Keys: str; Type:      coold; Time: 7.47e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: int; Type:       dict; Time: 8.26e-08; Sigma: 2e-09
Name: `for x in o`;             Size:    5; Keys: int; Type:      coold; Time: 7.48e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: str; Type:       dict; Time: 1.06e-05; Sigma: 7e-08
Name: `for x in o`;             Size: 1000; Keys: str; Type:      coold; Time: 8.71e-06; Sigma: 9e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: int; Type:       dict; Time: 1.06e-05; Sigma: 8e-08
Name: `for x in o`;             Size: 1000; Keys: int; Type:      coold; Time: 8.65e-06; Sigma: 1e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:       dict; Time: 8.59e-08; Sigma: 3e-09
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:      coold; Time: 7.32e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:       dict; Time: 8.57e-08; Sigma: 3e-09
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:      coold; Time: 7.34e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:       dict; Time: 1.04e-05; Sigma: 8e-08
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:      coold; Time: 8.73e-06; Sigma: 3e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:       dict; Time: 1.03e-05; Sigma: 1e-07
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:      coold; Time: 8.64e-06; Sigma: 2e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:       dict; Time: 1.27e-07; Sigma: 4e-09
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:      coold; Time: 1.26e-07; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:       dict; Time: 1.28e-07; Sigma: 2e-09
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:      coold; Time: 1.25e-07; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:       dict; Time: 1.75e-05; Sigma: 2e-07
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:      coold; Time: 1.76e-05; Sigma: 8e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:       dict; Time: 1.75e-05; Sigma: 2e-07
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:      coold; Time: 1.76e-05; Sigma: 1e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:       dict; Time: 6.65e-07; Sigma: 7e-09
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:      coold; Time: 2.42e-06; Sigma: 8e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:       dict; Time: 5.07e-07; Sigma: 2e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:      coold; Time: 2.36e-06; Sigma: 6e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:       dict; Time: 1.09e-04; Sigma: 2e-06
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:      coold; Time: 1.79e-04; Sigma: 7e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:       dict; Time: 3.09e-05; Sigma: 4e-07
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:      coold; Time: 7.57e-05; Sigma: 9e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:       dict; Time: 8.16e-07; Sigma: 1e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:      coold; Time: 1.88e-06; Sigma: 4e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:       dict; Time: 4.11e-07; Sigma: 1e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:      coold; Time: 1.45e-06; Sigma: 5e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:       dict; Time: 1.43e-04; Sigma: 2e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:      coold; Time: 2.05e-04; Sigma: 3e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:       dict; Time: 5.37e-05; Sigma: 7e-07
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:      coold; Time: 9.94e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:       dict; Time: 1.96e-07; Sigma: 6e-09
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:      coold; Time: 2.21e-07; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:       dict; Time: 1.99e-07; Sigma: 6e-09
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:      coold; Time: 2.41e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:       dict; Time: 3.78e-05; Sigma: 5e-07
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:      coold; Time: 3.63e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:       dict; Time: 2.84e-05; Sigma: 5e-07
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:      coold; Time: 2.87e-05; Sigma: 6e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size:    5; Keys: str; Type:       dict; Time: 8.25e-08; Sigma: 3e-09
Name: `for x in o.keys()`;      Size:    5; Keys: str; Type:      coold; Time: 7.35e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size:    5; Keys: int; Type:       dict; Time: 8.25e-08; Sigma: 3e-09
Name: `for x in o.keys()`;      Size:    5; Keys: int; Type:      coold; Time: 7.34e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size: 1000; Keys: str; Type:       dict; Time: 1.06e-05; Sigma: 9e-08
Name: `for x in o.keys()`;      Size: 1000; Keys: str; Type:      coold; Time: 8.71e-06; Sigma: 8e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size: 1000; Keys: int; Type:       dict; Time: 1.06e-05; Sigma: 7e-08
Name: `for x in o.keys()`;      Size: 1000; Keys: int; Type:      coold; Time: 8.64e-06; Sigma: 1e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size:    5; Keys: str; Type:       dict; Time: 1.01e-07; Sigma: 3e-09
Name: `for x in iter(o)`;       Size:    5; Keys: str; Type:      coold; Time: 9.27e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size:    5; Keys: int; Type:       dict; Time: 1.01e-07; Sigma: 3e-09
Name: `for x in iter(o)`;       Size:    5; Keys: int; Type:      coold; Time: 9.36e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size: 1000; Keys: str; Type:       dict; Time: 1.06e-05; Sigma: 1e-07
Name: `for x in iter(o)`;       Size: 1000; Keys: str; Type:      coold; Time: 8.74e-06; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size: 1000; Keys: int; Type:       dict; Time: 1.06e-05; Sigma: 8e-08
Name: `for x in iter(o)`;       Size: 1000; Keys: int; Type:      coold; Time: 8.67e-06; Sigma: 1e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size:    5; Keys: str; Type:       dict; Time: 7.83e-08; Sigma: 3e-09
Name: `o == d`;                 Size:    5; Keys: str; Type:      coold; Time: 7.96e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size:    5; Keys: int; Type:       dict; Time: 7.43e-08; Sigma: 2e-09
Name: `o == d`;                 Size:    5; Keys: int; Type:      coold; Time: 7.93e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.37e-05; Sigma: 1e-07
Name: `o == d`;                 Size: 1000; Keys: str; Type:      coold; Time: 1.33e-05; Sigma: 2e-07
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.01e-05; Sigma: 8e-08
Name: `o == d`;                 Size: 1000; Keys: int; Type:      coold; Time: 1.04e-05; Sigma: 2e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size:    5; Keys: str; Type:       dict; Time: 2.98e-08; Sigma: 4e-09
Name: `o.get(key)`;             Size:    5; Keys: str; Type:      coold; Time: 3.04e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size:    5; Keys: int; Type:       dict; Time: 2.94e-08; Sigma: 5e-09
Name: `o.get(key)`;             Size:    5; Keys: int; Type:      coold; Time: 2.92e-08; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size: 1000; Keys: str; Type:       dict; Time: 3.01e-08; Sigma: 4e-09
Name: `o.get(key)`;             Size: 1000; Keys: str; Type:      coold; Time: 3.07e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size: 1000; Keys: int; Type:       dict; Time: 3.04e-08; Sigma: 5e-09
Name: `o.get(key)`;             Size: 1000; Keys: int; Type:      coold; Time: 2.98e-08; Sigma: 4e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size:    5; Keys: str; Type:       dict; Time: 3.04e-08; Sigma: 1e-09
Name: `o[key]`;                 Size:    5; Keys: str; Type:      coold; Time: 2.99e-08; Sigma: 5e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size:    5; Keys: int; Type:       dict; Time: 3.06e-08; Sigma: 1e-09
Name: `o[key]`;                 Size:    5; Keys: int; Type:      coold; Time: 3.01e-08; Sigma: 9e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size: 1000; Keys: str; Type:       dict; Time: 2.81e-08; Sigma: 2e-09
Name: `o[key]`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.66e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size: 1000; Keys: int; Type:       dict; Time: 3.20e-08; Sigma: 6e-10
Name: `o[key]`;                 Size: 1000; Keys: int; Type:      coold; Time: 3.05e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size:    5; Keys: str; Type:       dict; Time: 2.49e-08; Sigma: 3e-09
Name: `key in o`;               Size:    5; Keys: str; Type:      coold; Time: 2.53e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size:    5; Keys: int; Type:       dict; Time: 2.46e-08; Sigma: 5e-09
Name: `key in o`;               Size:    5; Keys: int; Type:      coold; Time: 2.52e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size: 1000; Keys: str; Type:       dict; Time: 2.55e-08; Sigma: 4e-09
Name: `key in o`;               Size: 1000; Keys: str; Type:      coold; Time: 2.61e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size: 1000; Keys: int; Type:       dict; Time: 2.61e-08; Sigma: 4e-09
Name: `key in o`;               Size: 1000; Keys: int; Type:      coold; Time: 2.64e-08; Sigma: 3e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size:    5; Keys: str; Type:       dict; Time: 2.52e-08; Sigma: 4e-09
Name: `key not in o`;           Size:    5; Keys: str; Type:      coold; Time: 2.61e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size:    5; Keys: int; Type:       dict; Time: 2.49e-08; Sigma: 5e-09
Name: `key not in o`;           Size:    5; Keys: int; Type:      coold; Time: 2.58e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size: 1000; Keys: str; Type:       dict; Time: 2.58e-08; Sigma: 4e-09
Name: `key not in o`;           Size: 1000; Keys: str; Type:      coold; Time: 2.64e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size: 1000; Keys: int; Type:       dict; Time: 2.64e-08; Sigma: 4e-09
Name: `key not in o`;           Size: 1000; Keys: int; Type:      coold; Time: 2.66e-08; Sigma: 3e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size:    5; Keys: str; Type:      coold; Time: 4.30e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size:    5; Keys: int; Type:      coold; Time: 4.30e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 4.30e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 4.30e-08; Sigma: 8e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size:    5; Keys: str; Type:       dict; Time: 2.98e-08; Sigma: 9e-10
Name: `len(o)`;                 Size:    5; Keys: str; Type:      coold; Time: 3.04e-08; Sigma: 9e-10
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size:    5; Keys: int; Type:       dict; Time: 2.98e-08; Sigma: 7e-10
Name: `len(o)`;                 Size:    5; Keys: int; Type:      coold; Time: 3.04e-08; Sigma: 9e-10
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size: 1000; Keys: str; Type:       dict; Time: 3.90e-08; Sigma: 9e-10
Name: `len(o)`;                 Size: 1000; Keys: str; Type:      coold; Time: 3.93e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size: 1000; Keys: int; Type:       dict; Time: 3.90e-08; Sigma: 9e-10
Name: `len(o)`;                 Size: 1000; Keys: int; Type:      coold; Time: 3.93e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size:    5; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.keys()`;               Size:    5; Keys: str; Type:      coold; Time: 3.38e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size:    5; Keys: int; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.keys()`;               Size:    5; Keys: int; Type:      coold; Time: 3.38e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size: 1000; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.keys()`;               Size: 1000; Keys: str; Type:      coold; Time: 3.38e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.keys()`;               Size: 1000; Keys: int; Type:      coold; Time: 3.38e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size:    5; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.values()`;             Size:    5; Keys: str; Type:      coold; Time: 3.35e-08; Sigma: 7e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size:    5; Keys: int; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.values()`;             Size:    5; Keys: int; Type:      coold; Time: 3.35e-08; Sigma: 7e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size: 1000; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 2e-09
Name: `o.values()`;             Size: 1000; Keys: str; Type:      coold; Time: 3.36e-08; Sigma: 6e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size: 1000; Keys: int; Type:       dict; Time: 3.35e-08; Sigma: 2e-09
Name: `o.values()`;             Size: 1000; Keys: int; Type:      coold; Time: 3.35e-08; Sigma: 7e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size:    5; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 1e-09
Name: `o.items()`;              Size:    5; Keys: str; Type:      coold; Time: 3.41e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size:    5; Keys: int; Type:       dict; Time: 3.38e-08; Sigma: 1e-09
Name: `o.items()`;              Size:    5; Keys: int; Type:      coold; Time: 3.41e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size: 1000; Keys: str; Type:       dict; Time: 3.38e-08; Sigma: 1e-09
Name: `o.items()`;              Size: 1000; Keys: str; Type:      coold; Time: 3.41e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size: 1000; Keys: int; Type:       dict; Time: 3.38e-08; Sigma: 1e-09
Name: `o.items()`;              Size: 1000; Keys: int; Type:      coold; Time: 3.41e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size:    5; Keys: str; Type:       dict; Time: 4.41e-08; Sigma: 1e-09
Name: `iter(o)`;                Size:    5; Keys: str; Type:      coold; Time: 4.54e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size:    5; Keys: int; Type:       dict; Time: 4.40e-08; Sigma: 2e-09
Name: `iter(o)`;                Size:    5; Keys: int; Type:      coold; Time: 4.57e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size: 1000; Keys: str; Type:       dict; Time: 4.41e-08; Sigma: 1e-09
Name: `iter(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 4.55e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size: 1000; Keys: int; Type:       dict; Time: 4.42e-08; Sigma: 1e-09
Name: `iter(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 4.55e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size:    5; Keys: str; Type:       dict; Time: 1.35e-06; Sigma: 1e-08
Name: `repr(o)`;                Size:    5; Keys: str; Type:      coold; Time: 1.73e-06; Sigma: 5e-08
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size:    5; Keys: int; Type:       dict; Time: 6.47e-07; Sigma: 3e-08
Name: `repr(o)`;                Size:    5; Keys: int; Type:      coold; Time: 8.91e-07; Sigma: 1e-08
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size: 1000; Keys: str; Type:       dict; Time: 2.06e-04; Sigma: 3e-06
Name: `repr(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 2.33e-04; Sigma: 3e-05
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size: 1000; Keys: int; Type:       dict; Time: 1.02e-04; Sigma: 2e-06
Name: `repr(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 1.20e-04; Sigma: 6e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size:    5; Keys: str; Type:       dict; Time: 1.36e-06; Sigma: 1e-08
Name: `str(o)`;                 Size:    5; Keys: str; Type:      coold; Time: 1.75e-06; Sigma: 6e-08
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size:    5; Keys: int; Type:       dict; Time: 6.73e-07; Sigma: 2e-08
Name: `str(o)`;                 Size:    5; Keys: int; Type:      coold; Time: 9.19e-07; Sigma: 1e-08
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size: 1000; Keys: str; Type:       dict; Time: 2.06e-04; Sigma: 3e-06
Name: `str(o)`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.38e-04; Sigma: 3e-05
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.02e-04; Sigma: 3e-06
Name: `str(o)`;                 Size: 1000; Keys: int; Type:      coold; Time: 1.20e-04; Sigma: 6e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size:    5; Keys: str; Type:       dict; Time: 3.61e-08; Sigma: 2e-10
Name: `set`;                    Size:    5; Keys: str; Type:      coold; Time: 1.17e-07; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size:    5; Keys: int; Type:       dict; Time: 3.41e-08; Sigma: 1e-09
Name: `set`;                    Size:    5; Keys: int; Type:      coold; Time: 1.29e-07; Sigma: 9e-10
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size: 1000; Keys: str; Type:       dict; Time: 3.27e-08; Sigma: 9e-10
Name: `set`;                    Size: 1000; Keys: str; Type:      coold; Time: 6.19e-06; Sigma: 2e-07
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size: 1000; Keys: int; Type:       dict; Time: 3.50e-08; Sigma: 1e-09
Name: `set`;                    Size: 1000; Keys: int; Type:      coold; Time: 3.54e-06; Sigma: 2e-07
################################################################################
```

[1] Benchmarks done under Linux 64 bit, Python 3.10, using the C Extension.
