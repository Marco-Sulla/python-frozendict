import io
import pickle

import pytest

from .base import FrozendictTestBase


# noinspection PyMethodMayBeStatic
class FrozendictOnlyTest(FrozendictTestBase):
    def test_vars(self, fd):
        with pytest.raises(TypeError):
            vars(fd)

    def test_setattr(self, fd):
        with pytest.raises(AttributeError):
            fd._initialized = False

    def test_pickle_core(self, fd):
        class CustomUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                assert module == 'frozendict'
                assert name == 'frozendict'
                return super().find_class('frozendict.core', name)

        dump = pickle.dumps(fd)
        assert dump
        assert CustomUnpickler(io.BytesIO(dump)).load() == fd
