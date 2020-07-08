# frozendict

Welcome, fellow programmer!

`frozendict` is a simple immutable dictionary. Unlike other similar implementation, 
immutability is guaranteed: you can't change the internal variables of the 
class, and they are all immutable objects. `__init__` can be called only at 
object creation.

The API is the same as `dict`, without methods that can change the immutability. 
So it supports also `fromkeys`, unlike other implementations. Furthermore it 
can be `pickle`d and un`pickle`d, and can have an hash if all it's value are 
hashable.

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
fd2 is fd
# True

fd3 = frozendict(fd)
fd3 is fd
# True

fd4 = frozendict({"Hicks": "Bill", "Sulla": "Marco"})

print(fd4)
# frozendict({'Hicks': 'Bill', 'Sulla': 'Marco'})

fd4 is fd
# False

fd4 == fd
# True

import pickle
fd_unpickled = pickle.loads(pickle.dumps(fd))
print(fd_unpickled)
# frozendict({'Sulla': 'Marco', 'Hicks': 'Bill'})
fd_unpickled == fd
# True

frozendict()
# frozendict({})

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
# NotImplementedError: `frozendict` object is immutable.

del fd["Sulla"]
# NotImplementedError: `frozendict` object is immutable.

fd.clear()
# NotImplementedError: `frozendict` object is immutable.

fd.pop("Sulla")
# NotImplementedError: `frozendict` object is immutable.

fd.popitem()
# NotImplementedError: `frozendict` object is immutable.

fd.setdefault("Sulla")
# NotImplementedError: `frozendict` object is immutable.

fd.update({"God": "exists"})
# NotImplementedError: `frozendict` object is immutable.

fd.__init__({"Trump": "Donald"})
# NotImplementedError: `frozendict` object is immutable.

vars(fd)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: vars() argument must have __dict__ attribute
```

# Benchmarks

Some benchmarks between `dict`, `immutables.Map` and `frozendict`:

```
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.get(key)`;             time: 0.392; iterations: 13000000
Dictionary size:    8; Type:        Map; Statement: `d.get(key)`;             time: 0.702; iterations: 13000000
Dictionary size:    8; Type: frozendict; Statement: `d.get(key)`;             time: 0.409; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d[key]`;                 time: 0.426; iterations: 10000000
Dictionary size:    8; Type:        Map; Statement: `d[key]`;                 time: 0.523; iterations: 10000000
Dictionary size:    8; Type: frozendict; Statement: `d[key]`;                 time: 0.599; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `key in d`;               time: 0.756; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `key in d`;               time: 0.681; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `key in d`;               time: 1.072; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `key not in d`;           time: 0.761; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `key not in d`;           time: 0.654; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `key not in d`;           time: 1.205; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.603; iterations:   625000
Dictionary size:    8; Type:        Map; Statement: `pickle.dumps(d)`;        time: 2.022; iterations:   625000
Dictionary size:    8; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 1.947; iterations:   625000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.762; iterations:   500000
Dictionary size:    8; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.722; iterations:   500000
Dictionary size:    8; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 2.714; iterations:   500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:        Map; Statement: `hash(d)`;                time: 0.651; iterations: 10000000
Dictionary size:    8; Type: frozendict; Statement: `hash(d)`;                time: 4.029; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `len(d)`;                 time: 1.215; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `len(d)`;                 time: 1.217; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `len(d)`;                 time: 1.208; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.keys()`;               time: 1.634; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d.keys()`;               time: 2.126; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d.keys()`;               time: 1.633; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.values()`;             time: 1.509; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d.values()`;             time: 2.126; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d.values()`;             time: 1.548; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.items()`;              time: 1.552; iterations:  6250000
Dictionary size:    8; Type:        Map; Statement: `d.items()`;              time: 1.919; iterations:  6250000
Dictionary size:    8; Type: frozendict; Statement: `d.items()`;              time: 1.494; iterations:  6250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `iter(d)`;                time: 1.872; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `iter(d)`;                time: 2.268; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `iter(d)`;                time: 1.864; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(dict)`;      time: 0.382; iterations:  1250000
Dictionary size:    8; Type:        Map; Statement: `constructor(dict)`;      time: 0.867; iterations:  1250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(dict)`;      time: 2.850; iterations:  1250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(d.items())`; time: 0.501; iterations:  1250000
Dictionary size:    8; Type:        Map; Statement: `constructor(d.items())`; time: 0.776; iterations:  1250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(d.items())`; time: 2.957; iterations:  1250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(**d)`;       time: 0.180; iterations:   625000
Dictionary size:    8; Type:        Map; Statement: `constructor(**d)`;       time: 0.422; iterations:   625000
Dictionary size:    8; Type: frozendict; Statement: `constructor(**d)`;       time: 1.864; iterations:   625000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(self)`;      time: 1.897; iterations:  6250000
Dictionary size:    8; Type:        Map; Statement: `constructor(self)`;      time: 0.549; iterations:  6250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(self)`;      time: 6.946; iterations:  6250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d1 == d2`;               time: 1.538; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d1 == d2`;               time: 0.615; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d1 == d2`;               time: 1.564; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `self == self`;           time: 1.531; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `self == self`;           time: 0.546; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `self == self`;           time: 1.533; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `repr(d)`;                time: 1.039; iterations:   375000
Dictionary size:    8; Type:        Map; Statement: `repr(d)`;                time: 1.480; iterations:   375000
Dictionary size:    8; Type: frozendict; Statement: `repr(d)`;                time: 1.193; iterations:   375000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `str(d)`;                 time: 1.065; iterations:   375000
Dictionary size:    8; Type:        Map; Statement: `str(d)`;                 time: 1.506; iterations:   375000
Dictionary size:    8; Type: frozendict; Statement: `str(d)`;                 time: 1.238; iterations:   375000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;             time: 0.413; iterations: 13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;             time: 0.783; iterations: 13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;             time: 0.415; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                 time: 0.399; iterations: 10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                 time: 0.592; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                 time: 0.578; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;               time: 0.715; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;               time: 0.758; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;               time: 1.071; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;           time: 0.686; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;           time: 0.783; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;           time: 1.125; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.690; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;        time: 1.072; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 0.845; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.630; iterations:     4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.431; iterations:     4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 0.761; iterations:     4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                time: 0.643; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                time: 4.079; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                 time: 1.396; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                 time: 1.385; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                 time: 1.376; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;               time: 0.907; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;               time: 1.865; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;               time: 0.916; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;             time: 0.897; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;             time: 1.899; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;             time: 0.897; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;              time: 0.917; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;              time: 1.867; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;              time: 0.915; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                time: 0.914; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                time: 1.899; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                time: 0.979; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;      time: 0.257; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;      time: 1.877; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;      time: 0.274; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(d.items())`; time: 0.433; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(d.items())`; time: 1.747; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(d.items())`; time: 0.465; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;       time: 0.123; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;       time: 0.936; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;       time: 0.724; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;      time: 1.222; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;      time: 0.004; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;      time: 0.056; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;               time: 1.317; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;               time: 0.005; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;               time: 1.328; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;           time: 1.313; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;           time: 0.004; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;           time: 1.346; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                time: 0.803; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                time: 1.260; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                time: 0.824; iterations:     3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                 time: 0.804; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                 time: 1.265; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                 time: 0.816; iterations:     3000
```

`d[key]` and `key in d` is strangely slower, and `pickle` too. It seems 
this is caused by the overhead of the superclass (`frozendict` inherits 
`dict`).

Also constructors are slower, maybe for the overhead of some preprocessing
that `__new__()` and `__init__()` do. Indeed with very large maps the 
performance is the same as `dict`.

The other methods are comparable with `dict` and `immutables.Map`, and 
sometimes faster than `immutables.Map`.

Where `immutables.Map` is really fast is in creating a copy of itself, and 
checking equality with other `immutables.Map`s. This is because it's written 
in C. It has not to invoke the `dict` constructor but can simply copy and 
check its attributes. It seems fast also at checking equality with `dict`, but 
only because the check does not work...
