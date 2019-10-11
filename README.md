# frozendict

`frozendict` is an immutable dictionary. Unlike other similar implementation, 
immutability is guaranteed: you can't change the internal variables of the 
class, and they are all immutable objects. `__init__` can be called only at 
object creation.

The API is the same as `dict`, so it supports also `fromkeys`, unlike other 
implementations. Furthermore it supports `copy.deepcopy()` and can be 
`pickle`d and un`pickle`d.

In addition, a `frozendict` supports the `+` and `-` operand. If you add a 
`dict`-like object, a new `frozendict` will be returned, equal to the old 
`frozendict` updated with the other object. Example:

```python
frozendict({"Sulla": "Marco", 2: 3}) + {"Sulla": "Marò", 4: 7}
# frozendict({'Sulla': 'Marò', 2: 3, 4: 7})
```

You can also subtract an iterable from a `frozendict`. A new `frozendict`
will be returned, without the keys that are in the iterable. Examples:

```python
frozendict({"Sulla": "Marco", 2: 3}) - {"Sulla": "Marò", 4: 7}
# frozendict({2: 3})
frozendict({"Sulla": "Marco", 2: 3}) - [2]
# frozendict({'Sulla': 'Marco'})
```

`frozendict` supports `hash()`, but does not guarantee the immutability of its values; so
`hash()` will work only if all its values are immutable.


Some other examples:

```python
from frozendict import frozendict

fd = frozendict({"Sulla": "Marco", "Hicks": "Bill"})

print(fd)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})

print(fd["Sulla"])
# Marco

len(fd)
# 2

"Sulla" in fd
# True

"God" in fd
# False

fd2 = fd.copy()
fd2 == fd
# True
fd2 is fd
# False

fd_with_mutables = frozendict(Marco=["Francesco", "Sulla"])
fd_with_mutables2 = fd_with_mutables.copy()
fd_with_mutables2["Marco"] is fd_with_mutables["Marco"]
# True
import copy
fd_with_mutables3 = copy.deepcopy(fd_with_mutables)
print(fd_with_mutables3)
# frozendict({'Marco': ['Francesco, Sulla']})
fd_with_mutables3["Marco"] is fd_with_mutables["Marco"]
# False

hash(fd)
# 5596995276032009052

hash(fd_with_mutables)
# TypeError: unhashable frozendict

import pickle
fd_unpickled = pickle.loads(pickle.dumps(fd))
print(fd_unpickled)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})
fd_unpickled == fd
# True

fd.get("Sulla")
# 'Marco'

print(fd.get("God"))
# None

tuple(fd.keys())
# ('Sulla', 2)

tuple(fd.values())
# ('Marco', 3)

tuple(fd.items())
# (('Sulla', 'Marco'), (2, 3))

frozendict.fromkeys(["Marco", "Giulia"], "Sulla")
# frozendict({'Marco': 'Sulla', 'Giulia': 'Sulla'})

fd["Sulla"] = "Silla"
# TypeError: 'frozendict' object does not support item assignment

del fd["Sulla"]
# TypeError: 'frozendict' object does not support item deletion

fd.clear()
# AttributeError: 'frozendict' object has no attribute 'clear'

fd.pop("Sulla")
# AttributeError: 'frozendict' object has no attribute 'pop'

fd.popitem()
# AttributeError: 'frozendict' object has no attribute 'popitem'

fd.setdefault("Sulla")
# AttributeError: 'frozendict' object has no attribute 'setdefault'

fd.update({"God": "exists"})
# AttributeError: 'frozendict' object has no attribute 'update'

fd.__init__({"Trump": "Donald"})
# NotImplementedError: you can't reinitialize the object

vars(fd)
# {'_dict': mappingproxy({'Sulla': 'Marco', 'Hicks': 'Bill'}), '_repr': "frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})", '_hash': 1288371660109276517, '_frozendict__inizialized': True}

fd._dict = {"Hitler": "Adolf"}
# NotImplementedError: 'frozendict' object does not support attribute setting

del fd._dict
# NotImplementedError: 'frozendict' object does not support attribute deletion

print(fd._dict["Sulla"])
# Marco

fd._dict["Sulla"] = "Isabella"
# TypeError: 'mappingproxy' object does not support item assignment

frozendict(Sulla="Marco", Hicks="Bill")
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'}

frozendict((("Sulla", "Marco"), ("Hicks", "Bill")))
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})

"Sulla" not in fd
# False

iter(fd)
# <dict_keyiterator object at 0x7feb75c49188>

fd["God"]
# KeyError: 'God'
```
