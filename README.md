# frozendict

`frozendict` is a simple immutable dictionary. Unlike other similar implementation, 
immutability is guaranteed: you can't change the internal variables of the 
class, and they are all immutable objects. `__init__` can be called only at 
object creation.

The API is the same as `dict`, without methods that can change the immutability. 
So it supports also `fromkeys`, unlike other implementations. Furthermore it 
can be `pickle`d and un`pickle`d.

In addition, a `frozendict` supports the `+` and `-` operands. If you add a 
`dict`-like object, a new `frozendict` will be returned, equal to the old 
`frozendict` updated with the other object. Example:

```python
frozendict({"Sulla": "Marco", 2: 3}) + {"Sulla": "Marò", 4: 7}
# frozendict({'Sulla': 'Marò', 2: 3, 4: 7})
frozendict({"Sulla": "Marco", 2: 3}) + (("Sulla", "Marco"), ("Hicks", "Bill"))
# frozendict({'Sulla': 'Marco', 2: 3, 'Hicks': 'Bill'})
```

You can also subtract an iterable from a `frozendict`. A new `frozendict`
will be returned, without the keys that are in the iterable. Examples:

```python
frozendict({"Sulla": "Marco", 2: 3}) - {"Sulla": "Marò", 4: 7}
# frozendict({2: 3})
frozendict({"Sulla": "Marco", 2: 3}) - [2]
# frozendict({'Sulla': 'Marco'})
```

Unlike other implementations, all values of a `frozendict` must be immutable, 
i.e. support `hash()`, like `frozenset`.


Some other examples:

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

fd2 = fd.copy()
fd2 == fd
# True
fd2 is fd
# False

hash(fd)
# 5833699487320513741

import pickle
fd_unpickled = pickle.loads(pickle.dumps(fd))
print(fd_unpickled)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})
fd_unpickled == fd
# True

frozendict()
# frozendict({})

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

iter(fd)
# <dict_keyiterator object at 0x7feb75c49188>

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
# {}

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
```
