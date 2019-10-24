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
# TypeError: not all values are hashable

fd2 = fd.copy()
fd2 == fd
# True
fd2 is fd
# False

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
Dictionary size:    5; Type:       dict; Statement: `d.get(key)`;             time: 0.797; iterations: 13000000
Dictionary size:    5; Type:        Map; Statement: `d.get(key)`;             time: 0.864; iterations: 13000000
Dictionary size:    5; Type: frozendict; Statement: `d.get(key)`;             time: 0.827; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d[key]`;                 time: 0.315; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d[key]`;                 time: 0.393; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d[key]`;                 time: 0.891; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key in d`;               time: 0.501; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key in d`;               time: 0.519; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key in d`;               time: 0.920; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key not in d`;           time: 0.501; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `key not in d`;           time: 0.515; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `key not in d`;           time: 0.958; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.588; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `pickle.dumps(d)`;        time: 2.089; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 2.059; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.751; iterations:   800000
Dictionary size:    5; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.414; iterations:   800000
Dictionary size:    5; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 4.261; iterations:   800000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:        Map; Statement: `hash(d)`;                time: 0.445; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `hash(d)`;                time: 1.854; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `len(d)`;                 time: 0.711; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `len(d)`;                 time: 0.708; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `len(d)`;                 time: 0.702; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.keys()`;               time: 2.493; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.keys()`;               time: 3.137; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.keys()`;               time: 2.482; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.values()`;             time: 2.385; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d.values()`;             time: 3.140; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d.values()`;             time: 2.423; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.items()`;              time: 1.846; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `d.items()`;              time: 2.468; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `d.items()`;              time: 1.845; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `iter(d)`;                time: 2.357; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `iter(d)`;                time: 2.879; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `iter(d)`;                time: 2.360; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(dict)`;      time: 0.365; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(dict)`;      time: 0.787; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(dict)`;      time: 6.637; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(d.items())`; time: 0.717; iterations:  2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(d.items())`; time: 0.741; iterations:  2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(d.items())`; time: 7.148; iterations:  2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(**d)`;       time: 0.156; iterations:  1000000
Dictionary size:    5; Type:        Map; Statement: `constructor(**d)`;       time: 0.403; iterations:  1000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(**d)`;       time: 3.533; iterations:  1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(self)`;      time: 1.789; iterations: 10000000
Dictionary size:    5; Type:        Map; Statement: `constructor(self)`;      time: 0.700; iterations: 10000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(self)`;      time: 28.039; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d1 == d2`;               time: 1.306; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `d1 == d2`;               time: 0.629; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `d1 == d2`;               time: 1.326; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `self == self`;           time: 1.276; iterations: 20000000
Dictionary size:    5; Type:        Map; Statement: `self == self`;           time: 0.535; iterations: 20000000
Dictionary size:    5; Type: frozendict; Statement: `self == self`;           time: 1.313; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `repr(d)`;                time: 0.782; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `repr(d)`;                time: 1.093; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `repr(d)`;                time: 0.121; iterations:   600000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `str(d)`;                 time: 0.826; iterations:   600000
Dictionary size:    5; Type:        Map; Statement: `str(d)`;                 time: 1.121; iterations:   600000
Dictionary size:    5; Type: frozendict; Statement: `str(d)`;                 time: 0.151; iterations:   600000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;             time: 0.795; iterations: 13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;             time: 0.929; iterations: 13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;             time: 0.935; iterations: 13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                 time: 0.325; iterations: 10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                 time: 0.454; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                 time: 0.827; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;               time: 0.465; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;               time: 0.623; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;               time: 1.028; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;           time: 0.470; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;           time: 0.612; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;           time: 0.925; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;        time: 0.631; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;        time: 0.982; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;        time: 0.773; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;     time: 0.582; iterations:     4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;     time: 1.317; iterations:     4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;     time: 1.054; iterations:     4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                time: 0.465; iterations: 10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                time: 1.878; iterations: 10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                 time: 0.949; iterations: 20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                 time: 0.969; iterations: 20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                 time: 0.950; iterations: 20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;               time: 0.819; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;               time: 1.829; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;               time: 0.806; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;             time: 0.802; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;             time: 1.864; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;             time: 0.797; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;              time: 0.806; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;              time: 1.706; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;              time: 0.804; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                time: 0.811; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                time: 1.844; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                time: 0.808; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;      time: 0.197; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;      time: 1.904; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;      time: 0.718; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(d.items())`; time: 0.392; iterations:    10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(d.items())`; time: 1.705; iterations:    10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(d.items())`; time: 0.926; iterations:    10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;       time: 0.097; iterations:     5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;       time: 0.860; iterations:     5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;       time: 0.846; iterations:     5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;      time: 0.970; iterations:    50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;      time: 0.003; iterations:    50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;      time: 1.163; iterations:    50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;               time: 0.901; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;               time: 0.003; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;               time: 0.911; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;           time: 0.903; iterations:   100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;           time: 0.003; iterations:   100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;           time: 0.899; iterations:   100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                time: 0.552; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                time: 1.032; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                time: 0.001; iterations:     3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                 time: 0.559; iterations:     3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                 time: 1.019; iterations:     3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                 time: 0.001; iterations:     3000
```

`d[key]` and `key in d` is strangely slower, and constructors too. It seems 
this is caused by the overhead of the superclass (`frozendict` inherits 
`dict`).

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
