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
    return {"Guzzanti": "Corrado", "Hicks": "Bill", frozendict_class({1: 2}): "frozen"}

@pytest.fixture
def fd_dict_hole(fd_dict):
    new_dict = fd_dict.copy()
    del new_dict["Guzzanti"]
    return new_dict

@pytest.fixture
def fd_dict_eq():
    return {"Hicks": "Bill", "Guzzanti": "Corrado", frozendict_class({1: 2}): "frozen"}

def fd_dict_2_raw():
    return {"Guzzanti": "Corrado", "Hicks": "Bill", "frozen": frozendict_class({1: 2})}

@pytest.fixture
def fd_dict_sabina():
    return {'Corrado': 'Guzzanti', 'Sabina': 'Guzzanti'}

fd_dict_2 = pytest.fixture(fd_dict_2_raw)

@pytest.fixture
def generator_seq2(fd_dict):
    seq2 = list(fd_dict.items())
    seq2.append(("Guzzanti", "Mario"))
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
def fd_sabina(fd_dict_sabina):
    return frozendict_class(fd_dict_sabina)

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
    assert fd == frozendict_class(fd, Guzzanti="Corrado")

def test_constructor_generator(fd, generator_seq2):
    assert fd == frozendict_class(generator_seq2, Guzzanti="Corrado")

def test_constructor_hole(fd_hole, fd_dict_hole):
    assert fd_hole == frozendict_class(fd_dict_hole)

def test_constructor_map(fd_dict):
    assert frozendict_class(Map(fd_dict)) == fd_dict

def test_normalget(fd):
    assert fd["Guzzanti"] == "Corrado"

def test_keyerror(fd):
    with pytest.raises(KeyError):
        fd["Brignano"]

def test_len(fd, fd_dict):
    assert len(fd) == len(fd_dict)

def test_in_true(fd):
    assert "Guzzanti" in fd

def test_not_in_false(fd):
    assert not ("Guzzanti" not in fd)

def test_in_false(fd):
    assert not ("Brignano" in fd)

def test_not_in_true(fd):
    assert "Brignano" not in fd

def test_bool_true(fd):
    assert fd

def test_deepcopy_unhashable(fd_unhashable):
    fd_copy = deepcopy(fd_unhashable)
    assert fd_copy == fd_unhashable
    assert fd_copy is not fd_unhashable

def test_not_equal(fd, fd2, fd_sabina):
    assert fd != fd_sabina
    assert fd != fd2
    assert not (fd == fd_sabina)
    assert not (fd == fd2)

def test_equals_dict(fd, fd_dict):
    assert fd == fd_dict

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle(fd, protocol):
    dump = pickle.dumps(fd, protocol=protocol)
    assert dump
    assert pickle.loads(dump) == fd

def test_constructor_iterator(fd, fd_items):
    assert frozendict_class(fd_items) == fd

def test_todict(fd, fd_dict):
    assert dict(fd) == fd_dict

def test_get(fd):
    assert fd.get("Guzzanti") == "Corrado"

def test_get_fail(fd):
    default = object()
    assert fd.get("Brignano", default) is default

def test_keys(fd, fd_dict):
    assert tuple(fd.keys()) == tuple(fd_dict.keys())

def test_values(fd, fd_dict):
    assert tuple(fd.values()) == tuple(fd_dict.values())

def test_items(fd, fd_dict):
    assert tuple(fd.items()) == tuple(fd_dict.items())

def test_fromkeys(fd_sabina):
    assert frozendict_class.fromkeys(["Corrado", "Sabina"], "Guzzanti") == fd_sabina

def test_fromkeys_dict(fd_sabina, fd_dict_sabina):
    assert frozendict_class.fromkeys(fd_dict_sabina, "Guzzanti") == fd_sabina

def test_fromkeys_set(fd_sabina, fd_dict_sabina):
    assert frozendict_class.fromkeys(set(fd_dict_sabina), "Guzzanti") == fd_sabina

def test_repr(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    assert repr(fd) == f"{module_prefix}{classname}({repr(fd_dict)})"

def test_str(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    assert str(fd) == f"{module_prefix}{classname}({repr(fd_dict)})"

def test_format(fd, fd_dict, module_prefix):
    classname = frozendict_class.__name__
    assert format(fd) == f"{module_prefix}{classname}({repr(fd_dict)})"

def test_iter(fd):
    items = []

    for x in iter(fd):
        items.append((x, fd[x]))

    assert tuple(items) == tuple(fd.items())

def test_sum(fd, fd_dict, fd_dict_sabina):
    new_fd = fd | fd_dict_sabina
    new_dict = dict(fd_dict)
    new_dict.update(fd_dict_sabina)
    assert new_fd == new_dict

def test_union(fd_dict, fd_sabina):
    new_fd = frozendict_class(fd_dict)
    id_fd = id(new_fd)
    new_fd |= fd_sabina
    assert id_fd != id(new_fd)
    new_dict = dict(fd_dict)
    new_dict.update(fd_sabina)
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
    assert "Guzzanti" in fd.keys()

def test_in_items(fd):
    assert ("Guzzanti", "Corrado") in fd.items()

def test_disjoint_true_keys(fd, fd_sabina):
    assert fd.keys().isdisjoint(fd_sabina)

def test_disjoint_true_items(fd, fd_sabina):
    assert fd.items().isdisjoint(fd_sabina.items())

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
    assert tuple(pickle.loads(dump)) == tuple(orig)

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_iter_item(fd, protocol):
    orig = iter(fd.items())
    dump = pickle.dumps(orig, protocol=protocol)
    assert dump
    assert tuple(pickle.loads(dump)) == tuple(orig)

@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_iter_value(fd, protocol):
    orig = iter(fd.values())
    dump = pickle.dumps(orig, protocol=protocol)
    assert dump
    assert tuple(pickle.loads(dump)) == tuple(orig)

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

def test_set_replace(fd_dict, generator_seq2):
    items = tuple(generator_seq2)
    d2 = dict(items)
    assert fd_dict != d2
    fd2 = frozendict_class(items)
    fd3 = fd2.set("Guzzanti", "Corrado")
    assert fd3 == fd_dict

def test_set_add(fd_dict):
    d2 = dict(fd_dict, a="b")
    assert fd_dict != d2
    fd2 = frozendict_class(fd_dict)
    fd3 = fd2.set("a", "b")
    assert fd3 == d2

def test_setdefault_notinsert(fd, fd_dict):
    assert fd.setdefault("Hicks") is fd

def test_setdefault_insert_default(fd, fd_dict):
    fd_dict.setdefault("Allen")
    assert fd_dict == fd.setdefault("Allen")

def test_setdefault_insert(fd, fd_dict):
    fd_dict.setdefault("Allen", "Woody")
    assert fd_dict == fd.setdefault("Allen", "Woody")

def test_del(fd_dict):
    d2 = dict(fd_dict)
    d2["a"] = "b"
    fd2 = frozendict_class(d2)
    fd3 = fd2.delete("a")
    assert fd3 == fd_dict

def test_key(fd):
    assert fd.key() == fd.key(0) == "Guzzanti"
    assert fd.key(1) == fd.key(-2) == "Hicks"

def test_key_out_of_range(fd):
    with pytest.raises(IndexError):
        fd.key(3)
    
    with pytest.raises(IndexError):
        fd.key(-4)

def test_value(fd):
    assert fd.value() == fd.value(0) == "Corrado"
    assert fd.value(1) == fd.value(-2) == "Bill"

def test_value_out_of_range(fd):
    with pytest.raises(IndexError):
        fd.value(3)
    
    with pytest.raises(IndexError):
        fd.value(-4)

def test_item(fd):
    assert fd.item() == fd.item(0) == ("Guzzanti", "Corrado")
    assert fd.item(1) == fd.item(-2) == ("Hicks", "Bill")

def test_item_out_of_range(fd):
    with pytest.raises(IndexError):
        fd.item(3)
    
    with pytest.raises(IndexError):
        fd.item(-4)

##############################################################################
# immutability tests

def test_normalset(fd):
    with pytest.raises(TypeError):
        fd["Guzzanti"] = "Caterina"

def test_del(fd):
    with pytest.raises(TypeError):
        del fd["Guzzanti"]

def test_clear(fd):
    with pytest.raises(AttributeError):
        fd.clear()

def test_pop(fd):
    with pytest.raises(AttributeError):
        fd.pop("Guzzanti")

def test_popitem(fd):
    with pytest.raises(AttributeError):
        fd.popitem()

def test_update(fd):
    with pytest.raises(AttributeError):
        fd.update({"Brignano": "Enrico"})

def test_delattr(fd):
    with pytest.raises(AttributeError):
        del fd._initialized
