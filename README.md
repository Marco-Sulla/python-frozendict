# frozendict
### Table of Contents
* [Introduction](#introduction)
* [API](#api)
* [Examples](#examples)
* [Building](#building)
* [Benchmarks](#benchmarks)

# Introduction
Welcome, fellow programmer!

`frozendict` is a simple immutable dictionary. It's fast as `dict`, and 
[sometimes faster](https://github.com/Marco-Sulla/python-frozendict#benchmarks)!

Unlike other similar implementations, immutability is guaranteed: you can't 
change the internal variables of the class, and they are all immutable 
objects.  Reinvoking `__init__` does not alter the object.

The API is the same as `dict`, without methods that can change the 
immutability. So it supports also `fromkeys`, unlike other implementations. 
Furthermore it can be `pickle`d, un`pickle`d and have an hash, if all values 
are hashable.

You can also add any `dict` to a `frozendict` using the `|` operator. The result is a new `frozendict`.

# API
The API is the same of `dict` of Python 3.10, without the methods and operands which alter the map. Additionally, `frozendict` supports these methods:

### `__hash__()`

If all the values of the `frozendict` are hashable, returns an hash, otherwise raises a TypeError.

### `set(key, value)`

It returns a new `frozendict`. If key is already in the original `frozendict`, the new one will have it with the new value associated. Otherwise, the new `frozendict` will contain the new (key, value) item.

### `delete(key)`

It returns a new `frozendict` without the item corresponding to the key. If the key is not present, a KeyError is raised.

### `setdefault(key[, default])`

If key is already in `frozendict`, the object itself is returned unchanged. Otherwise, the new `frozendict` will contain the new (key, default) item. The parameter default defaults to None.

### `key([index])`

It returns the key at the specified index (determined by the insertion order). If index is not passed, it defaults to 0. If the index is negative, the position will be the size of the `frozendict` + index

### `value([index])`
Same as `key(index)`, but it returns the value at the given index.

### `item([index])`
Same as `key(index)`, but it returns a tuple with (key, value) at the given index.

# Examples

```python
from frozendict import frozendict

fd = frozendict({"Guzzanti": "Corrado", "Hicks": "Bill"})

print(fd)
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})

print(fd["Guzzanti"])
# Corrado

fd["Brignano"]
# KeyError: 'Brignano'

len(fd)
# 2

"Guzzanti" in fd
# True

"Guzzanti" not in fd
# False

"Brignano" in fd
# False

hash(fd)
# 5833699487320513741

fd_unhashable = frozendict({1: []})
hash(fd_unhashable)
# TypeError: Not all values are hashable.

fd | {1: 2}
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})

fd5 = frozendict(fd)
id_fd5 = id(fd5)
fd5 |= {1: 2}
fd5
# frozendict.frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})
id(fd5) != id_fd5
# True

fd.set(1, 2)
# frozendict.frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})

fd.set("Guzzanti", "Sabina")
# frozendict.frozendict({'Guzzanti': 'Sabina', 'Hicks': 'Bill'})

fd.delete("Guzzanti")
# frozendict.frozendict({'Hicks': 'Bill'})

fd.setdefault("Guzzanti", "Sabina")
# frozendict.frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})

fd.setdefault(1, 2)
# frozendict.frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})

fd.key()
# 'Guzzanti'

fd.value(1)
# 'Bill'

fd.item(-1)
# (1, 2)

fd2 = fd.copy()
fd2 == fd
# True

fd3 = frozendict(fd)
fd3 == fd
# True

fd4 = frozendict({"Hicks": "Bill", "Guzzanti": "Corrado"})

print(fd4)
# frozendict({'Hicks': 'Bill', 'Guzzanti': 'Corrado'})

fd4 == fd
# True

import pickle
fd_unpickled = pickle.loads(pickle.dumps(fd))
print(fd_unpickled)
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})
fd_unpickled == fd
# True

frozendict(Guzzanti="Corrado", Hicks="Bill")
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'}

frozendict((("Guzzanti", "Corrado"), ("Hicks", "Bill")))
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})

fd.get("Guzzanti")
# 'Corrado'

print(fd.get("Brignano"))
# None

tuple(fd.keys())
# ('Guzzanti', 'Hicks')

tuple(fd.values())
# ('Corrado', 'Bill')

tuple(fd.items())
# (('Guzzanti', 'Corrado'), ('Hicks', 'Bill'))

frozendict.fromkeys(["Corrado", "Sabina"], "Guzzanti")
# frozendict({'Corrado': 'Guzzanti', 'Sabina': 'Guzzanti'})

iter(fd)
# <dict_keyiterator object at 0x7feb75c49188>

fd["Guzzanti"] = "Caterina"
# TypeError: 'frozendict' object doesn't support item assignment
```

# Building
You can build `frozendict` directly from the code, using

```
python3 setup.py bdist_wheel
```

The C Extension is not optional by default. You can build the pure py package using the `py` custom argument:

```
python3 setup.py py bdist_wheel
```

# Benchmarks

Some benchmarks between `dict` and `frozendict`[1]:

```
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: str; Type:       dict; Time: 8.02e-08; Sigma: 4e-09
Name: `constructor(d)`;         Size:    5; Keys: str; Type: frozendict; Time: 8.81e-08; Sigma: 3e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size:    5; Keys: int; Type:       dict; Time: 7.96e-08; Sigma: 5e-09
Name: `constructor(d)`;         Size:    5; Keys: int; Type: frozendict; Time: 8.97e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: str; Type:       dict; Time: 6.38e-06; Sigma: 9e-08
Name: `constructor(d)`;         Size: 1000; Keys: str; Type: frozendict; Time: 6.21e-06; Sigma: 2e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(d)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.49e-06; Sigma: 3e-07
Name: `constructor(d)`;         Size: 1000; Keys: int; Type: frozendict; Time: 3.48e-06; Sigma: 2e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type:       dict; Time: 2.40e-07; Sigma: 1e-09
Name: `constructor(kwargs)`;    Size:    5; Keys: str; Type: frozendict; Time: 2.48e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type:       dict; Time: 4.80e-05; Sigma: 1e-06
Name: `constructor(kwargs)`;    Size: 1000; Keys: str; Type: frozendict; Time: 2.90e-05; Sigma: 7e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type:       dict; Time: 2.01e-07; Sigma: 9e-10
Name: `constructor(seq2)`;      Size:    5; Keys: str; Type: frozendict; Time: 2.50e-07; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type:       dict; Time: 2.18e-07; Sigma: 2e-09
Name: `constructor(seq2)`;      Size:    5; Keys: int; Type: frozendict; Time: 2.73e-07; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type:       dict; Time: 4.29e-05; Sigma: 6e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: str; Type: frozendict; Time: 4.33e-05; Sigma: 6e-07
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type:       dict; Time: 3.04e-05; Sigma: 4e-07
Name: `constructor(seq2)`;      Size: 1000; Keys: int; Type: frozendict; Time: 3.45e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: str; Type:       dict; Time: 7.93e-08; Sigma: 3e-09
Name: `constructor(o)`;         Size:    5; Keys: str; Type: frozendict; Time: 2.41e-08; Sigma: 6e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size:    5; Keys: int; Type:       dict; Time: 7.94e-08; Sigma: 5e-09
Name: `constructor(o)`;         Size:    5; Keys: int; Type: frozendict; Time: 2.41e-08; Sigma: 6e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: str; Type:       dict; Time: 6.18e-06; Sigma: 3e-07
Name: `constructor(o)`;         Size: 1000; Keys: str; Type: frozendict; Time: 2.41e-08; Sigma: 6e-10
////////////////////////////////////////////////////////////////////////////////
Name: `constructor(o)`;         Size: 1000; Keys: int; Type:       dict; Time: 3.47e-06; Sigma: 2e-07
Name: `constructor(o)`;         Size: 1000; Keys: int; Type: frozendict; Time: 2.41e-08; Sigma: 6e-10
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: str; Type:       dict; Time: 7.28e-08; Sigma: 2e-09
Name: `o.copy()`;               Size:    5; Keys: str; Type: frozendict; Time: 3.18e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size:    5; Keys: int; Type:       dict; Time: 7.21e-08; Sigma: 4e-09
Name: `o.copy()`;               Size:    5; Keys: int; Type: frozendict; Time: 3.32e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: str; Type:       dict; Time: 6.16e-06; Sigma: 3e-07
Name: `o.copy()`;               Size: 1000; Keys: str; Type: frozendict; Time: 3.18e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o.copy()`;               Size: 1000; Keys: int; Type:       dict; Time: 3.46e-06; Sigma: 1e-07
Name: `o.copy()`;               Size: 1000; Keys: int; Type: frozendict; Time: 3.18e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: str; Type:       dict; Time: 7.23e-08; Sigma: 8e-10
Name: `o == o`;                 Size:    5; Keys: str; Type: frozendict; Time: 2.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size:    5; Keys: int; Type:       dict; Time: 7.30e-08; Sigma: 1e-09
Name: `o == o`;                 Size:    5; Keys: int; Type: frozendict; Time: 2.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: str; Type:       dict; Time: 1.38e-05; Sigma: 1e-07
Name: `o == o`;                 Size: 1000; Keys: str; Type: frozendict; Time: 2.44e-08; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `o == o`;                 Size: 1000; Keys: int; Type:       dict; Time: 1.05e-05; Sigma: 7e-08
Name: `o == o`;                 Size: 1000; Keys: int; Type: frozendict; Time: 2.44e-08; Sigma: 2e-09
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: str; Type:       dict; Time: 7.33e-08; Sigma: 2e-09
Name: `for x in o`;             Size:    5; Keys: str; Type: frozendict; Time: 6.70e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size:    5; Keys: int; Type:       dict; Time: 7.33e-08; Sigma: 2e-09
Name: `for x in o`;             Size:    5; Keys: int; Type: frozendict; Time: 6.70e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: str; Type:       dict; Time: 8.84e-06; Sigma: 5e-08
Name: `for x in o`;             Size: 1000; Keys: str; Type: frozendict; Time: 7.06e-06; Sigma: 6e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o`;             Size: 1000; Keys: int; Type:       dict; Time: 8.67e-06; Sigma: 7e-08
Name: `for x in o`;             Size: 1000; Keys: int; Type: frozendict; Time: 6.94e-06; Sigma: 3e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: str; Type:       dict; Time: 7.28e-08; Sigma: 9e-10
Name: `for x in o.values()`;    Size:    5; Keys: str; Type: frozendict; Time: 6.48e-08; Sigma: 8e-10
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size:    5; Keys: int; Type:       dict; Time: 7.25e-08; Sigma: 1e-09
Name: `for x in o.values()`;    Size:    5; Keys: int; Type: frozendict; Time: 6.45e-08; Sigma: 1e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type:       dict; Time: 9.06e-06; Sigma: 5e-07
Name: `for x in o.values()`;    Size: 1000; Keys: str; Type: frozendict; Time: 7.04e-06; Sigma: 4e-08
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type:       dict; Time: 9.53e-06; Sigma: 3e-08
Name: `for x in o.values()`;    Size: 1000; Keys: int; Type: frozendict; Time: 6.97e-06; Sigma: 3e-08
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: str; Type:       dict; Time: 1.13e-07; Sigma: 3e-09
Name: `for x in o.items()`;     Size:    5; Keys: str; Type: frozendict; Time: 1.16e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size:    5; Keys: int; Type:       dict; Time: 1.14e-07; Sigma: 3e-09
Name: `for x in o.items()`;     Size:    5; Keys: int; Type: frozendict; Time: 1.17e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type:       dict; Time: 1.53e-05; Sigma: 3e-07
Name: `for x in o.items()`;     Size: 1000; Keys: str; Type: frozendict; Time: 1.53e-05; Sigma: 4e-07
////////////////////////////////////////////////////////////////////////////////
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type:       dict; Time: 1.53e-05; Sigma: 3e-07
Name: `for x in o.items()`;     Size: 1000; Keys: int; Type: frozendict; Time: 1.55e-05; Sigma: 4e-07
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type:       dict; Time: 6.82e-07; Sigma: 2e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: str; Type: frozendict; Time: 2.86e-06; Sigma: 1e-07
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type:       dict; Time: 4.77e-07; Sigma: 2e-08
Name: `pickle.dumps(o)`;        Size:    5; Keys: int; Type: frozendict; Time: 2.72e-06; Sigma: 8e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type:       dict; Time: 1.24e-04; Sigma: 4e-06
Name: `pickle.dumps(o)`;        Size: 1000; Keys: str; Type: frozendict; Time: 1.92e-04; Sigma: 5e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type:       dict; Time: 2.81e-05; Sigma: 6e-07
Name: `pickle.dumps(o)`;        Size: 1000; Keys: int; Type: frozendict; Time: 7.37e-05; Sigma: 1e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type:       dict; Time: 9.08e-07; Sigma: 6e-09
Name: `pickle.loads(dump)`;     Size:    5; Keys: str; Type: frozendict; Time: 1.79e-06; Sigma: 9e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type:       dict; Time: 4.46e-07; Sigma: 6e-09
Name: `pickle.loads(dump)`;     Size:    5; Keys: int; Type: frozendict; Time: 1.32e-06; Sigma: 7e-08
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type:       dict; Time: 1.57e-04; Sigma: 8e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: str; Type: frozendict; Time: 1.69e-04; Sigma: 7e-06
////////////////////////////////////////////////////////////////////////////////
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type:       dict; Time: 5.97e-05; Sigma: 5e-06
Name: `pickle.loads(dump)`;     Size: 1000; Keys: int; Type: frozendict; Time: 6.68e-05; Sigma: 2e-06
################################################################################
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type:       dict; Time: 1.88e-07; Sigma: 1e-09
Name: `class.fromkeys()`;       Size:    5; Keys: str; Type: frozendict; Time: 2.22e-07; Sigma: 7e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type:       dict; Time: 2.08e-07; Sigma: 6e-09
Name: `class.fromkeys()`;       Size:    5; Keys: int; Type: frozendict; Time: 2.44e-07; Sigma: 2e-09
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type:       dict; Time: 4.05e-05; Sigma: 4e-06
Name: `class.fromkeys()`;       Size: 1000; Keys: str; Type: frozendict; Time: 3.84e-05; Sigma: 5e-07
////////////////////////////////////////////////////////////////////////////////
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type:       dict; Time: 2.93e-05; Sigma: 7e-07
Name: `class.fromkeys()`;       Size: 1000; Keys: int; Type: frozendict; Time: 3.08e-05; Sigma: 2e-06
################################################################################
```

[1] Benchmarks done under Linux 64 bit, Python 3.10.2, using the C Extension.
