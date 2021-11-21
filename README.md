# frozendict

Welcome, fellow programmer!

`frozendict` is a simple immutable dictionary. Unlike other similar 
implementations, immutability is guaranteed: you can't change the internal 
variables of the class, and they are all immutable objects.  Reinvoking 
`__init__` does not alter the object.

The API is the same as `dict`, without methods that can change the immutability. 
So it supports also `fromkeys`, unlike other implementations. Furthermore it 
can be `pickle`d, un`pickle`d and have an hash, if all values are hashable.

You can also add any `dict` to a `frozendict` using the `|` operator. The result is a new `frozendict`.

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

fd | {1: 2}
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill', 1: 2})

fd5 = frozendict(fd)
id_fd5 = id(fd5)
fd5 |= {1: 2}
fd5
# frozendict.frozendict({'Sulla': 'Marco', 'Hicks': 'Bill', 1: 2})
id(fd5) != id_fd5
# True

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
Name: `constructor(d)`;         Size:    5; Keys: str; Type:       dict; Time: 7.88e-08; Sigma: 5e-09
Name: `constructor(d)`;         Size:    5; Keys: str; Type:      coold; Time: 2.99e-07; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: int; Type:       dict; Time: 8.16e-08; Sigma: 4e-09
Name: `constructor(d)`;         Size:    5; Keys: int; Type:      coold; Time: 3.12e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:       dict; Time: 5.90e-06; Sigma: 5e-07
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:      coold; Time: 5.22e-05; Sigma: 8e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.44e-06; Sigma: 2e-07
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:      coold; Time: 4.05e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:       dict; Time: 2.38e-07; Sigma: 2e-09
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:      coold; Time: 2.25e-07; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:       dict; Time: 4.67e-05; Sigma: 1e-06
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:      coold; Time: 2.73e-05; Sigma: 6e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:       dict; Time: 2.01e-07; Sigma: 2e-09
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:      coold; Time: 2.44e-07; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:       dict; Time: 2.18e-07; Sigma: 3e-09
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:      coold; Time: 2.59e-07; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:       dict; Time: 4.22e-05; Sigma: 6e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:      coold; Time: 4.20e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:       dict; Time: 2.98e-05; Sigma: 3e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:      coold; Time: 3.08e-05; Sigma: 5e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: str; Type:       dict; Time: 7.88e-08; Sigma: 5e-09
Name: `constructor(o)`;         Size:    5; Keys: str; Type:      coold; Time: 2.58e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: int; Type:       dict; Time: 8.35e-08; Sigma: 3e-09
Name: `constructor(o)`;         Size:    5; Keys: int; Type:      coold; Time: 2.58e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:       dict; Time: 6.09e-06; Sigma: 2e-07
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:      coold; Time: 2.58e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.48e-06; Sigma: 2e-07
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:      coold; Time: 2.58e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: str; Type:       dict; Time: 7.08e-08; Sigma: 4e-09
Name: `o.copy()`;               Size:    5; Keys: str; Type:      coold; Time: 3.35e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: int; Type:       dict; Time: 7.18e-08; Sigma: 5e-09
Name: `o.copy()`;               Size:    5; Keys: int; Type:      coold; Time: 3.35e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: str; Type:       dict; Time: 6.10e-06; Sigma: 2e-07
Name: `o.copy()`;               Size: 1000; Keys: str; Type:      coold; Time: 3.35e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.46e-06; Sigma: 2e-07
Name: `o.copy()`;               Size: 1000; Keys: int; Type:      coold; Time: 3.35e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: str; Type:       dict; Time: 7.21e-08; Sigma: 3e-10
Name: `o == o`;                 Size:    5; Keys: str; Type:      coold; Time: 2.78e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: int; Type:       dict; Time: 7.27e-08; Sigma: 1e-09
Name: `o == o`;                 Size:    5; Keys: int; Type:      coold; Time: 2.78e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.36e-05; Sigma: 2e-07
Name: `o == o`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.78e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.00e-05; Sigma: 7e-08
Name: `o == o`;                 Size: 1000; Keys: int; Type:      coold; Time: 2.78e-08; Sigma: 9e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: str; Type:       dict; Time: 7.91e-08; Sigma: 1e-09
Name: `for x in o`;             Size:    5; Keys: str; Type:      coold; Time: 7.08e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: int; Type:       dict; Time: 7.91e-08; Sigma: 1e-09
Name: `for x in o`;             Size:    5; Keys: int; Type:      coold; Time: 7.08e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: str; Type:       dict; Time: 9.82e-06; Sigma: 4e-08
Name: `for x in o`;             Size: 1000; Keys: str; Type:      coold; Time: 8.10e-06; Sigma: 3e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: int; Type:       dict; Time: 9.79e-06; Sigma: 3e-08
Name: `for x in o`;             Size: 1000; Keys: int; Type:      coold; Time: 8.07e-06; Sigma: 3e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:       dict; Time: 8.22e-08; Sigma: 1e-09
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:      coold; Time: 6.83e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:       dict; Time: 8.24e-08; Sigma: 1e-09
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:      coold; Time: 6.83e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:       dict; Time: 1.07e-05; Sigma: 4e-08
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:      coold; Time: 8.13e-06; Sigma: 3e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:       dict; Time: 1.07e-05; Sigma: 3e-08
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:      coold; Time: 8.07e-06; Sigma: 2e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:       dict; Time: 1.19e-07; Sigma: 3e-09
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:      coold; Time: 1.20e-07; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:       dict; Time: 1.21e-07; Sigma: 3e-09
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:      coold; Time: 1.21e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:       dict; Time: 1.64e-05; Sigma: 4e-07
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:      coold; Time: 1.64e-05; Sigma: 2e-07
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:       dict; Time: 1.65e-05; Sigma: 4e-07
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:      coold; Time: 1.65e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:       dict; Time: 6.50e-07; Sigma: 3e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:      coold; Time: 2.76e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:       dict; Time: 4.59e-07; Sigma: 3e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:      coold; Time: 2.56e-06; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:       dict; Time: 1.26e-04; Sigma: 2e-06
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:      coold; Time: 1.93e-04; Sigma: 3e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:       dict; Time: 2.88e-05; Sigma: 5e-07
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:      coold; Time: 7.31e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:       dict; Time: 8.95e-07; Sigma: 2e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:      coold; Time: 2.07e-06; Sigma: 5e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:       dict; Time: 4.46e-07; Sigma: 1e-08
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:      coold; Time: 1.62e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:       dict; Time: 1.56e-04; Sigma: 7e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:      coold; Time: 2.21e-04; Sigma: 7e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:       dict; Time: 5.61e-05; Sigma: 1e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:      coold; Time: 1.00e-04; Sigma: 3e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:       dict; Time: 1.84e-07; Sigma: 6e-09
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:      coold; Time: 2.15e-07; Sigma: 9e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:       dict; Time: 2.10e-07; Sigma: 6e-09
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:      coold; Time: 2.31e-07; Sigma: 6e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:       dict; Time: 3.99e-05; Sigma: 7e-07
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:      coold; Time: 3.83e-05; Sigma: 5e-07
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:       dict; Time: 2.96e-05; Sigma: 5e-07
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:      coold; Time: 2.90e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size:    5; Keys: str; Type:       dict; Time: 7.65e-08; Sigma: 1e-09
Name: `for x in o.keys()`;      Size:    5; Keys: str; Type:      coold; Time: 6.91e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size:    5; Keys: int; Type:       dict; Time: 7.65e-08; Sigma: 1e-09
Name: `for x in o.keys()`;      Size:    5; Keys: int; Type:      coold; Time: 6.86e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size: 1000; Keys: str; Type:       dict; Time: 9.81e-06; Sigma: 3e-08
Name: `for x in o.keys()`;      Size: 1000; Keys: str; Type:      coold; Time: 8.09e-06; Sigma: 3e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.keys()`;      Size: 1000; Keys: int; Type:       dict; Time: 9.81e-06; Sigma: 3e-08
Name: `for x in o.keys()`;      Size: 1000; Keys: int; Type:      coold; Time: 8.07e-06; Sigma: 2e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size:    5; Keys: str; Type:       dict; Time: 1.00e-07; Sigma: 3e-09
Name: `for x in iter(o)`;       Size:    5; Keys: str; Type:      coold; Time: 9.19e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size:    5; Keys: int; Type:       dict; Time: 1.00e-07; Sigma: 3e-09
Name: `for x in iter(o)`;       Size:    5; Keys: int; Type:      coold; Time: 9.20e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size: 1000; Keys: str; Type:       dict; Time: 9.85e-06; Sigma: 3e-08
Name: `for x in iter(o)`;       Size: 1000; Keys: str; Type:      coold; Time: 8.13e-06; Sigma: 4e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in iter(o)`;       Size: 1000; Keys: int; Type:       dict; Time: 9.82e-06; Sigma: 4e-08
Name: `for x in iter(o)`;       Size: 1000; Keys: int; Type:      coold; Time: 8.10e-06; Sigma: 3e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size:    5; Keys: str; Type:       dict; Time: 7.45e-08; Sigma: 6e-10
Name: `o == d`;                 Size:    5; Keys: str; Type:      coold; Time: 7.96e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size:    5; Keys: int; Type:       dict; Time: 7.30e-08; Sigma: 8e-10
Name: `o == d`;                 Size:    5; Keys: int; Type:      coold; Time: 8.90e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.37e-05; Sigma: 2e-07
Name: `o == d`;                 Size: 1000; Keys: str; Type:      coold; Time: 1.58e-05; Sigma: 2e-07
////////////////////////////////////////////////////////////////////////////////
Name: `o == d`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.01e-05; Sigma: 7e-08
Name: `o == d`;                 Size: 1000; Keys: int; Type:      coold; Time: 1.20e-05; Sigma: 1e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size:    5; Keys: str; Type:       dict; Time: 2.95e-08; Sigma: 5e-09
Name: `o.get(key)`;             Size:    5; Keys: str; Type:      coold; Time: 2.98e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size:    5; Keys: int; Type:       dict; Time: 2.89e-08; Sigma: 4e-09
Name: `o.get(key)`;             Size:    5; Keys: int; Type:      coold; Time: 2.90e-08; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size: 1000; Keys: str; Type:       dict; Time: 3.09e-08; Sigma: 3e-09
Name: `o.get(key)`;             Size: 1000; Keys: str; Type:      coold; Time: 3.04e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.get(key)`;             Size: 1000; Keys: int; Type:       dict; Time: 2.98e-08; Sigma: 4e-09
Name: `o.get(key)`;             Size: 1000; Keys: int; Type:      coold; Time: 2.95e-08; Sigma: 4e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size:    5; Keys: str; Type:       dict; Time: 2.81e-08; Sigma: 6e-10
Name: `o[key]`;                 Size:    5; Keys: str; Type:      coold; Time: 2.81e-08; Sigma: 7e-10
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size:    5; Keys: int; Type:       dict; Time: 2.97e-08; Sigma: 6e-10
Name: `o[key]`;                 Size:    5; Keys: int; Type:      coold; Time: 3.03e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size: 1000; Keys: str; Type:       dict; Time: 2.84e-08; Sigma: 6e-10
Name: `o[key]`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.75e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o[key]`;                 Size: 1000; Keys: int; Type:       dict; Time: 3.05e-08; Sigma: 8e-10
Name: `o[key]`;                 Size: 1000; Keys: int; Type:      coold; Time: 3.07e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size:    5; Keys: str; Type:       dict; Time: 2.29e-08; Sigma: 4e-09
Name: `key in o`;               Size:    5; Keys: str; Type:      coold; Time: 2.32e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size:    5; Keys: int; Type:       dict; Time: 2.26e-08; Sigma: 5e-09
Name: `key in o`;               Size:    5; Keys: int; Type:      coold; Time: 2.22e-08; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size: 1000; Keys: str; Type:       dict; Time: 2.44e-08; Sigma: 3e-09
Name: `key in o`;               Size: 1000; Keys: str; Type:      coold; Time: 2.35e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key in o`;               Size: 1000; Keys: int; Type:       dict; Time: 2.38e-08; Sigma: 3e-09
Name: `key in o`;               Size: 1000; Keys: int; Type:      coold; Time: 2.33e-08; Sigma: 3e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size:    5; Keys: str; Type:       dict; Time: 2.29e-08; Sigma: 4e-09
Name: `key not in o`;           Size:    5; Keys: str; Type:      coold; Time: 2.32e-08; Sigma: 4e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size:    5; Keys: int; Type:       dict; Time: 2.26e-08; Sigma: 5e-09
Name: `key not in o`;           Size:    5; Keys: int; Type:      coold; Time: 2.23e-08; Sigma: 5e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size: 1000; Keys: str; Type:       dict; Time: 2.44e-08; Sigma: 3e-09
Name: `key not in o`;           Size: 1000; Keys: str; Type:      coold; Time: 2.38e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `key not in o`;           Size: 1000; Keys: int; Type:       dict; Time: 2.38e-08; Sigma: 3e-09
Name: `key not in o`;           Size: 1000; Keys: int; Type:      coold; Time: 2.35e-08; Sigma: 3e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size:    5; Keys: str; Type:      coold; Time: 4.17e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size:    5; Keys: int; Type:      coold; Time: 4.19e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 4.15e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `hash(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 4.15e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size:    5; Keys: str; Type:       dict; Time: 3.21e-08; Sigma: 2e-09
Name: `len(o)`;                 Size:    5; Keys: str; Type:      coold; Time: 3.21e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size:    5; Keys: int; Type:       dict; Time: 3.21e-08; Sigma: 2e-09
Name: `len(o)`;                 Size:    5; Keys: int; Type:      coold; Time: 3.21e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size: 1000; Keys: str; Type:       dict; Time: 3.95e-08; Sigma: 2e-09
Name: `len(o)`;                 Size: 1000; Keys: str; Type:      coold; Time: 3.95e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `len(o)`;                 Size: 1000; Keys: int; Type:       dict; Time: 3.95e-08; Sigma: 2e-09
Name: `len(o)`;                 Size: 1000; Keys: int; Type:      coold; Time: 3.95e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size:    5; Keys: str; Type:       dict; Time: 3.27e-08; Sigma: 2e-09
Name: `o.keys()`;               Size:    5; Keys: str; Type:      coold; Time: 3.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size:    5; Keys: int; Type:       dict; Time: 3.27e-08; Sigma: 2e-09
Name: `o.keys()`;               Size:    5; Keys: int; Type:      coold; Time: 3.41e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size: 1000; Keys: str; Type:       dict; Time: 3.26e-08; Sigma: 2e-09
Name: `o.keys()`;               Size: 1000; Keys: str; Type:      coold; Time: 3.45e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.keys()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.27e-08; Sigma: 2e-09
Name: `o.keys()`;               Size: 1000; Keys: int; Type:      coold; Time: 3.41e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size:    5; Keys: str; Type:       dict; Time: 3.23e-08; Sigma: 2e-09
Name: `o.values()`;             Size:    5; Keys: str; Type:      coold; Time: 3.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size:    5; Keys: int; Type:       dict; Time: 3.23e-08; Sigma: 2e-09
Name: `o.values()`;             Size:    5; Keys: int; Type:      coold; Time: 3.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size: 1000; Keys: str; Type:       dict; Time: 3.24e-08; Sigma: 2e-09
Name: `o.values()`;             Size: 1000; Keys: str; Type:      coold; Time: 3.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.values()`;             Size: 1000; Keys: int; Type:       dict; Time: 3.23e-08; Sigma: 2e-09
Name: `o.values()`;             Size: 1000; Keys: int; Type:      coold; Time: 3.44e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size:    5; Keys: str; Type:       dict; Time: 3.22e-08; Sigma: 2e-09
Name: `o.items()`;              Size:    5; Keys: str; Type:      coold; Time: 3.50e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size:    5; Keys: int; Type:       dict; Time: 3.18e-08; Sigma: 3e-09
Name: `o.items()`;              Size:    5; Keys: int; Type:      coold; Time: 3.50e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size: 1000; Keys: str; Type:       dict; Time: 3.24e-08; Sigma: 2e-09
Name: `o.items()`;              Size: 1000; Keys: str; Type:      coold; Time: 3.48e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.items()`;              Size: 1000; Keys: int; Type:       dict; Time: 3.24e-08; Sigma: 2e-09
Name: `o.items()`;              Size: 1000; Keys: int; Type:      coold; Time: 3.50e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size:    5; Keys: str; Type:       dict; Time: 4.44e-08; Sigma: 2e-09
Name: `iter(o)`;                Size:    5; Keys: str; Type:      coold; Time: 4.69e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size:    5; Keys: int; Type:       dict; Time: 4.44e-08; Sigma: 2e-09
Name: `iter(o)`;                Size:    5; Keys: int; Type:      coold; Time: 4.67e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size: 1000; Keys: str; Type:       dict; Time: 4.44e-08; Sigma: 2e-09
Name: `iter(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 4.70e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `iter(o)`;                Size: 1000; Keys: int; Type:       dict; Time: 4.44e-08; Sigma: 2e-09
Name: `iter(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 4.70e-08; Sigma: 1e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size:    5; Keys: str; Type:       dict; Time: 1.83e-06; Sigma: 4e-08
Name: `repr(o)`;                Size:    5; Keys: str; Type:      coold; Time: 2.14e-06; Sigma: 8e-08
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size:    5; Keys: int; Type:       dict; Time: 7.60e-07; Sigma: 7e-09
Name: `repr(o)`;                Size:    5; Keys: int; Type:      coold; Time: 9.24e-07; Sigma: 1e-08
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size: 1000; Keys: str; Type:       dict; Time: 2.71e-04; Sigma: 5e-06
Name: `repr(o)`;                Size: 1000; Keys: str; Type:      coold; Time: 2.90e-04; Sigma: 2e-05
////////////////////////////////////////////////////////////////////////////////
Name: `repr(o)`;                Size: 1000; Keys: int; Type:       dict; Time: 1.22e-04; Sigma: 1e-06
Name: `repr(o)`;                Size: 1000; Keys: int; Type:      coold; Time: 1.23e-04; Sigma: 5e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size:    5; Keys: str; Type:       dict; Time: 1.86e-06; Sigma: 5e-08
Name: `str(o)`;                 Size:    5; Keys: str; Type:      coold; Time: 2.17e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size:    5; Keys: int; Type:       dict; Time: 7.93e-07; Sigma: 5e-09
Name: `str(o)`;                 Size:    5; Keys: int; Type:      coold; Time: 9.51e-07; Sigma: 2e-08
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size: 1000; Keys: str; Type:       dict; Time: 2.73e-04; Sigma: 5e-06
Name: `str(o)`;                 Size: 1000; Keys: str; Type:      coold; Time: 2.88e-04; Sigma: 3e-05
////////////////////////////////////////////////////////////////////////////////
Name: `str(o)`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.22e-04; Sigma: 1e-06
Name: `str(o)`;                 Size: 1000; Keys: int; Type:      coold; Time: 1.23e-04; Sigma: 5e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size:    5; Keys: str; Type:       dict; Time: 3.50e-08; Sigma: 2e-09
Name: `set`;                    Size:    5; Keys: str; Type:      coold; Time: 1.26e-07; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size:    5; Keys: int; Type:       dict; Time: 3.61e-08; Sigma: 2e-09
Name: `set`;                    Size:    5; Keys: int; Type:      coold; Time: 1.28e-07; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size: 1000; Keys: str; Type:       dict; Time: 3.53e-08; Sigma: 2e-09
Name: `set`;                    Size: 1000; Keys: str; Type:      coold; Time: 6.20e-06; Sigma: 5e-07
////////////////////////////////////////////////////////////////////////////////
Name: `set`;                    Size: 1000; Keys: int; Type:       dict; Time: 3.70e-08; Sigma: 2e-09
Name: `set`;                    Size: 1000; Keys: int; Type:      coold; Time: 3.61e-06; Sigma: 2e-07
################################################################################
```

[1] Benchmarks done under Linux 64 bit, Python 3.10, using the C Extension.
