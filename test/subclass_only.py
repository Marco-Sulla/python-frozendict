import gc

import pytest
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
