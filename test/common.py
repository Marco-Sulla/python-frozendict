import pytest
import pickle
from copy import copy, deepcopy
import sys
from collections.abc import MutableMapping

class Map(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]
    
    def __iter__(self):
        return iter(self._dict)
    
    def __len__(self):
        return len(self._dict)

pyversion = sys.version_info
pyversion_major = pyversion[0]
pyversion_minor = pyversion[1]

##############################################################################
# dict fixtures

@pytest.fixture
def fd_dict():
    return {"Sulla": "Marco", "Hicks": "Bill", frozendict_class({1: 2}): "frozen"}

@pytest.fixture
def fd_dict_hole(fd_dict):
    new_dict = fd_dict.copy()
    del new_dict["Sulla"]
    return new_dict

@pytest.fixture
def fd_dict_eq():
    return {"Hicks": "Bill", "Sulla": "Marco", frozendict_class({1: 2}): "frozen"}

def fd_dict_2_raw():
    return {"Sulla": "Marco", "Hicks": "Bill", "frozen": frozendict_class({1: 2})}

@pytest.fixture
def fd_dict_giulia():
    return {'Marco': 'Sulla', 'Giulia': 'Sulla'}

fd_dict_2 = pytest.fixture(fd_dict_2_raw)

@pytest.fixture
def generator_seq2(fd_dict):
    seq2 = list(fd_dict.items())
    seq2.append(("Sulla", "Mario"))
    return (x for x in seq2)

##############################################################################
# frozendict fixtures

@pytest.fixture
def fd(fd_dict):
    return frozendict_class(fd_dict)

@pytest.fixture
def fd_hole(fd_dict_hole):
    return frozendict_class(fd_dict_hole)

@pytest.fixture
def fd_unhashable():
    return frozendict_class({1: []})

@pytest.fixture
def fd_eq(fd_dict_eq):
    return frozendict_class(fd_dict_eq)

def fd2_raw():
    return frozendict_class(fd_dict_2_raw())

fd2 = pytest.fixture(fd2_raw)

@pytest.fixture
def fd_giulia(fd_dict_giulia):
    return frozendict_class(fd_dict_giulia)

@pytest.fixture
def fd_items(fd_dict):
    return tuple(fd_dict.items())

@pytest.fixture
def fd_empty():
    return frozendict_class()

@pytest.fixture
def module_prefix():
    try:
        sc = subclass
    except NameError:
        sc = False
    
    if sc:
        return ""
    
    return "frozendict."

##############################################################################
# main tests

def test_bool_false(fd_empty):
    assert not fd_empty

def test_constructor_kwargs(fd2, fd_dict_2):
    assert frozendict_class(**fd_dict_2) == fd2

def test_constructor_self(fd):
    assert fd == frozendict_class(fd, Sulla="Marco")

def test_constructor_generator(fd, generator_seq2):
    assert fd == frozendict_class(generator_seq2, Sulla="Marco")

def test_constructor_hole(fd_hole, fd_dict_hole):
    assert fd_hole == frozendict_class(fd_dict_hole)

def test_constructor_map(fd_dict):
    m = Map(fd_dict)
    assert frozendict_class(m) == fd_dict

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

def test_copycopy(fd):
    fd3 = copy(fd)
    assert fd3 == fd

def test_deepcopy(fd):
    fd2 = deepcopy(fd)
    assert fd2 == fd

def test_deepcopy_unhashable(fd_unhashable):
    fd2 = deepcopy(fd_unhashable)
    assert fd2 == fd_unhashable
    assert fd2 is not fd_unhashable

def test_not_equal(fd, fd_giulia):
    assert fd != fd_giulia

def test_equals_dict(fd, fd_dict):
    assert fd == fd_dict

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle(fd, protocol):
    dump = pickle.dumps(fd, protocol=protocol)
    assert dump
    fd_unpickled = pickle.loads(dump)
    assert fd_unpickled == fd

def test_constructor_iterator(fd, fd_items):
    assert frozendict_class(fd_items) == fd

def test_todict(fd, fd_dict):
    assert dict(fd) == fd_dict

def test_get(fd):
    assert fd.get("Sulla") == "Marco"

def test_get_fail(fd):
    default = object()
    assert fd.get("God", default) is default

def test_keys(fd, fd_dict):
    assert tuple(fd.keys()) == tuple(fd_dict.keys())

def test_values(fd, fd_dict):
    assert tuple(fd.values()) == tuple(fd_dict.values())

def test_items(fd, fd_dict):
    assert tuple(fd.items()) == tuple(fd_dict.items())

def test_fromkeys(fd_giulia):
    assert frozendict_class.fromkeys(["Marco", "Giulia"], "Sulla") == fd_giulia

def test_fromkeys_dict(fd_giulia, fd_dict_giulia):
    assert frozendict_class.fromkeys(fd_dict_giulia, "Sulla") == fd_giulia

def test_fromkeys_set(fd_giulia, fd_dict_giulia):
    assert frozendict_class.fromkeys(set(fd_dict_giulia), "Sulla") == fd_giulia

def test_repr(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    repr_fd = repr(fd)
    prefix = module_prefix
    expected_repr = f"{prefix}{classname}({repr(fd_dict)})"
    assert repr_fd == expected_repr

def test_str(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    prefix = module_prefix
    assert str(fd) == f"{prefix}{classname}({repr(fd_dict)})"

def test_format(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    prefix = module_prefix
    assert format(fd) == f"{prefix}{classname}({repr(fd_dict)})"

def test_iter(fd):
    items = []

    for x in iter(fd):
        items.append((x, fd[x]))

    assert tuple(items) == tuple(fd.items())

def test_sum(fd, fd_dict, fd_dict_giulia):
    new_fd = fd | fd_dict_giulia
    new_dict = dict(fd_dict)
    new_dict.update(fd_dict_giulia)
    assert new_fd == new_dict

def test_union(fd_dict, fd_giulia):
    new_fd = frozendict_class(fd_dict)
    id_fd = id(new_fd)
    new_fd |= fd_giulia
    assert id_fd != id(new_fd)
    new_dict = dict(fd_dict)
    new_dict.update(fd_giulia)
    assert new_fd == new_dict

def test_reversed(fd, fd_dict):
    assert(tuple(reversed(fd)) == tuple(reversed(tuple(fd_dict))))

def test_iter_len(fd):
    assert iter(fd).__length_hint__() >= 0

def test_keys_len(fd):
    assert len(fd.keys()) == len(fd)

def test_items_len(fd):
    assert len(fd.items()) == len(fd)

def test_values_len(fd):
    assert len(fd.values()) == len(fd)

def test_equal_keys(fd, fd_dict):
    assert fd.keys() == fd_dict.keys()

def test_equal_items(fd, fd_dict):
    assert fd.items() == fd_dict.items()

def test_in_keys(fd):
    assert "Sulla" in fd.keys()

def test_in_items(fd):
    assert ("Sulla", "Marco") in fd.items()

def test_disjoint_true_keys(fd, fd_giulia):
    assert fd.keys().isdisjoint(fd_giulia)

def test_disjoint_true_items(fd, fd_giulia):
    assert fd.items().isdisjoint(fd_giulia.items())

def test_disjoint_false_keys(fd):
    assert not fd.keys().isdisjoint(fd)

def test_disjoint_false_items(fd):
    assert not fd.items().isdisjoint(fd.items())

def test_sub_keys(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.keys()) - frozenset(fd_dict_2.keys())
    assert fd.keys() - fd2.keys() == res

def test_sub_items(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.items()) - frozenset(fd_dict_2.items())
    assert fd.items() - fd2.items() == res

def test_and_keys(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.keys()) & frozenset(fd_dict_2.keys())
    assert fd.keys() & fd2.keys() == res

def test_and_items(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.items()) & frozenset(fd_dict_2.items())
    assert fd.items() & fd2.items() == res

def test_or_keys(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.keys()) | frozenset(fd_dict_2.keys())
    assert fd.keys() | fd2.keys() == res

def test_or_items(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.items()) | frozenset(fd_dict_2.items())
    assert fd.items() | fd2.items() == res

def test_xor_keys(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.keys()) ^ frozenset(fd_dict_2.keys())
    assert fd.keys() ^ fd2.keys() == res

def test_xor_items(fd, fd_dict, fd2, fd_dict_2):
    res = frozenset(fd_dict.items()) ^ frozenset(fd_dict_2.items())
    assert fd.items() ^ fd2.items() == res

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_iter_key(fd, protocol):
    orig = iter(fd.keys())
    dump = pickle.dumps(orig, protocol=protocol)
    assert dump
    unpickled = pickle.loads(dump)
    assert tuple(unpickled) == tuple(orig)

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_iter_item(fd, protocol):
    orig = iter(fd.items())
    dump = pickle.dumps(orig, protocol=protocol)
    assert dump
    unpickled = pickle.loads(dump)
    assert tuple(unpickled) == tuple(orig)

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_iter_value(fd, protocol):
    orig = iter(fd.values())
    dump = pickle.dumps(orig, protocol=protocol)
    assert dump
    unpickled = pickle.loads(dump)
    assert tuple(unpickled) == tuple(orig)

def test_lt_key(fd, fd_hole):
    assert fd_hole.keys() < fd.keys()

def test_gt_key(fd, fd_hole):
    assert fd.keys() > fd_hole.keys()

def test_le_key(fd, fd_hole):
    assert fd_hole.keys() <= fd.keys()
    assert fd.keys() <= fd.keys()

def test_ge_key(fd, fd_hole):
    assert fd.keys() >= fd_hole.keys()
    assert fd.keys() >= fd.keys()

def test_lt_item(fd, fd_hole):
    assert fd_hole.items() < fd.items()

def test_gt_item(fd, fd_hole):
    assert fd.items() > fd_hole.items()

def test_le_item(fd, fd_hole):
    assert fd_hole.items() <= fd.items()
    assert fd.items() <= fd.items()

def test_ge_item(fd, fd_hole):
    assert fd.items() >= fd_hole.items()
    assert fd.items() >= fd.items()

if c_ext or (
    pyversion_major > 3 or 
    (pyversion_major == 3 and pyversion_minor > 9)
):
    def test_mapping_keys(fd):
        assert fd.keys().mapping == fd
    
    def test_mapping_items(fd):
        assert fd.items().mapping == fd
    
    def test_mapping_values(fd):
        assert fd.values().mapping == fd

if c_ext or (
    pyversion_major > 3 or 
    (pyversion_major == 3 and pyversion_minor > 7)
):
    def test_reversed_keys(fd, fd_dict):
        assert(tuple(reversed(fd.keys())) == tuple(reversed(tuple(fd_dict.keys()))))

    def test_reversed_items(fd, fd_dict):
        assert(tuple(reversed(fd.items())) == tuple(reversed(tuple(fd_dict.items()))))

    def test_reversed_values(fd, fd_dict):
        assert(tuple(reversed(fd.values())) == tuple(reversed(tuple(fd_dict.values()))))

##############################################################################
# frozendict-only tests

def test_hash(fd, fd_eq):
    assert hash(fd)
    assert hash(fd) == hash(fd_eq)

def test_unhashable_value(fd_unhashable):
    with pytest.raises(TypeError):
        hash(fd_unhashable)

    # hash is cached
    with pytest.raises(TypeError):
        hash(fd_unhashable)

##############################################################################
# immutability tests

def test_normalset(fd):
    with pytest.raises(TypeError):
        fd["Sulla"] = "Silla"

def test_del(fd):
    with pytest.raises(TypeError):
        del fd["Sulla"]

def test_clear(fd):
    with pytest.raises(AttributeError):
        fd.clear()

def test_pop(fd):
    with pytest.raises(AttributeError):
        fd.pop("Sulla")

def test_popitem(fd):
    with pytest.raises(AttributeError):
        fd.popitem()

def test_setdefault(fd):
    with pytest.raises(AttributeError):
        fd.setdefault("Sulla")

def test_update(fd):
    with pytest.raises(AttributeError):
        fd.update({"God": "exists"})

def test_delattr(fd):
    with pytest.raises(AttributeError):
        del fd._initialized
