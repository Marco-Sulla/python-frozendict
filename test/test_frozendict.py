from frozendict import frozendict
import pytest
import pickle

@pytest.fixture
def fd_dict():
	return {"Sulla": "Marco", "Hicks": "Bill", "frozen": frozendict({1: 2})}

@pytest.fixture
def fd(fd_dict):
	return frozendict(fd_dict)

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
	return "{}({})".format(frozendict.__name__, repr(fd_dict))

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

def test_copy_equals(fd):
	fd2 = fd.copy()
	assert fd2 == fd

def test_copy_not_identical(fd):
	fd2 = fd.copy()
	assert fd2 is not fd

def test_not_equal(fd, fd_giulia):
	assert fd != fd_giulia

def test_equals_dict(fd, fd_dict):
	assert fd == fd_dict

def test_hash(fd):
	assert hash(fd)

def test_pickle(fd):
	fd_unpickled = pickle.loads(pickle.dumps(fd))
	assert fd_unpickled == fd

def test_empty(fd_empty):
	assert fd_empty == frozendict({})

def test_constructor_self(fd):
	assert fd == frozendict(fd)

def test_constructor_self_not_identical(fd):
	assert fd is not frozendict(fd)

def test_constructor_kwargs(fd, fd_dict):
	assert frozendict(**fd_dict) == fd

def test_constructor_iterator(fd, fd_items):
	assert frozendict(fd_items) == fd

def test_unhashable_value():
    with pytest.raises(TypeError):
        frozendict({1: []})

def test_todict(fd, fd_dict):
	assert dict(fd) == fd_dict

def test_get(fd):
	assert fd.get("Sulla") == "Marco"

def test_get_fail(fd):
	default = "?"
	assert fd.get("God", default) == default

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
	assert not vars(fd)

def test_initialized(fd):
	assert fd._initialized

def test_setattr(fd):
    with pytest.raises(NotImplementedError):
        fd._initialized = False

def test_delattr(fd):
    with pytest.raises(NotImplementedError):
        del fd._initialized

def test_delvar(fd):
    del fd

    with pytest.raises(NameError):
        fd