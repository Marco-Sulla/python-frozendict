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

frozendict(fd)
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
Dictionary size:    5; Type:       dict; Statement: `d.get(key)`;             time: 0.576; iterations: 13000000
Dictionary size:    5; Type:        Map; Statement: `d.get(key)`;             time: 0.934; iterations: 13000000
Dictionary size:    5; Type: frozendict; Statement: `d.get(key)`;             time: 0.522; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d[key]`;                 time: 0.605; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d[key]`;                 time: 0.703; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d[key]`;                 time: 0.846; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key in d`;               time: 1.065; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key in d`;               time: 0.914; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key in d`;               time: 1.418; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key not in d`;           time: 0.983; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key not in d`;           time: 0.873; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key not in d`;           time: 1.515; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.976; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `pickle.dumps(d)`;        time: 3.668; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 3.600; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.loads(dump)`;     time: 1.121; iterations:   800000
Dictionary size:    5; Type:        Map; Statement: `pickle.loads(dump)`;     time: 2.682; iterations:   800000
Dictionary size:    5; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 6.426; iterations:   800000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:        Map; Statement: `hash(d)`;                time: 0.855; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `hash(d)`;                time: 2.890; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `len(d)`;                 time: 1.402; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `len(d)`;                 time: 1.407; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `len(d)`;                 time: 1.392; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.keys()`;               time: 2.777; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.keys()`;               time: 3.742; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.keys()`;               time: 2.783; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.values()`;             time: 2.559; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.values()`;             time: 3.740; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.values()`;             time: 2.641; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.items()`;              time: 2.160; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d.items()`;              time: 3.186; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d.items()`;              time: 2.179; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `iter(d)`;                time: 3.490; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `iter(d)`;                time: 4.164; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `iter(d)`;                time: 3.553; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(dict)`;      time: 0.550; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(dict)`;      time: 1.214; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(dict)`;      time: 8.532; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(d.items())`; time: 0.764; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(d.items())`; time: 1.073; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(d.items())`; time: 8.767; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(**d)`;       time: 0.253; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `constructor(**d)`;       time: 0.584; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(**d)`;       time: 4.341; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(self)`;      time: 2.720; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `constructor(self)`;      time: 1.130; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(self)`;      time: 13.751; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d1 == d2`;               time: 2.590; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d1 == d2`;               time: 1.363; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d1 == d2`;               time: 2.658; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `self == self`;           time: 2.539; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `self == self`;           time: 1.117; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `self == self`;           time: 2.535; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `repr(d)`;                time: 1.441; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `repr(d)`;                time: 1.996; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `repr(d)`;                time: 1.783; iterations:   600000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `str(d)`;                 time: 1.490; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `str(d)`;                 time: 2.035; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `str(d)`;                 time: 1.809; iterations:   600000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;             time: 0.529; iterations: 13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;             time: 1.052; iterations: 13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;             time: 0.556; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                 time: 0.527; iterations: 10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                 time: 0.784; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                 time: 0.776; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;               time: 0.873; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;               time: 1.092; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;               time: 1.504; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;           time: 0.890; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;           time: 0.974; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;           time: 1.429; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.926; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;        time: 1.425; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 1.121; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.852; iterations:     4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.995; iterations:     4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 1.024; iterations:     4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                time: 0.855; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                time: 2.915; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                 time: 1.654; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                 time: 1.633; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                 time: 1.644; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;               time: 1.223; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;               time: 2.520; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;               time: 1.215; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;             time: 1.209; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;             time: 2.496; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;             time: 1.204; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;              time: 1.242; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;              time: 2.439; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;              time: 1.242; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                time: 1.228; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                time: 2.518; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                time: 1.220; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;      time: 0.323; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;      time: 2.511; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;      time: 0.376; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(d.items())`; time: 0.603; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(d.items())`; time: 2.422; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(d.items())`; time: 0.665; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;       time: 0.162; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;       time: 1.258; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;       time: 0.970; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;      time: 1.604; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;      time: 0.006; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;      time: 0.072; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;               time: 1.760; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;               time: 0.007; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;               time: 1.786; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;           time: 1.755; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;           time: 0.006; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;           time: 1.755; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                time: 1.058; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                time: 1.794; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                time: 1.068; iterations:     3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                 time: 1.052; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                 time: 1.793; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                 time: 1.066; iterations:     3000
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
