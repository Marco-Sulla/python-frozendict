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
# ('Marco', 3)

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
Dictionary size:    5; Type:       dict; Statement: `d.get(key)`;                    time: 0.839; iterations:   13000000
Dictionary size:    5; Type:        Map; Statement: `d.get(key)`;                    time: 0.864; iterations:   13000000
Dictionary size:    5; Type: frozendict; Statement: `d.get(key)`;                    time: 0.868; iterations:   13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d[key]`;                        time: 0.350; iterations:   10000000
Dictionary size:    5; Type:        Map; Statement: `d[key]`;                        time: 0.402; iterations:   10000000
Dictionary size:    5; Type: frozendict; Statement: `d[key]`;                        time: 0.826; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key in d`;                      time: 0.620; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `key in d`;                      time: 0.509; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `key in d`;                      time: 0.930; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `key not in d`;                  time: 0.519; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `key not in d`;                  time: 0.780; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `key not in d`;                  time: 0.978; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.dumps(d)`;               time: 0.626; iterations:    1000000
Dictionary size:    5; Type:        Map; Statement: `pickle.dumps(d)`;               time: 2.038; iterations:    1000000
Dictionary size:    5; Type: frozendict; Statement: `pickle.dumps(d)`;               time: 2.010; iterations:    1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `pickle.loads(dump)`;            time: 0.741; iterations:     800000
Dictionary size:    5; Type:        Map; Statement: `pickle.loads(dump)`;            time: 1.352; iterations:     800000
Dictionary size:    5; Type: frozendict; Statement: `pickle.loads(dump)`;            time: 5.166; iterations:     800000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:        Map; Statement: `hash(d)`;                       time: 0.475; iterations:   10000000
Dictionary size:    5; Type: frozendict; Statement: `hash(d)`;                       time: 1.749; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `len(d)`;                        time: 0.658; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `len(d)`;                        time: 0.658; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `len(d)`;                        time: 0.652; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.keys()`;                      time: 2.342; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `d.keys()`;                      time: 3.162; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `d.keys()`;                      time: 2.446; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.values()`;                    time: 2.369; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `d.values()`;                    time: 3.073; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `d.values()`;                    time: 2.405; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d.items()`;                     time: 1.706; iterations:   10000000
Dictionary size:    5; Type:        Map; Statement: `d.items()`;                     time: 2.433; iterations:   10000000
Dictionary size:    5; Type: frozendict; Statement: `d.items()`;                     time: 1.741; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `iter(d)`;                       time: 2.338; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `iter(d)`;                       time: 2.929; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `iter(d)`;                       time: 2.295; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(dict)`;             time: 0.361; iterations:    2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(dict)`;             time: 0.817; iterations:    2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(dict)`;             time: 9.058; iterations:    2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(tuple(d.items()))`; time: 0.717; iterations:    2000000
Dictionary size:    5; Type:        Map; Statement: `constructor(tuple(d.items()))`; time: 0.750; iterations:    2000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(tuple(d.items()))`; time: 9.472; iterations:    2000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(**d)`;              time: 0.154; iterations:    1000000
Dictionary size:    5; Type:        Map; Statement: `constructor(**d)`;              time: 0.390; iterations:    1000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(**d)`;              time: 4.600; iterations:    1000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `constructor(self)`;             time: 1.784; iterations:   10000000
Dictionary size:    5; Type:        Map; Statement: `constructor(self)`;             time: 0.666; iterations:   10000000
Dictionary size:    5; Type: frozendict; Statement: `constructor(self)`;             time: 41.362; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `d1 == d2`;                      time: 1.304; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `d1 == d2`;                      time: 0.623; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `d1 == d2`;                      time: 1.298; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `self == self`;                  time: 1.313; iterations:   20000000
Dictionary size:    5; Type:        Map; Statement: `self == self`;                  time: 0.534; iterations:   20000000
Dictionary size:    5; Type: frozendict; Statement: `self == self`;                  time: 1.309; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `repr(d)`;                       time: 0.780; iterations:     600000
Dictionary size:    5; Type:        Map; Statement: `repr(d)`;                       time: 1.111; iterations:     600000
Dictionary size:    5; Type: frozendict; Statement: `repr(d)`;                       time: 0.127; iterations:     600000
////////////////////////////////////////////////////////////////////////////////
Dictionary size:    5; Type:       dict; Statement: `str(d)`;                        time: 0.826; iterations:     600000
Dictionary size:    5; Type:        Map; Statement: `str(d)`;                        time: 1.129; iterations:     600000
Dictionary size:    5; Type: frozendict; Statement: `str(d)`;                        time: 0.146; iterations:     600000
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.get(key)`;                    time: 0.796; iterations:   13000000
Dictionary size: 1000; Type:        Map; Statement: `d.get(key)`;                    time: 0.920; iterations:   13000000
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`;                    time: 1.045; iterations:   13000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d[key]`;                        time: 0.321; iterations:   10000000
Dictionary size: 1000; Type:        Map; Statement: `d[key]`;                        time: 0.484; iterations:   10000000
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`;                        time: 0.793; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key in d`;                      time: 0.547; iterations:   20000000
Dictionary size: 1000; Type:        Map; Statement: `key in d`;                      time: 0.574; iterations:   20000000
Dictionary size: 1000; Type: frozendict; Statement: `key in d`;                      time: 0.941; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `key not in d`;                  time: 0.545; iterations:   20000000
Dictionary size: 1000; Type:        Map; Statement: `key not in d`;                  time: 0.561; iterations:   20000000
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`;                  time: 0.916; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.dumps(d)`;               time: 0.629; iterations:       5000
Dictionary size: 1000; Type:        Map; Statement: `pickle.dumps(d)`;               time: 0.975; iterations:       5000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.dumps(d)`;               time: 0.764; iterations:       5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `pickle.loads(dump)`;            time: 0.569; iterations:       4000
Dictionary size: 1000; Type:        Map; Statement: `pickle.loads(dump)`;            time: 1.312; iterations:       4000
Dictionary size: 1000; Type: frozendict; Statement: `pickle.loads(dump)`;            time: 1.018; iterations:       4000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:        Map; Statement: `hash(d)`;                       time: 0.497; iterations:   10000000
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`;                       time: 1.786; iterations:   10000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `len(d)`;                        time: 0.870; iterations:   20000000
Dictionary size: 1000; Type:        Map; Statement: `len(d)`;                        time: 0.879; iterations:   20000000
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`;                        time: 0.877; iterations:   20000000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.keys()`;                      time: 0.814; iterations:     100000
Dictionary size: 1000; Type:        Map; Statement: `d.keys()`;                      time: 1.778; iterations:     100000
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`;                      time: 0.820; iterations:     100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.values()`;                    time: 0.801; iterations:     100000
Dictionary size: 1000; Type:        Map; Statement: `d.values()`;                    time: 1.815; iterations:     100000
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`;                    time: 0.804; iterations:     100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d.items()`;                     time: 0.756; iterations:      50000
Dictionary size: 1000; Type:        Map; Statement: `d.items()`;                     time: 1.753; iterations:      50000
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`;                     time: 0.755; iterations:      50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `iter(d)`;                       time: 0.807; iterations:     100000
Dictionary size: 1000; Type:        Map; Statement: `iter(d)`;                       time: 1.804; iterations:     100000
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`;                       time: 0.853; iterations:     100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(dict)`;             time: 0.204; iterations:      10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(dict)`;             time: 1.763; iterations:      10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`;             time: 0.733; iterations:      10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(tuple(d.items()))`; time: 0.401; iterations:      10000
Dictionary size: 1000; Type:        Map; Statement: `constructor(tuple(d.items()))`; time: 1.669; iterations:      10000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(tuple(d.items()))`; time: 0.924; iterations:      10000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(**d)`;              time: 0.096; iterations:       5000
Dictionary size: 1000; Type:        Map; Statement: `constructor(**d)`;              time: 0.847; iterations:       5000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`;              time: 0.640; iterations:       5000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `constructor(self)`;             time: 1.010; iterations:      50000
Dictionary size: 1000; Type:        Map; Statement: `constructor(self)`;             time: 0.003; iterations:      50000
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`;             time: 1.236; iterations:      50000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `d1 == d2`;                      time: 0.903; iterations:     100000
Dictionary size: 1000; Type:        Map; Statement: `d1 == d2`;                      time: 0.003; iterations:     100000
Dictionary size: 1000; Type: frozendict; Statement: `d1 == d2`;                      time: 0.909; iterations:     100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `self == self`;                  time: 0.896; iterations:     100000
Dictionary size: 1000; Type:        Map; Statement: `self == self`;                  time: 0.003; iterations:     100000
Dictionary size: 1000; Type: frozendict; Statement: `self == self`;                  time: 0.888; iterations:     100000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `repr(d)`;                       time: 0.569; iterations:       3000
Dictionary size: 1000; Type:        Map; Statement: `repr(d)`;                       time: 1.041; iterations:       3000
Dictionary size: 1000; Type: frozendict; Statement: `repr(d)`;                       time: 0.001; iterations:       3000
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type:       dict; Statement: `str(d)`;                        time: 0.560; iterations:       3000
Dictionary size: 1000; Type:        Map; Statement: `str(d)`;                        time: 1.006; iterations:       3000
Dictionary size: 1000; Type: frozendict; Statement: `str(d)`;                        time: 0.001; iterations:       3000
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
