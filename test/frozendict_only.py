import io
import pickle
from copy import copy, deepcopy

import pytest

from .base import FrozendictSubclass, FrozendictTestBase


class DictSubclass(dict):
    pass


class BadHash:
    def __hash__(self):
        raise MemoryError()


# noinspection PyMethodMayBeStatic
class FrozendictOnlyTest(FrozendictTestBase):
    def test_empty(self, fd_empty, dict_empty):
        fd_empty_set = self.FrozendictClass(dict_empty)
        fd_empty_list = self.FrozendictClass([])
        fd_empty_dict = self.FrozendictClass(dict_empty, **dict_empty)
        
        assert fd_empty is fd_empty_set is fd_empty_list
        assert fd_empty is fd_empty_dict

    def test_constructor_self_1(self, fd):
        assert fd is self.FrozendictClass(fd)

    def test_vars(self, fd):
        with pytest.raises(TypeError):
            vars(fd)

    def test_setattr(self, fd):
        with pytest.raises(AttributeError):
            fd._initialized = False

    def test_copy(self, fd):
        # noinspection PyTestUnpassedFixture
        assert fd.copy() is fd

    def test_copycopy(self, fd, fd_unhashable):
        assert copy(fd) is fd
        assert copy(fd_unhashable) is fd_unhashable

    def test_deepcopy(self, fd):
        assert deepcopy(fd) is fd
    
    def test_deepcopy_propagates_hash_error(self):
        fd = self.FrozendictClass({"Brignano": BadHash()})
        
        with pytest.raises(MemoryError):
            deepcopy(fd)
    
    def test_init(self, fd):
        # noinspection PyTestUnpassedFixture
        fd_copy = fd.copy()
        fd_clone = self.FrozendictClass(dict(fd))
        fd.__init__({"Trump": "Donald"})
        assert fd_copy is fd
        assert fd_clone == fd

    def test_del_empty(self):
        fd = self.FrozendictClass({1: 2})
        fd2 = fd.delete(1)
        assert fd2 is self.FrozendictClass()
        assert fd2 != fd

    def test_pickle_core(self, fd):
        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                assert module == 'frozendict'
                assert name == 'frozendict'
                return super().find_class('frozendict.core', name)

        dump = pickle.dumps(fd)
        assert dump
        assert CustomUnpickler(io.BytesIO(dump)).load() == fd

    def test_or_right_empty(self, fd, dict_empty):
        res = fd | dict_empty
        assert res is fd

    def test_or_left_empty(self, fd, fd_empty):
        res = fd_empty | fd
        assert res is fd

    def test_ior_dict_empty_right(self, fd, fd_dict, dict_empty):
        res = fd
        res |= dict_empty
        assert type(res) is type(fd)
        assert res == fd_dict
        assert res is fd

    def test_or_right_empty_subclass(self, fd):
        res = fd | DictSubclass()
        assert type(res) is type(fd)
        assert res == fd
        assert res is not fd

    def test_or_left_empty_subclass(self, fd_dict, fd_empty):
        other = FrozendictSubclass(fd_dict)
        res = fd_empty | other
        assert res == other
        assert res is not other
        assert type(res) is self.FrozendictClass

    def test_or_both_empty_subclass(self, fd_empty):
        assert fd_empty | DictSubclass() is fd_empty

    def test_repr(self, fd, fd_dict):
        classname = self.FrozendictClass.__name__
        modulename = self.FrozendictClass.__module__
        dict_repr = repr(fd_dict)
        assert repr(fd) == f"{modulename}.{classname}({dict_repr})"

    def test_str(self, fd, fd_dict):
        classname = self.FrozendictClass.__name__
        modulename = self.FrozendictClass.__module__
        assert str(fd) == f"{modulename}.{classname}({repr(fd_dict)})"

    def test_format(self, fd, fd_dict):
        classname = self.FrozendictClass.__name__
        modulename = self.FrozendictClass.__module__
        dict_repr = repr(fd_dict)
        assert format(fd) == f"{modulename}.{classname}({dict_repr})"
