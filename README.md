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

In addition, `frozendict` supports the `+` and `-` operands. If you add a 
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

fd.initialized
# True

fd.initialized = False
# NotImplementedError: `frozendict` object is immutable.

del fd.initialized
# NotImplementedError: `frozendict` object is immutable.
```

# Benchmarks

Some benchmarks between `dict`, `immutables.Map` and `frozendict`:

```
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.get(key)`;             time: 0.571; iterations: 13000000
Dictionary size:    8; Type:        Map; Statement: `d.get(key)`;             time: 0.974; iterations: 13000000
Dictionary size:    8; Type: frozendict; Statement: `d.get(key)`;             time: 0.559; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d[key]`;                 time: 0.608; iterations: 10000000
Dictionary size:    8; Type:        Map; Statement: `d[key]`;                 time: 0.794; iterations: 10000000
Dictionary size:    8; Type: frozendict; Statement: `d[key]`;                 time: 0.844; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `key in d`;               time: 0.937; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `key in d`;               time: 0.929; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `key in d`;               time: 1.563; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `key not in d`;           time: 1.001; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `key not in d`;           time: 0.912; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `key not in d`;           time: 1.547; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.859; iterations:   625000
Dictionary size:    8; Type:        Map; Statement: `pickle.dumps(d)`;        time: 2.841; iterations:   625000
Dictionary size:    8; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 2.718; iterations:   625000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `pickle.loads(dump)`;     time: 1.040; iterations:   500000
Dictionary size:    8; Type:        Map; Statement: `pickle.loads(dump)`;     time: 2.343; iterations:   500000
Dictionary size:    8; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 3.825; iterations:   500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:        Map; Statement: `hash(d)`;                time: 0.960; iterations: 10000000
Dictionary size:    8; Type: frozendict; Statement: `hash(d)`;                time: 4.816; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `len(d)`;                 time: 1.612; iterations: 20000000
Dictionary size:    8; Type:        Map; Statement: `len(d)`;                 time: 1.611; iterations: 20000000
Dictionary size:    8; Type: frozendict; Statement: `len(d)`;                 time: 1.544; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.keys()`;               time: 2.317; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d.keys()`;               time: 3.089; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d.keys()`;               time: 2.314; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.values()`;             time: 2.161; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d.values()`;             time: 3.042; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d.values()`;             time: 2.238; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d.items()`;              time: 2.120; iterations:  6250000
Dictionary size:    8; Type:        Map; Statement: `d.items()`;              time: 2.792; iterations:  6250000
Dictionary size:    8; Type: frozendict; Statement: `d.items()`;              time: 2.131; iterations:  6250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `iter(d)`;                time: 2.644; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `iter(d)`;                time: 3.273; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `iter(d)`;                time: 2.642; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(dict)`;      time: 0.511; iterations:  1250000
Dictionary size:    8; Type:        Map; Statement: `constructor(dict)`;      time: 1.336; iterations:  1250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(dict)`;      time: 4.406; iterations:  1250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(d.items())`; time: 0.646; iterations:  1250000
Dictionary size:    8; Type:        Map; Statement: `constructor(d.items())`; time: 1.204; iterations:  1250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(d.items())`; time: 4.599; iterations:  1250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(**d)`;       time: 0.252; iterations:   625000
Dictionary size:    8; Type:        Map; Statement: `constructor(**d)`;       time: 0.658; iterations:   625000
Dictionary size:    8; Type: frozendict; Statement: `constructor(**d)`;       time: 2.815; iterations:   625000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `constructor(self)`;      time: 2.594; iterations:  6250000
Dictionary size:    8; Type:        Map; Statement: `constructor(self)`;      time: 0.764; iterations:  6250000
Dictionary size:    8; Type: frozendict; Statement: `constructor(self)`;      time: 9.138; iterations:  6250000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `d1 == d2`;               time: 2.119; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `d1 == d2`;               time: 0.891; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `d1 == d2`;               time: 2.146; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `self == self`;           time: 2.099; iterations: 12500000
Dictionary size:    8; Type:        Map; Statement: `self == self`;           time: 0.708; iterations: 12500000
Dictionary size:    8; Type: frozendict; Statement: `self == self`;           time: 2.138; iterations: 12500000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `repr(d)`;                time: 1.481; iterations:   375000
Dictionary size:    8; Type:        Map; Statement: `repr(d)`;                time: 2.025; iterations:   375000
Dictionary size:    8; Type: frozendict; Statement: `repr(d)`;                time: 1.663; iterations:   375000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    8; Type:       dict; Statement: `str(d)`;                 time: 1.468; iterations:   375000
Dictionary size:    8; Type:        Map; Statement: `str(d)`;                 time: 2.019; iterations:   375000
Dictionary size:    8; Type: frozendict; Statement: `str(d)`;                 time: 1.690; iterations:   375000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;             time: 0.543; iterations: 13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;             time: 1.044; iterations: 13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;             time: 0.672; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                 time: 0.548; iterations: 10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                 time: 0.836; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                 time: 0.843; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;               time: 0.891; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;               time: 1.036; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;               time: 1.579; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;           time: 0.971; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;           time: 1.024; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;           time: 1.635; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.967; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;        time: 1.484; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 1.222; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.892; iterations:     4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;     time: 2.064; iterations:     4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 1.089; iterations:     4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                time: 0.945; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                time: 4.623; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                 time: 1.798; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                 time: 1.779; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                 time: 1.809; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;               time: 1.293; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;               time: 2.608; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;               time: 1.258; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;             time: 1.236; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;             time: 2.636; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;             time: 1.233; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;              time: 1.264; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;              time: 2.537; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;              time: 1.283; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                time: 1.265; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                time: 2.596; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                time: 1.268; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;      time: 0.344; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;      time: 2.528; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;      time: 0.393; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(d.items())`; time: 0.628; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(d.items())`; time: 2.423; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(d.items())`; time: 0.669; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;       time: 0.173; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;       time: 1.273; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;       time: 1.035; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;      time: 1.713; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;      time: 0.006; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;      time: 0.076; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;               time: 1.860; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;               time: 0.007; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;               time: 1.903; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;           time: 1.886; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;           time: 0.006; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;           time: 1.839; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                time: 1.086; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                time: 1.712; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                time: 1.096; iterations:     3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                 time: 1.092; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                 time: 1.714; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                 time: 1.083; iterations:     3000
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

I think a really good solution is to create a `C` `basedict` and 
`frozendict`, and let `dict` and `frozendict` inherits from `basedict`, a sort
of `C` version of `collections.abc.Mapping`. IMHO this solution is much better 
than the proposal in [PEP 603](https://www.python.org/dev/peps/pep-0603/).
