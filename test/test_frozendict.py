from frozendict import frozendict
import pytest
import pickle

################################################################################
# dict fixtures

@pytest.fixture
def fd_dict():
    return {"Sulla": "Marco", "Hicks": "Bill", frozendict({1: 2}): "frozen"}

@pytest.fixture
def fd_dict_eq():
    return {"Hicks": "Bill", "Sulla": "Marco", frozendict({1: 2}): "frozen"}

def fd_dict_2_raw():
    return {"Sulla": "Marco", "Hicks": "Bill", "frozen": frozendict({1: 2})}

fd_dict_2 = pytest.fixture(fd_dict_2_raw)

@pytest.fixture
def fd_dict_bad_raw():
    return {"Sulla": "Hitler", "Hicks": "Stalin"}

@pytest.fixture
def fd_nested_raw():
    return {
        "Sulla": ("Marco", "Adele", "Mario", "Giulia"), 
        "Hicks": ("Bill", ), 
        "others": (frozendict({
            "comedians": ["Woody Allen", "George Carlin", "Emo Philips", "Groucho Marx", "Corrado Guzzanti"],
            "comedies": ["Bananas", "Dogma", "E=mo²", "A Night at the Opera", "Fascisti su Marte"]
        }))
    }

def math_dict_raw():
    return {"Sulla": "Marò", 5: 7}

math_dict = pytest.fixture(math_dict_raw)

################################################################################
# frozendict fixtures

@pytest.fixture
def fd(fd_dict):
    return frozendict(fd_dict)

@pytest.fixture
def fd_unhashable():
    return frozendict({1: []})

@pytest.fixture
def fd_eq(fd_dict_eq):
    return frozendict(fd_dict_eq)

def fd2_raw():
    return frozendict(fd_dict_2_raw())

fd2 = pytest.fixture(fd2_raw)

@pytest.fixture
def fd_bad(fd_dict_bad_raw):
    return frozendict(fd_dict_bad_raw)

@pytest.fixture
def fd_nested(fd_nested_raw):
    return frozendict(fd_nested_raw)

def math_fd_raw(math_dict):
    return frozendict(math_dict)

def math_items_raw(math_dict):
    return tuple(math_dict.items())

@pytest.fixture
def fd_giulia():
    return frozendict({'Marco': 'Sulla', 'Giulia': 'Sulla'})

@pytest.fixture
def fd_items(fd_dict):
    return tuple(fd_dict.items())

@pytest.fixture
def fd_empty():
    return frozendict()

@pytest.fixture
def fd_repr(fd_dict):
    return f"{frozendict.__name__}({repr(fd_dict)})"

################################################################################
# main tests

def test_normalget(fd):
    assert fd["Sulla"] == "Marco"

def test_keyerror(fd):
    with pytest.raises(KeyError):
        fd["God"]

def test_len(fd, fd_dict):
    assert len(fd) == len(fd_dict)

def test_in_true(fd):
    assert "Sulla" in fd

def test_not_in_false(fd):
    assert not ("Sulla" not in fd)

def test_in_false(fd):
    assert not ("God" in fd)

def test_not_in_true(fd):
    assert "God" not in fd

def test_bool_true(fd):
    assert fd

def test_bool_false(fd_empty):
    assert not fd_empty

def test_copy(fd):
    fd2 = fd.copy()
    assert fd2 is fd

def test_not_equal(fd, fd_giulia):
    assert fd != fd_giulia

def test_equals_dict(fd, fd_dict):
    assert fd == fd_dict

def test_hash(fd, fd_eq):
    assert hash(fd)
    assert hash(fd) == hash(fd_eq)

def test_hash_no_errors(fd, fd_eq):
    assert fd.hash_no_errors()
    assert fd.hash_no_errors() == fd_eq.hash_no_errors()

def test_pickle(fd):
    fd_unpickled = pickle.loads(pickle.dumps(fd))
    assert fd_unpickled == fd

def test_empty(fd_empty):
    assert fd_empty is frozendict({}) is frozendict([])

def test_constructor_self(fd):
    assert fd is frozendict(fd)

def test_constructor_kwargs(fd2, fd_dict_2):
    assert frozendict(**fd_dict_2) == fd2

def test_constructor_iterator(fd, fd_items):
    assert frozendict(fd_items) == fd

def test_sorted_keys(fd2, fd_dict_2):
    fd_sorted = fd2.sorted()
    assert list(fd_sorted) == sorted(fd_dict_2)
    assert fd_sorted is fd_sorted.sorted()

def test_sorted_values(fd, fd_dict):
    fd_sorted = fd.sorted(by="values")
    
    res = []
    
    for k, v in fd_dict.items():
        if not res:
            res.append((k, v))
        else:
            pos = None
            
            for i, entry in enumerate(res):
                if v < entry[1]:
                    pos = i
                    break
        
            if pos is None:
                res.append((k, v))
            else:
                res.insert(pos, (k, v))
    
    assert list(fd_sorted.items()) == res
    assert fd_sorted is fd_sorted.sorted(by="values")

def test_sorted_empty(fd_empty):
    assert fd_empty.sorted() is fd_empty

def test_sorted_bad_by(fd):
    with pytest.raises(ValueError):
        fd_sorted = fd.sorted(by="value")

def test_unhashable_value(fd_unhashable):
    with pytest.raises(TypeError):
        hash(fd_unhashable)

    # hash is cached
    with pytest.raises(TypeError):
        hash(fd_unhashable)

def test_unhashable_value_no_errors(fd_unhashable):
    assert fd_unhashable.hash_no_errors() == -1
    # hash is cached
    assert fd_unhashable.hash_no_errors() == -1

def test_todict(fd, fd_dict):
    assert dict(fd) == fd_dict

def test_get(fd):
    assert fd.get("Sulla") == "Marco"

def test_get_fail(fd):
    default = object()
    assert fd.get("God", default) is default

def test_get_deep(fd_nested):
    excuse = "Not a bug, work for linter"
    assert fd_nested.get_deep(("Hicks",)) == ("Bill", )
    assert fd_nested.get_deep("others", "comedies", 4) == "Fascisti su Marte"
    assert fd_nested.get_deep("others", "comedians", 1000, default=excuse) == excuse
    
    with pytest.raises(KeyError):
        fd_nested.get_deep("others", "fascists")
    
    with pytest.raises(IndexError):
        fd_nested.get_deep("Sulla", 88)

def test_keys(fd, fd_dict):
    assert tuple(fd.keys()) == tuple(fd_dict.keys())

def test_values(fd, fd_dict):
    assert tuple(fd.values()) == tuple(fd_dict.values())

def test_items(fd, fd_dict):
    assert tuple(fd.items()) == tuple(fd_dict.items())

def test_fromkeys(fd, fd_giulia):
    assert frozendict.fromkeys(["Marco", "Giulia"], "Sulla") == fd_giulia

def test_repr(fd, fd_repr):
    assert repr(fd) == fd_repr

def test_str(fd, fd_repr):
    assert str(fd) == fd_repr

def test_format(fd, fd_repr):
    assert format(fd) == fd_repr

def test_iter(fd):
    items = []

    for x in iter(fd):
        items.append((x, fd[x]))

    assert tuple(fd.items()) == tuple(items)

@pytest.mark.parametrize("addend", (
    math_dict_raw(), 
    math_fd_raw(math_dict_raw()), 
    pytest.param("hell-o", marks=pytest.mark.xfail),
))
def test_add(fd, addend):
    fd_copy = fd.copy()
    newd = dict(fd)
    newd.update(addend)
    newfrozen = frozendict(newd)
    assert fd + addend == newfrozen
    assert fd is fd_copy
    fd += addend
    assert fd == newfrozen

@pytest.mark.parametrize("subtrahend", (
    math_dict_raw(), 
    math_fd_raw(math_dict_raw()), 
    math_items_raw(math_dict_raw()),
))
def test_sub(fd, fd_dict, subtrahend):
    fd_copy = fd.copy()
    newd = {k: v for k, v in fd.items() if k not in subtrahend}
    newfrozen = frozendict(newd)
    assert fd - subtrahend == newfrozen
    assert fd is fd_copy
    fd -= subtrahend
    assert fd == newfrozen

@pytest.mark.parametrize("other", (
    fd2_raw(), 
    ("frozen", "Sulla", "Hicks"), 
    pytest.param(5, marks=pytest.mark.xfail),
))
def test_bitwise_and(fd_eq, other):
    assert fd_eq & other == {"Sulla": "Marco", "Hicks": "Bill"}


def test_bitwise_and_wins_last(fd_bad, fd2):
    assert fd_bad & fd2 == {"Sulla": "Marco", "Hicks": "Bill"}

def test_isdisjoint_true(fd, fd_empty):
    assert fd.isdisjoint(fd_empty)
    assert fd_empty.isdisjoint(fd)
    assert fd.isdisjoint({1: 2})

def test_isdisjoint_false(fd, fd_bad, fd_dict_bad_raw):
    assert not fd.isdisjoint(fd_bad)
    assert not fd_bad.isdisjoint(fd)
    assert not fd.isdisjoint(fd_dict_bad_raw)


################################################################################
# immutability tests

def test_normalset(fd):
    with pytest.raises(NotImplementedError):
        fd["Sulla"] = "Silla"

def test_del(fd):
    with pytest.raises(NotImplementedError):
        del fd["Sulla"]

def test_clear(fd):
    with pytest.raises(NotImplementedError):
        fd.clear()

def test_pop(fd):
    with pytest.raises(NotImplementedError):
        fd.pop("Sulla")

def test_popitem(fd):
    with pytest.raises(NotImplementedError):
        fd.popitem()

def test_setdefault(fd):
    with pytest.raises(NotImplementedError):
        fd.setdefault("Sulla")

def test_update(fd):
    with pytest.raises(NotImplementedError):
        fd.update({"God": "exists"})

def test_init(fd):
    with pytest.raises(NotImplementedError):
        fd.__init__({"Trump": "Donald"})

def test_vars(fd):
    with pytest.raises(TypeError):
        vars(fd)

def test_initialized(fd):
    assert fd.initialized

def test_setattr(fd):
    with pytest.raises(NotImplementedError):
        fd.initialized = False

def test_delattr(fd):
    with pytest.raises(NotImplementedError):
        del fd.initialized

def test_delvar(fd):
    del fd

    with pytest.raises(NameError):
        fd
