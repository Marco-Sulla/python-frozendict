# frozendict
### Table of Contents
* [Introduction](#introduction)
* [Install](#install)
* [API](#api)
  * [frozendict API](#frozendict-api)
  * [deepfreeze API](#deepfreeze-api)
* [Examples](#examples)
  * [frozendict examples](#frozendict-examples)
  * [deepfreeze examples](#deepfreeze-examples)
* [Building](#building)
* [Benchmarks](#benchmarks)

# Introduction
Welcome, fellow programmer, to the house of `frozendict` and 
[deepfreeze](#deepfreeze-api)!

`frozendict` is a simple immutable dictionary. It's fast as `dict`, and 
[sometimes faster](https://github.com/Marco-Sulla/python-frozendict#benchmarks)!

Unlike other similar implementations, immutability is guaranteed: you can't 
change the internal variables of the class, and they are all immutable 
objects.  Reinvoking `__init__` does not alter the object.

The API is the same as `dict`, without methods that can change the 
immutability. So it supports also `fromkeys`, unlike other implementations. 
Furthermore, it can be `pickle`d, un`pickle`d and have a hash, if all values 
are hashable.

You can also add any `dict` to a `frozendict` using the `|` operator. The result is a new `frozendict`.

# Install

You can install `frozendict` by simply typing in a command line:

```bash
pip install frozendict
```

The C Extension is optional by default from version 2.3.5. You can make it mandatory using:

```bash
CIBUILDWHEEL=1 pip install frozendict
```

On the contrary, if you want the pure py implementation:

```bash
FROZENDICT_PURE_PY=1 pip install frozendict
```

# API

## frozendict API
The API is the same of `dict` of Python 3.10, without the methods and operands which alter the map. Additionally, `frozendict` supports these methods:

### `__hash__()`

If all the values of the `frozendict` are hashable, returns a hash, otherwise raises a TypeError.

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

## deepfreeze API

The `frozendict` _module_ has also these static methods:

### `frozendict.deepfreeze(o, custom_converters = None, custom_inverse_converters = None)`
Converts the object and all the objects nested in it, into their immutable
counterparts.

The conversion map is in `getFreezeConversionMap()`.

You can register a new conversion using `register()` You can also 
pass a map of custom converters with `custom_converters` and a map 
of custom inverse converters with `custom_inverse_converters`, 
without using `register()`.

By default, if the type is not registered and has a `__dict__` 
attribute, it's converted to the `frozendict` of that `__dict__`.

This function assumes that hashable == immutable (that is not 
always true).

This function uses recursion, with all the limits of recursions in 
Python.

Where is a good old tail call when you need it?

### `frozendict.register(to_convert, converter, *, inverse = False)`

Adds a `converter` for a type `to_convert`. `converter`
must be callable. The new converter will be used by `deepfreeze()`
and has precedence over any previous converter. 

If `to_covert` has already a converter, a FreezeWarning is raised.

If `inverse` is True, the conversion is considered from an immutable 
type to a mutable one. This make it possible to convert mutable 
objects nested in the registered immutable one.

### `frozendict.unregister(type, inverse = False)`
Unregister a type from custom conversion. If `inverse` is `True`, 
the unregistered conversion is an inverse conversion 
(see `register()`).

# Examples

## frozendict examples
```python
from frozendict import frozendict

fd = frozendict(Guzzanti = "Corrado", Hicks = "Bill")

print(fd)
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})

frozendict({"Guzzanti": "Corrado", "Hicks": "Bill"})
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill'})

hash(fd)
# 5833699487320513741

fd_unhashable = frozendict({1: []})
hash(fd_unhashable)
# TypeError: Not all values are hashable.

frozendict({frozendict(nested = 4, key = 2): 42})
# frozendict({frozendict({'nested': 4, 'key': 2}): 42})

fd | {1: 2}
# frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})

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

fd5 = frozendict(fd)
id_fd5 = id(fd5)
fd5 |= {1: 2}
fd5
# frozendict.frozendict({'Guzzanti': 'Corrado', 'Hicks': 'Bill', 1: 2})
id(fd5) != id_fd5
# True

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

## deepfreeze examples
```python
import frozendict as cool

from frozendict import frozendict
from array import array
from collections import OrderedDict
from types import MappingProxyType

class A:
    def __init__(self, x):
        self.x = x

a = A(3)
        
o = {"x": [
    5, 
    frozendict(y = {5, "b", memoryview(b"b")}), 
    array("B", (0, 1, 2)), 
    OrderedDict(a=bytearray(b"a")),
    MappingProxyType({2: []}),
    a
]}

cool.deepfreeze(o)
# frozendict(x = (
#     5, 
#     frozendict(y = frozenset({5, "b", memoryview(b"b")})), 
#     (0, 1, 2), 
#     frozendict(a = b'a'),
#     MappingProxyType({2: ()}),
#     frozendict(x = 3),
# ))

```

# Building
You can build `frozendict` directly from the code, using

```
python3 setup.py bdist_wheel
```

The C Extension is optional by default from version 2.3.5. You can make it mandatory by passing the environment variable `CIBUILDWHEEL` with value `1`

On the contrary, if you want the pure py implementation, you can pass the env var `FROZENDICT_PURE_PY` with value `1`

# Benchmarks

Some benchmarks between `dict`, `frozendict` and `immutables.Map` [1].
`init(d)` means construction from a dict.
`init(kwargs)` means construction from keyword arguments (e.g. `frozendict(a=1, b=2)`).
`init(o)` means constructor applied to the object itself.
`init(holes)` means construction from a dict with holes.


```
################################################################################
Seed: 0
################################################################################
////////////////////////////////////////////////////////////////////////////////
init(d)     ; Size:    5; Keys: str; Type:       dict; Time: 8.72e-08; CV: 2e-01
init(d)     ; Size:    5; Keys: str; Type: frozendict; Time: 8.23e-08; CV: 2e-01
init(d)     ; Size:    5; Keys: str; Type:        Map; Time: 4.64e-07; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
init(d)     ; Size:    5; Keys: int; Type:       dict; Time: 9.16e-08; CV: 8e-02
init(d)     ; Size:    5; Keys: int; Type: frozendict; Time: 8.01e-08; CV: 5e-01
init(d)     ; Size:    5; Keys: int; Type:        Map; Time: 4.83e-07; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
init(d)     ; Size: 5000; Keys: str; Type:       dict; Time: 3.43e-05; CV: 6e-02
init(d)     ; Size: 5000; Keys: str; Type: frozendict; Time: 3.44e-05; CV: 2e-01
init(d)     ; Size: 5000; Keys: str; Type:        Map; Time: 7.82e-04; CV: 7e-02
////////////////////////////////////////////////////////////////////////////////
init(d)     ; Size: 5000; Keys: int; Type:       dict; Time: 1.50e-05; CV: 4e-02
init(d)     ; Size: 5000; Keys: int; Type: frozendict; Time: 1.55e-05; CV: 1e-01
init(d)     ; Size: 5000; Keys: int; Type:        Map; Time: 5.06e-04; CV: 1e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
init(kwargs); Size:    5; Keys: str; Type:       dict; Time: 1.89e-07; CV: 1e-01
init(kwargs); Size:    5; Keys: str; Type: frozendict; Time: 1.63e-07; CV: 2e-01
init(kwargs); Size:    5; Keys: str; Type:        Map; Time: 6.03e-07; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
init(kwargs); Size: 5000; Keys: str; Type:       dict; Time: 4.61e-04; CV: 7e-02
init(kwargs); Size: 5000; Keys: str; Type: frozendict; Time: 3.70e-04; CV: 4e-02
init(kwargs); Size: 5000; Keys: str; Type:        Map; Time: 1.04e-03; CV: 1e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
init(seq2)  ; Size:    5; Keys: str; Type:       dict; Time: 2.45e-07; CV: 1e-01
init(seq2)  ; Size:    5; Keys: str; Type: frozendict; Time: 2.67e-07; CV: 5e-02
init(seq2)  ; Size:    5; Keys: str; Type:        Map; Time: 4.22e-07; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
init(seq2)  ; Size:    5; Keys: int; Type:       dict; Time: 2.45e-07; CV: 2e-01
init(seq2)  ; Size:    5; Keys: int; Type: frozendict; Time: 2.82e-07; CV: 4e-02
init(seq2)  ; Size:    5; Keys: int; Type:        Map; Time: 4.22e-07; CV: 9e-02
////////////////////////////////////////////////////////////////////////////////
init(seq2)  ; Size: 5000; Keys: str; Type:       dict; Time: 2.25e-04; CV: 4e-01
init(seq2)  ; Size: 5000; Keys: str; Type: frozendict; Time: 2.34e-04; CV: 1e-01
init(seq2)  ; Size: 5000; Keys: str; Type:        Map; Time: 6.93e-04; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
init(seq2)  ; Size: 5000; Keys: int; Type:       dict; Time: 1.53e-04; CV: 2e-01
init(seq2)  ; Size: 5000; Keys: int; Type: frozendict; Time: 1.81e-04; CV: 7e-01
init(seq2)  ; Size: 5000; Keys: int; Type:        Map; Time: 4.20e-04; CV: 7e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
init(o)     ; Size:    5; Keys: str; Type:       dict; Time: 9.47e-08; CV: 1e-01
init(o)     ; Size:    5; Keys: str; Type: frozendict; Time: 2.37e-08; CV: 1e-02
init(o)     ; Size:    5; Keys: str; Type:        Map; Time: 7.95e-08; CV: 2e-02
////////////////////////////////////////////////////////////////////////////////
init(o)     ; Size:    5; Keys: int; Type:       dict; Time: 9.29e-08; CV: 1e-01
init(o)     ; Size:    5; Keys: int; Type: frozendict; Time: 2.28e-08; CV: 4e-02
init(o)     ; Size:    5; Keys: int; Type:        Map; Time: 7.84e-08; CV: 5e-01
////////////////////////////////////////////////////////////////////////////////
init(o)     ; Size: 5000; Keys: str; Type:       dict; Time: 3.51e-05; CV: 6e-02
init(o)     ; Size: 5000; Keys: str; Type: frozendict; Time: 2.19e-08; CV: 3e-02
init(o)     ; Size: 5000; Keys: str; Type:        Map; Time: 7.92e-08; CV: 8e-02
////////////////////////////////////////////////////////////////////////////////
init(o)     ; Size: 5000; Keys: int; Type:       dict; Time: 1.69e-05; CV: 5e-02
init(o)     ; Size: 5000; Keys: int; Type: frozendict; Time: 2.37e-08; CV: 8e-02
init(o)     ; Size: 5000; Keys: int; Type:        Map; Time: 7.89e-08; CV: 2e-02
################################################################################
////////////////////////////////////////////////////////////////////////////////
init(holes) ; Size:    4; Keys: str; Type:       dict; Time: 1.97e-07; CV: 9e-02
init(holes) ; Size:    4; Keys: str; Type: frozendict; Time: 1.35e-07; CV: 2e-02
init(holes) ; Size:    4; Keys: str; Type:        Map; Time: 3.91e-07; CV: 3e-01
////////////////////////////////////////////////////////////////////////////////
init(holes) ; Size:    4; Keys: int; Type:       dict; Time: 1.91e-07; CV: 5e-01
init(holes) ; Size:    4; Keys: int; Type: frozendict; Time: 1.31e-07; CV: 9e-02
init(holes) ; Size:    4; Keys: int; Type:        Map; Time: 3.88e-07; CV: 6e-01
////////////////////////////////////////////////////////////////////////////////
init(holes) ; Size: 4999; Keys: str; Type:       dict; Time: 1.46e-04; CV: 3e-01
init(holes) ; Size: 4999; Keys: str; Type: frozendict; Time: 1.10e-04; CV: 2e-01
init(holes) ; Size: 4999; Keys: str; Type:        Map; Time: 7.82e-04; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
init(holes) ; Size: 4999; Keys: int; Type:       dict; Time: 1.06e-04; CV: 4e-02
init(holes) ; Size: 4999; Keys: int; Type: frozendict; Time: 8.11e-05; CV: 5e-02
init(holes) ; Size: 4999; Keys: int; Type:        Map; Time: 5.06e-04; CV: 3e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
copy        ; Size:    5; Keys: str; Type:       dict; Time: 6.66e-08; CV: 6e-01
copy        ; Size:    5; Keys: str; Type: frozendict; Time: 2.09e-08; CV: 2e-02
copy        ; Size:    5; Keys: str; Type:        Map; Time: 2.03e-06; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
copy        ; Size:    5; Keys: int; Type:       dict; Time: 6.63e-08; CV: 8e-01
copy        ; Size:    5; Keys: int; Type: frozendict; Time: 2.50e-08; CV: 1e-02
copy        ; Size:    5; Keys: int; Type:        Map; Time: 2.01e-06; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
copy        ; Size: 5000; Keys: str; Type:       dict; Time: 3.40e-05; CV: 4e-02
copy        ; Size: 5000; Keys: str; Type: frozendict; Time: 1.92e-08; CV: 4e-02
copy        ; Size: 5000; Keys: str; Type:        Map; Time: 1.01e-03; CV: 4e-02
////////////////////////////////////////////////////////////////////////////////
copy        ; Size: 5000; Keys: int; Type:       dict; Time: 1.50e-05; CV: 8e-02
copy        ; Size: 5000; Keys: int; Type: frozendict; Time: 1.88e-08; CV: 3e+00
copy        ; Size: 5000; Keys: int; Type:        Map; Time: 7.43e-04; CV: 2e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
iter keys   ; Size:    5; Keys: str; Type:       dict; Time: 7.95e-08; CV: 5e-02
iter keys   ; Size:    5; Keys: str; Type: frozendict; Time: 7.12e-08; CV: 9e-01
iter keys   ; Size:    5; Keys: str; Type:        Map; Time: 1.27e-07; CV: 7e-02
////////////////////////////////////////////////////////////////////////////////
iter keys   ; Size:    5; Keys: int; Type:       dict; Time: 7.07e-08; CV: 5e-01
iter keys   ; Size:    5; Keys: int; Type: frozendict; Time: 7.89e-08; CV: 3e-02
iter keys   ; Size:    5; Keys: int; Type:        Map; Time: 1.17e-07; CV: 5e-02
////////////////////////////////////////////////////////////////////////////////
iter keys   ; Size: 5000; Keys: str; Type:       dict; Time: 5.97e-05; CV: 6e-02
iter keys   ; Size: 5000; Keys: str; Type: frozendict; Time: 4.07e-05; CV: 8e-01
iter keys   ; Size: 5000; Keys: str; Type:        Map; Time: 8.36e-05; CV: 1e+00
////////////////////////////////////////////////////////////////////////////////
iter keys   ; Size: 5000; Keys: int; Type:       dict; Time: 4.63e-05; CV: 1e+01
iter keys   ; Size: 5000; Keys: int; Type: frozendict; Time: 4.60e-05; CV: 2e+00
iter keys   ; Size: 5000; Keys: int; Type:        Map; Time: 6.37e-05; CV: 1e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
iter values ; Size:    5; Keys: str; Type:       dict; Time: 7.67e-08; CV: 4e-02
iter values ; Size:    5; Keys: str; Type: frozendict; Time: 8.20e-08; CV: 3e-02
iter values ; Size:    5; Keys: str; Type:        Map; Time: 1.27e-07; CV: 3e-02
////////////////////////////////////////////////////////////////////////////////
iter values ; Size:    5; Keys: int; Type:       dict; Time: 8.19e-08; CV: 4e+00
iter values ; Size:    5; Keys: int; Type: frozendict; Time: 7.36e-08; CV: 5e-02
iter values ; Size:    5; Keys: int; Type:        Map; Time: 1.22e-07; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
iter values ; Size: 5000; Keys: str; Type:       dict; Time: 5.29e-05; CV: 1e-01
iter values ; Size: 5000; Keys: str; Type: frozendict; Time: 4.49e-05; CV: 2e-01
iter values ; Size: 5000; Keys: str; Type:        Map; Time: 9.01e-05; CV: 1e+00
////////////////////////////////////////////////////////////////////////////////
iter values ; Size: 5000; Keys: int; Type:       dict; Time: 4.62e-05; CV: 6e-02
iter values ; Size: 5000; Keys: int; Type: frozendict; Time: 4.17e-05; CV: 2e+00
iter values ; Size: 5000; Keys: int; Type:        Map; Time: 7.02e-05; CV: 1e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
iter items  ; Size:    5; Keys: str; Type:       dict; Time: 1.37e-07; CV: 1e+00
iter items  ; Size:    5; Keys: str; Type: frozendict; Time: 1.45e-07; CV: 1e+00
iter items  ; Size:    5; Keys: str; Type:        Map; Time: 2.30e-07; CV: 8e-02
////////////////////////////////////////////////////////////////////////////////
iter items  ; Size:    5; Keys: int; Type:       dict; Time: 1.52e-07; CV: 3e-02
iter items  ; Size:    5; Keys: int; Type: frozendict; Time: 1.46e-07; CV: 5e-02
iter items  ; Size:    5; Keys: int; Type:        Map; Time: 2.20e-07; CV: 9e-02
////////////////////////////////////////////////////////////////////////////////
iter items  ; Size: 5000; Keys: str; Type:       dict; Time: 1.13e-04; CV: 4e+00
iter items  ; Size: 5000; Keys: str; Type: frozendict; Time: 1.07e-04; CV: 5e+00
iter items  ; Size: 5000; Keys: str; Type:        Map; Time: 1.87e-04; CV: 5e-01
////////////////////////////////////////////////////////////////////////////////
iter items  ; Size: 5000; Keys: int; Type:       dict; Time: 1.11e-04; CV: 2e-02
iter items  ; Size: 5000; Keys: int; Type: frozendict; Time: 9.76e-05; CV: 2e-02
iter items  ; Size: 5000; Keys: int; Type:        Map; Time: 1.66e-04; CV: 9e-02
################################################################################
////////////////////////////////////////////////////////////////////////////////
pickle.dumps; Size:    5; Keys: str; Type:       dict; Time: 7.35e-07; CV: 2e-01
pickle.dumps; Size:    5; Keys: str; Type: frozendict; Time: 2.22e-06; CV: 6e-02
pickle.dumps; Size:    5; Keys: str; Type:        Map; Time: 2.85e-06; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
pickle.dumps; Size:    5; Keys: int; Type:       dict; Time: 5.16e-07; CV: 2e-01
pickle.dumps; Size:    5; Keys: int; Type: frozendict; Time: 2.06e-06; CV: 3e-01
pickle.dumps; Size:    5; Keys: int; Type:        Map; Time: 2.70e-06; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
pickle.dumps; Size: 5000; Keys: str; Type:       dict; Time: 6.37e-04; CV: 9e-02
pickle.dumps; Size: 5000; Keys: str; Type: frozendict; Time: 6.69e-04; CV: 3e-01
pickle.dumps; Size: 5000; Keys: str; Type:        Map; Time: 1.00e-03; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
pickle.dumps; Size: 5000; Keys: int; Type:       dict; Time: 1.58e-04; CV: 2e-02
pickle.dumps; Size: 5000; Keys: int; Type: frozendict; Time: 1.75e-04; CV: 7e-02
pickle.dumps; Size: 5000; Keys: int; Type:        Map; Time: 3.39e-04; CV: 2e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
pickle.loads; Size:    5; Keys: str; Type:       dict; Time: 9.56e-07; CV: 2e-01
pickle.loads; Size:    5; Keys: str; Type: frozendict; Time: 2.12e-06; CV: 1e-01
pickle.loads; Size:    5; Keys: str; Type:        Map; Time: 2.73e-06; CV: 9e-01
////////////////////////////////////////////////////////////////////////////////
pickle.loads; Size:    5; Keys: int; Type:       dict; Time: 5.04e-07; CV: 6e-01
pickle.loads; Size:    5; Keys: int; Type: frozendict; Time: 1.66e-06; CV: 8e-01
pickle.loads; Size:    5; Keys: int; Type:        Map; Time: 2.26e-06; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
pickle.loads; Size: 5000; Keys: str; Type:       dict; Time: 7.89e-04; CV: 1e-01
pickle.loads; Size: 5000; Keys: str; Type: frozendict; Time: 8.30e-04; CV: 1e-01
pickle.loads; Size: 5000; Keys: str; Type:        Map; Time: 1.56e-03; CV: 1e-01
////////////////////////////////////////////////////////////////////////////////
pickle.loads; Size: 5000; Keys: int; Type:       dict; Time: 3.22e-04; CV: 4e-02
pickle.loads; Size: 5000; Keys: int; Type: frozendict; Time: 3.66e-04; CV: 2e-01
pickle.loads; Size: 5000; Keys: int; Type:        Map; Time: 9.39e-04; CV: 6e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
fromkeys    ; Size:    5; Keys: str; Type:       dict; Time: 2.35e-07; CV: 4e-02
fromkeys    ; Size:    5; Keys: str; Type: frozendict; Time: 2.53e-07; CV: 4e-02
////////////////////////////////////////////////////////////////////////////////
fromkeys    ; Size:    5; Keys: int; Type:       dict; Time: 2.29e-07; CV: 1e+00
fromkeys    ; Size:    5; Keys: int; Type: frozendict; Time: 2.64e-07; CV: 1e-02
////////////////////////////////////////////////////////////////////////////////
fromkeys    ; Size: 5000; Keys: str; Type:       dict; Time: 2.10e-04; CV: 1e-01
fromkeys    ; Size: 5000; Keys: str; Type: frozendict; Time: 2.17e-04; CV: 2e-01
////////////////////////////////////////////////////////////////////////////////
fromkeys    ; Size: 5000; Keys: int; Type:       dict; Time: 1.50e-04; CV: 1e+00
fromkeys    ; Size: 5000; Keys: int; Type: frozendict; Time: 1.76e-04; CV: 3e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
set         ; Size:    5; Keys: str; Type:       dict; Time: 8.75e-08; CV: 2e+00
set         ; Size:    5; Keys: str; Type: frozendict; Time: 9.38e-08; CV: 4e-01
set         ; Size:    5; Keys: str; Type:        Map; Time: 1.46e-07; CV: 3e-01
////////////////////////////////////////////////////////////////////////////////
set         ; Size:    5; Keys: int; Type:       dict; Time: 8.98e-08; CV: 3e-01
set         ; Size:    5; Keys: int; Type: frozendict; Time: 1.03e-07; CV: 1e-01
set         ; Size:    5; Keys: int; Type:        Map; Time: 1.51e-07; CV: 3e-01
////////////////////////////////////////////////////////////////////////////////
set         ; Size: 5000; Keys: str; Type:       dict; Time: 3.44e-05; CV: 2e-01
set         ; Size: 5000; Keys: str; Type: frozendict; Time: 3.41e-05; CV: 1e-01
set         ; Size: 5000; Keys: str; Type:        Map; Time: 3.37e-07; CV: 3e+00
////////////////////////////////////////////////////////////////////////////////
set         ; Size: 5000; Keys: int; Type:       dict; Time: 1.51e-05; CV: 1e-01
set         ; Size: 5000; Keys: int; Type: frozendict; Time: 1.43e-05; CV: 4e+00
set         ; Size: 5000; Keys: int; Type:        Map; Time: 3.29e-07; CV: 8e-01
################################################################################
////////////////////////////////////////////////////////////////////////////////
delete      ; Size:    5; Keys: str; Type:       dict; Time: 8.78e-08; CV: 5e-01
delete      ; Size:    5; Keys: str; Type: frozendict; Time: 9.52e-08; CV: 3e-01
delete      ; Size:    5; Keys: str; Type:        Map; Time: 1.01e-07; CV: 2e+00
////////////////////////////////////////////////////////////////////////////////
delete      ; Size:    5; Keys: int; Type:       dict; Time: 9.00e-08; CV: 1e-01
delete      ; Size:    5; Keys: int; Type: frozendict; Time: 1.06e-07; CV: 8e-02
delete      ; Size:    5; Keys: int; Type:        Map; Time: 1.05e-07; CV: 6e-02
////////////////////////////////////////////////////////////////////////////////
delete      ; Size: 5000; Keys: str; Type:       dict; Time: 3.42e-05; CV: 2e-02
delete      ; Size: 5000; Keys: str; Type: frozendict; Time: 3.67e-05; CV: 2e+00
delete      ; Size: 5000; Keys: str; Type:        Map; Time: 2.96e-07; CV: 3e+00
////////////////////////////////////////////////////////////////////////////////
delete      ; Size: 5000; Keys: int; Type:       dict; Time: 1.51e-05; CV: 2e-01
delete      ; Size: 5000; Keys: int; Type: frozendict; Time: 2.20e-05; CV: 5e+00
delete      ; Size: 5000; Keys: int; Type:        Map; Time: 2.98e-07; CV: 1e+00
################################################################################
```

[1] Benchmarks done using the C Extension with:

* Linux x86_64
* CPU with 4 cores and 8 threads
* Python 3.10.21 compiled with GCC 12, without PGO and LTO. An optimized build of Python would be unfair, since the C Extension has no PGO and no LTO.
* Commands run before the benchmark:

```
sudo pyperf system tune
sudo cpupower frequency-set -d 3001MHz -u 3001MHz
sudo tuna --cpus=2,3 --isolate
```

* Benchmark command:

```
PYTHONHASHSEED=0 taskset -c 2 python -u test/bench.py --seed 0
```

CV is the robust coefficient of variation: MAD / median.
