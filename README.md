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
```

You can also subtract an iterable from a `frozendict`. A new `frozendict`
will be returned, without the keys that are in the iterable. Examples:

```python
frozendict({"Sulla": "Marco", 2: 3}) - {"Sulla": "Marò", 4: 7}
# frozendict({2: 3})
frozendict({"Sulla": "Marco", 2: 3}) - [2, 4]
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

frozendict(fd)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})

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

iter(fd)
# <dict_keyiterator object at 0x7feb75c49188>

frozendict.fromkeys(["Marco", "Giulia"], "Sulla")
# frozendict({'Marco': 'Sulla', 'Giulia': 'Sulla'})

fd["Sulla"] = "Silla"
# NotImplementedError: 'frozendict' object is immutable

del fd["Sulla"]
# NotImplementedError: 'frozendict' object is immutable

fd.clear()
# NotImplementedError: 'frozendict' object is immutable

fd.pop("Sulla")
# NotImplementedError: 'frozendict' object is immutable

fd.popitem()
# NotImplementedError: 'frozendict' object is immutable

fd.setdefault("Sulla")
# NotImplementedError: 'frozendict' object is immutable

fd.update({"God": "exists"})
# NotImplementedError: 'frozendict' object is immutable

fd.__init__({"Trump": "Donald"})
# NotImplementedError: 'frozendict' object is immutable

vars(fd)
# {}

fd._initialized
# True

fd._initialized = False
# NotImplementedError: 'frozendict' object is immutable

del fd._initialized
# NotImplementedError: 'frozendict' object is immutable
```

# Benchmarks

Some benchmarks between `dict`, `immutables.Map` and `frozendict`:

```
Dictionary size:    5; Type:       dict; Statement: `d.get(key)`;             time: 0.831; iterations: 13000000
Dictionary size:    5; Type:        Map; Statement: `d.get(key)`;             time: 0.855; iterations: 13000000
Dictionary size:    5; Type: frozendict; Statement: `d.get(key)`;             time: 0.836; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d[key]`;                 time: 0.289; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d[key]`;                 time: 0.395; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d[key]`;                 time: 0.811; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key in d`;               time: 0.576; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key in d`;               time: 0.527; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key in d`;               time: 1.023; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key not in d`;           time: 0.468; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key not in d`;           time: 0.517; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key not in d`;           time: 0.911; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.600; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `pickle.dumps(d)`;        time: 2.069; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 1.941; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.742; iterations:   800000
Dictionary size:    5; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.436; iterations:   800000
Dictionary size:    5; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 5.165; iterations:   800000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:        Map; Statement: `hash(d)`;                time: 0.537; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `hash(d)`;                time: 1.721; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `len(d)`;                 time: 0.653; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `len(d)`;                 time: 0.676; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `len(d)`;                 time: 0.660; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.keys()`;               time: 2.310; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.keys()`;               time: 3.114; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.keys()`;               time: 2.342; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.values()`;             time: 2.319; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.values()`;             time: 3.165; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.values()`;             time: 2.357; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.items()`;              time: 1.736; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d.items()`;              time: 2.281; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d.items()`;              time: 1.723; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `iter(d)`;                time: 2.440; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `iter(d)`;                time: 3.079; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `iter(d)`;                time: 2.404; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(dict)`;      time: 0.354; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(dict)`;      time: 0.967; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(dict)`;      time: 9.323; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(d.items())`; time: 0.717; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(d.items())`; time: 0.895; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(d.items())`; time: 9.714; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(**d)`;       time: 0.157; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `constructor(**d)`;       time: 0.463; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(**d)`;       time: 4.658; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(self)`;      time: 1.778; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `constructor(self)`;      time: 0.666; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(self)`;      time: 41.716; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d1 == d2`;               time: 1.265; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d1 == d2`;               time: 0.630; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d1 == d2`;               time: 1.271; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `self == self`;           time: 1.200; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `self == self`;           time: 0.528; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `self == self`;           time: 1.224; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `repr(d)`;                time: 0.806; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `repr(d)`;                time: 1.121; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `repr(d)`;                time: 0.125; iterations:   600000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `str(d)`;                 time: 0.835; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `str(d)`;                 time: 1.105; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `str(d)`;                 time: 0.143; iterations:   600000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;             time: 0.917; iterations: 13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;             time: 0.925; iterations: 13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;             time: 0.824; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                 time: 0.294; iterations: 10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                 time: 0.467; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                 time: 0.830; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;               time: 0.510; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;               time: 0.560; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;               time: 0.916; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;           time: 0.507; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;           time: 0.619; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;           time: 1.067; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.609; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;        time: 0.966; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 0.753; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.565; iterations:     4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.313; iterations:     4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 1.037; iterations:     4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                time: 0.473; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                time: 1.832; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                 time: 0.893; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                 time: 0.906; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                 time: 0.897; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;               time: 0.819; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;               time: 1.872; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;               time: 0.810; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;             time: 0.798; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;             time: 1.885; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;             time: 0.824; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;              time: 0.775; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;              time: 1.721; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;              time: 0.755; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                time: 0.812; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                time: 1.871; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                time: 0.829; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;      time: 0.209; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;      time: 1.744; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;      time: 0.708; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(d.items())`; time: 0.387; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(d.items())`; time: 1.683; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(d.items())`; time: 0.953; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;       time: 0.098; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;       time: 0.857; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;       time: 0.644; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;      time: 0.963; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;      time: 0.003; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;      time: 1.216; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;               time: 0.904; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;               time: 0.003; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;               time: 0.927; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;           time: 0.899; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;           time: 0.003; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;           time: 0.926; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                time: 0.549; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                time: 1.013; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                time: 0.001; iterations:     3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                 time: 0.563; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                 time: 1.003; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                 time: 0.001; iterations:     3000
```

`d[key]` and `key in d` is strangely slower, probably because there's the 
overhead of the superclass (`frozendict` inherits `dict`).

The other methods are comparable with `dict` and `immutables.Map`, and 
sometimes faster than `immutables.Map`. Constructors are much slower, but I 
suppose this is because `frozendict` overrides `__setattr__`, checking if 
the object is not already created and so creating an overhead. This become
less problematic with the growing of number of items.

Where `immutables.Map` is really fast is in creating a copy of itself, and 
checking equality with other `immutables.Map`s. This is because it's written 
in C. It has not to invoke the `dict` constructor but can simply copy and 
check its attributes. It seems fast also at checking equality with `dict`, but 
only because it does not work...

I think a really good solution is to create a `C` `basedict` and 
`frozendict`, and let `dict` and `frozendict` inherits from `basedict`, a sort
of `C` version of `collections.abc.Mapping`. IMHO this solution is much better 
than the proposal in [PEP 603](https://www.python.org/dev/peps/pep-0603/).
