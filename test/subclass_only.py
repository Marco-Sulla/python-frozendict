import gc
from copy import copy, deepcopy

import pytest
from frozendict import frozendict
from .base import FrozendictTestBase


class EvilKeys:
    def __init__(self, real_keys):
        self._it = iter(real_keys)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        gc.collect()
        return next(self._it)


class EvilMapping:
    def __init__(self, d):
        self._d = d
    
    def keys(self):
        return EvilKeys(list(self._d.keys()))
    
    def __getitem__(self, key):
        return self._d[key]


# noinspection PyMethodMayBeStatic
class FrozendictSubclassOnlyTest(FrozendictTestBase):
    _FrozendictMissingClass = None
    
    @property
    def FrozendictMissingClass(self):
        val = self._FrozendictMissingClass
        
        if val is None:
            raise ValueError("FrozendictMissingClass is None")
        
        return val
    
    @FrozendictMissingClass.setter
    def FrozendictMissingClass(self, val):
        self._FrozendictMissingClass = val
    
    ####################################################################
    # tests
    
    def test_empty_sub(self, fd_empty):
        fd_empty_2 = self.FrozendictClass({})
        fd_empty_3 = self.FrozendictClass([])
        fd_empty_4 = self.FrozendictClass({}, **{})
        
        assert fd_empty == fd_empty_2 == fd_empty_3 == fd_empty_4
        assert fd_empty is not fd_empty_2 is not fd_empty_3
        assert fd_empty is not fd_empty_4
    
    def test_constructor_self_sub(self, fd):
        fd_clone = self.FrozendictClass(fd)
        assert fd == fd_clone
        assert fd is not fd_clone

    def test_copy_sub(self, fd):
        # noinspection PyTestUnpassedFixture
        fd_copy = fd.copy()
        assert fd_copy == fd
        assert fd_copy is not fd

    def test_copycopy_sub(self, fd, fd_unhashable):
        fd_copy = copy(fd)
        fd_copy_unhashable = copy(fd_unhashable)
        assert fd_copy == fd
        assert fd_copy_unhashable == fd_unhashable
        assert fd_copy is not fd
        assert fd_copy_unhashable is not fd_unhashable

    def test_deepcopy_sub(self, fd):
        fd_copy = deepcopy(fd)
        assert fd_copy == fd
        assert fd_copy is not fd
        
        # test deepcopy afer caching at C level
        deepcopy(fd)

    def test_init_sub(self, fd):
        # noinspection PyTestUnpassedFixture
        fd_copy = fd.copy()
        fd_clone = self.FrozendictClass(dict(fd))
        fd.__init__({"Trump": "Donald"})
        assert fd_copy == fd
        assert fd_clone == fd
        assert fd_copy is not fd

    def test_del_empty_sub(self, fd_empty):
        f = self.FrozendictClass({1: 2})
        f2 = f.delete(1)
        assert f2 == fd_empty
        assert f2 is not fd_empty

    def test_missing(self, fd):
        fd_missing = self.FrozendictMissingClass(fd)
        assert fd_missing[0] == 0
    
    def test_subclass_construction_survives_gc_mid_init(self, fd_dict):
        # regression test: constructing a frozendict subclass from a mapping whose .keys()
        # triggers a GC pass mid-construction used to segfault: dict_traverse dereferenced ma_keys
        # while it was still NULL.
        
        if not self.c_ext:
            pytest.skip("only the C extension had this bug")
        
        assert self.FrozendictClass(EvilMapping(fd_dict)) == fd_dict

    def test_or_right_empty_sub(self, fd):
        res = fd | {}
        assert res == fd
        assert res is not fd
        assert type(res) is type(fd)

    def test_or_left_empty_sub(self, fd, fd_empty):
        res = fd_empty | fd
        assert res == fd
        assert res is not fd
        assert type(res) is type(fd_empty)

    def test_or_left_empty_exact(self, fd_dict, fd_empty):
        other = frozendict(fd_dict)
        res = fd_empty | other
        assert res == other
        assert res is not other
        assert type(res) is type(fd_empty)
