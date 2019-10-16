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
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `d.get(key)`; time: 0.6404073936864734
Dictionary size: 5; Type: Map; Statement: `d.get(key)`; time: 0.8398521831259131
Dictionary size: 5; Type: frozendict; Statement: `d.get(key)`; time: 0.7333620935678482
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `d[key]`; time: 0.3543422678485513
Dictionary size: 5; Type: Map; Statement: `d[key]`; time: 0.4251683773472905
Dictionary size: 5; Type: frozendict; Statement: `d[key]`; time: 0.8944470779970288
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `key in d`; time: 0.25107845198363066
Dictionary size: 5; Type: Map; Statement: `key in d`; time: 0.4149868739768863
Dictionary size: 5; Type: frozendict; Statement: `key in d`; time: 0.5072012739256024
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `key not in d`; time: 0.27066949661821127
Dictionary size: 5; Type: Map; Statement: `key not in d`; time: 0.28093732707202435
Dictionary size: 5; Type: frozendict; Statement: `key not in d`; time: 0.4915514634922147
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `pickle`; time: 0.0015882188454270363
Dictionary size: 5; Type: Map; Statement: `pickle`; time: 0.007595198228955269
Dictionary size: 5; Type: frozendict; Statement: `pickle`; time: 0.01410688366740942
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: Map; Statement: `hash(d)`; time: 0.49810644518584013
Dictionary size: 5; Type: frozendict; Statement: `hash(d)`; time: 1.4157478529959917
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `len(d)`; time: 0.3665856886655092
Dictionary size: 5; Type: Map; Statement: `len(d)`; time: 0.35659957490861416
Dictionary size: 5; Type: frozendict; Statement: `len(d)`; time: 0.36777565628290176
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `d.keys()`; time: 0.012457741424441338
Dictionary size: 5; Type: Map; Statement: `d.keys()`; time: 0.015815681777894497
Dictionary size: 5; Type: frozendict; Statement: `d.keys()`; time: 0.01351218018680811
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `d.values()`; time: 0.012507420964539051
Dictionary size: 5; Type: Map; Statement: `d.values()`; time: 0.016471431590616703
Dictionary size: 5; Type: frozendict; Statement: `d.values()`; time: 0.012361526489257812
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `d.items()`; time: 0.018460323102772236
Dictionary size: 5; Type: Map; Statement: `d.items()`; time: 0.02549740858376026
Dictionary size: 5; Type: frozendict; Statement: `d.items()`; time: 0.01748696807771921
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `iter(d)`; time: 0.013251944445073605
Dictionary size: 5; Type: Map; Statement: `iter(d)`; time: 0.014584753662347794
Dictionary size: 5; Type: frozendict; Statement: `iter(d)`; time: 0.01282238494604826
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `constructor(dict)`; time: 0.0017991233617067337
Dictionary size: 5; Type: Map; Statement: `constructor(dict)`; time: 0.004049944691359997
Dictionary size: 5; Type: frozendict; Statement: `constructor(dict)`; time: 0.068474599160254
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `constructor(tuple(d.items()))`; time: 0.0035259947180747986
Dictionary size: 5; Type: Map; Statement: `constructor(tuple(d.items()))`; time: 0.003862365148961544
Dictionary size: 5; Type: frozendict; Statement: `constructor(tuple(d.items()))`; time: 0.07279269304126501
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `constructor(**d)`; time: 0.0014834655448794365
Dictionary size: 5; Type: Map; Statement: `constructor(**d)`; time: 0.005941973067820072
Dictionary size: 5; Type: frozendict; Statement: `constructor(**d)`; time: 0.08952728938311338
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 5; Type: dict; Statement: `constructor(self)`; time: 0.021734904497861862
Dictionary size: 5; Type: Map; Statement: `constructor(self)`; time: 0.008985992521047592
Dictionary size: 5; Type: frozendict; Statement: `constructor(self)`; time: 0.4039854137226939
################################################################################
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `d.get(key)`; time: 0.6351042548194528
Dictionary size: 1000; Type: Map; Statement: `d.get(key)`; time: 0.7028853939846158
Dictionary size: 1000; Type: frozendict; Statement: `d.get(key)`; time: 0.660289959050715
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `d[key]`; time: 0.3358355574309826
Dictionary size: 1000; Type: Map; Statement: `d[key]`; time: 0.4900661613792181
Dictionary size: 1000; Type: frozendict; Statement: `d[key]`; time: 0.9077386716380715
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `key in d`; time: 0.23840515036135912
Dictionary size: 1000; Type: Map; Statement: `key in d`; time: 0.305002236738801
Dictionary size: 1000; Type: frozendict; Statement: `key in d`; time: 0.4551010709255934
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `key not in d`; time: 0.23901387955993414
Dictionary size: 1000; Type: Map; Statement: `key not in d`; time: 0.30526933167129755
Dictionary size: 1000; Type: frozendict; Statement: `key not in d`; time: 0.5060138450935483
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `pickle`; time: 0.3483383385464549
Dictionary size: 1000; Type: Map; Statement: `pickle`; time: 0.6261633019894361
Dictionary size: 1000; Type: frozendict; Statement: `pickle`; time: 0.7198446122929454
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: Map; Statement: `hash(d)`; time: 0.5203868690878153
Dictionary size: 1000; Type: frozendict; Statement: `hash(d)`; time: 1.4172934535890818
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `len(d)`; time: 0.46103369910269976
Dictionary size: 1000; Type: Map; Statement: `len(d)`; time: 0.5159762632101774
Dictionary size: 1000; Type: frozendict; Statement: `len(d)`; time: 0.47666538320481777
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `d.keys()`; time: 0.8257003212347627
Dictionary size: 1000; Type: Map; Statement: `d.keys()`; time: 1.9189182091504335
Dictionary size: 1000; Type: frozendict; Statement: `d.keys()`; time: 0.9059777185320854
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `d.values()`; time: 0.8014922793954611
Dictionary size: 1000; Type: Map; Statement: `d.values()`; time: 1.900040527805686
Dictionary size: 1000; Type: frozendict; Statement: `d.values()`; time: 0.8274175515398383
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `d.items()`; time: 1.5621327869594097
Dictionary size: 1000; Type: Map; Statement: `d.items()`; time: 3.454783245921135
Dictionary size: 1000; Type: frozendict; Statement: `d.items()`; time: 1.5342026641592383
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `iter(d)`; time: 0.8342807488515973
Dictionary size: 1000; Type: Map; Statement: `iter(d)`; time: 1.9118214435875416
Dictionary size: 1000; Type: frozendict; Statement: `iter(d)`; time: 0.8299530521035194
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `constructor(dict)`; time: 0.19477931130677462
Dictionary size: 1000; Type: Map; Statement: `constructor(dict)`; time: 1.8007300645112991
Dictionary size: 1000; Type: frozendict; Statement: `constructor(dict)`; time: 2.898253229446709
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `constructor(tuple(d.items()))`; time: 0.3937703538686037
Dictionary size: 1000; Type: Map; Statement: `constructor(tuple(d.items()))`; time: 1.7514557195827365
Dictionary size: 1000; Type: frozendict; Statement: `constructor(tuple(d.items()))`; time: 3.1277628084644675
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `constructor(**d)`; time: 0.1946127936244011
Dictionary size: 1000; Type: Map; Statement: `constructor(**d)`; time: 1.7412115084007382
Dictionary size: 1000; Type: frozendict; Statement: `constructor(**d)`; time: 3.9152183709666133
////////////////////////////////////////////////////////////////////////////////
Dictionary size: 1000; Type: dict; Statement: `constructor(self)`; time: 1.9696954665705562
Dictionary size: 1000; Type: Map; Statement: `constructor(self)`; time: 0.006853778846561909
Dictionary size: 1000; Type: frozendict; Statement: `constructor(self)`; time: 2.4460258912295103
```

`d[key]` and `key in d` is strangely slower, probably because there's the 
overhead of the superclass (`frozendict` inherits `dict`).
The other methods are comparable with `dict` and `immutables.Map`, and 
sometimes faster than `immutables.Map`. Constructors are much slower, but I 
suppose this is because `frozendict` checks if values are hashable, while 
`immutables.Map` not, so it is not **really** immutable. 
Where `immutables.Map` is really fast is in creating a copy of itself, and 
this is because it's written in C. It has not to invoke the `dict` constructor
but can simply copy its attributes.

I think a really good solution is to create a `C` `basedict` and 
`frozendict`, and let `dict` and `frozendict` inherits from `basedict`, a sort
of `C` version of `collections.abc.Mapping`. IMHO this solution is much better 
than the proposal in [PEP 603](https://www.python.org/dev/peps/pep-0603/)
