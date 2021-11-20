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
    fd2 = fd.copy()
    assert fd2 is fd

def test_init(fd):
    fd_copy = fd.copy()
    fd_clone = frozendict_class(dict(fd))
    fd.__init__({"Trump": "Donald"})
    assert fd_copy is fd
    assert fd_clone == fd
