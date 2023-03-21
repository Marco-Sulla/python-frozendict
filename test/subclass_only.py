subclass = True

def test_empty_sub(fd_empty):
    fd_empty_2 = frozendict_class({})
    fd_empty_3 = frozendict_class([])
    fd_empty_4 = frozendict_class({}, **{})
    assert fd_empty == fd_empty_2 == fd_empty_3 == fd_empty_4
    assert fd_empty is not fd_empty_2 is not fd_empty_3 is not fd_empty_4

def test_constructor_self_sub(fd):
    fd_clone = frozendict_class(fd)
    assert fd == fd_clone
    assert fd is not fd_clone

def test_copy_sub(fd):
    fd_copy = fd.copy()
    assert fd_copy == fd
    assert fd_copy is not fd

def test_copycopy_sub(fd, fd_unhashable):
    fd_copy = copy(fd)
    fd_copy_unhashable = copy(fd_unhashable)
    assert fd_copy == fd
    assert fd_copy_unhashable == fd_unhashable
    assert fd_copy is not fd
    assert fd_copy_unhashable is not fd_unhashable

def test_deepcopy_sub(fd):
    fd_copy = deepcopy(fd)
    assert fd_copy == fd
    assert fd_copy is not fd

def test_init_sub(fd):
    fd_copy = fd.copy()
    fd_clone = frozendict_class(dict(fd))
    fd.__init__({"Trump": "Donald"})
    assert fd_copy == fd
    assert fd_clone == fd
    assert fd_copy is not fd

def test_del_empty_sub():
    fd = frozendict_class({1: 2})
    fd2 = fd.delete(1)
    fd_empty = frozendict_class()
    assert fd2 == fd_empty
    assert fd2 is not fd_empty

def test_missing(fd):
    fd_missing = FMissing(fd)
    assert fd_missing[0] == 0
