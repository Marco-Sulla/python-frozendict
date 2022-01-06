subclass = True

def test_empty_sub(fd_empty):
    assert fd_empty == frozendict_class({}) == frozendict_class([]) == frozendict_class({}, **{})

def test_constructor_self_sub(fd):
    assert fd == frozendict_class(fd)

def test_copy_sub(fd):
    fd2 = fd.copy()
    assert fd2 == fd

def test_init_sub(fd):
    fd_copy = fd.copy()
    fd_clone = frozendict_class(dict(fd))
    fd.__init__({"Trump": "Donald"})
    assert fd_copy == fd
    assert fd_clone == fd

def test_missing(fd):
    fd_missing = FMissing(fd)
    assert fd_missing[0] == 0
