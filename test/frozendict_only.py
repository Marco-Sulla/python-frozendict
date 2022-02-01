def test_empty(fd_empty):
    assert fd_empty is frozendict_class({}) is frozendict_class([]) is frozendict_class({}, **{})

def test_constructor_self_1(fd):
    assert fd is frozendict_class(fd)

def test_vars(fd):
    with pytest.raises(TypeError):
        vars(fd)

def test_setattr(fd):
    with pytest.raises(AttributeError):
        fd._initialized = False

def test_copy(fd):
    assert fd.copy() is fd

def test_copycopy(fd, fd_unhashable):
    assert copy(fd) is fd
    assert copy(fd_unhashable) is fd_unhashable

def test_deepcopy(fd):
    assert deepcopy(fd) is fd

def test_init(fd):
    fd_copy = fd.copy()
    fd_clone = frozendict_class(dict(fd))
    fd.__init__({"Trump": "Donald"})
    assert fd_copy is fd
    assert fd_clone == fd

def test_del_empty():
    fd = frozendict_class({1: 2})
    assert fd.delete(1) is frozendict_class()
