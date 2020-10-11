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
def generator_seq2(fd_dict):
    seq2 = list(fd_dict.items())
    seq2.append(("Sulla", "Mario"))
    return (x for x in seq2)

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

def test_bool_false(fd_empty):
    assert not fd_empty

def test_empty(fd_empty):
    assert fd_empty is frozendict({}) is frozendict([]) is frozendict({}, **{})

def test_constructor_kwargs(fd2, fd_dict_2):
    assert frozendict(**fd_dict_2) == fd2

def test_constructor_self(fd):
    assert fd == frozendict(fd, Sulla="Marco")
    assert fd is frozendict(fd)

def test_constructor_generator(fd, generator_seq2):
    assert fd == frozendict(generator_seq2, Sulla="Marco")

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

def test_copy(fd):
    fd2 = fd.copy()
    assert fd2 is fd

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
    assert frozendict(fd_items) == fd

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

    assert tuple(items) == tuple(fd.items())

################################################################################
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

################################################################################
# immutability tests

def test_init(fd):
    fd_copy = fd.copy()
    fd_clone = frozendict(dict(fd))
    fd.__init__({"Trump": "Donald"})
    assert fd_copy is fd
    assert fd_clone == fd

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

def test_vars(fd):
    with pytest.raises(TypeError):
        vars(fd)

def test_setattr(fd):
    with pytest.raises(AttributeError):
        fd._initialized = False

def test_delattr(fd):
    with pytest.raises(AttributeError):
        del fd._initialized
