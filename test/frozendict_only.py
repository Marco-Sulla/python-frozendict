import pytest
from copy import copy, deepcopy
from .base import FrozendictTestBase

class FrozendictOnlyTest(FrozendictTestBase):
    def test_empty(self, fd_empty):
        assert fd_empty is self.frozendict_class({}) is self.frozendict_class([]) is self.frozendict_class({}, **{})

    def test_constructor_self_1(self, fd):
        assert fd is self.frozendict_class(fd)

    def test_vars(self, fd):
        with pytest.raises(TypeError):
            vars(fd)

    def test_setattr(self, fd):
        with pytest.raises(AttributeError):
            fd._initialized = False

    def test_copy(self, fd):
        assert fd.copy() is fd

    def test_copycopy(self, fd, fd_unhashable):
        assert copy(fd) is fd
        assert copy(fd_unhashable) is fd_unhashable

    def test_deepcopy(self, fd):
        assert deepcopy(fd) is fd

    def test_init(self, fd):
        fd_copy = fd.copy()
        fd_clone = self.frozendict_class(dict(fd))
        fd.__init__({"Trump": "Donald"})
        assert fd_copy is fd
        assert fd_clone == fd

    def test_del_empty(self):
        fd = self.frozendict_class({1: 2})
        assert fd.delete(1) is self.frozendict_class()
