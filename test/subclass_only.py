def test_empty(fd_empty):
    assert fd_empty == frozendict_class({}) == frozendict_class([]) == frozendict_class({}, **{})

def test_constructor_self(fd):
    assert fd == frozendict_class(fd)
