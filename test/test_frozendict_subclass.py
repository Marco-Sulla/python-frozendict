from frozendict.core import frozendict as FrozendictPyClass
from .common import FrozendictCommonTest
from .subclass_only import FrozendictSubclassOnlyTest
import frozendict as cool
from frozendict import frozendict as FrozendictClass


is_subclass = True


class FrozendictPySubclass(FrozendictPyClass):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)


class FrozendictPyMissingSubclass(FrozendictPyClass):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)
    
    def __missing__(self, key):
        return key


class TestFrozendictPySubclass(
        FrozendictCommonTest, 
        FrozendictSubclassOnlyTest
):
    FrozendictClass = FrozendictPySubclass
    FrozendictMissingClass = FrozendictPyMissingSubclass
    c_ext = False
    is_subclass = is_subclass


if cool.c_ext:
    class FrozendictSubclass(FrozendictClass):
        def __new__(cls, *args, **kwargs):
                return super().__new__(cls, *args, **kwargs)


    class FrozendictMissingSubclass(FrozendictClass):
        def __new__(cls, *args, **kwargs):
                return super().__new__(cls, *args, **kwargs)
        
        def __missing__(self, key):
            return key
    
    
    class TestFrozendictSubclass(
            FrozendictCommonTest, 
            FrozendictSubclassOnlyTest
    ):
        FrozendictClass = FrozendictSubclass
        FrozendictMissingClass = FrozendictMissingSubclass
        c_ext = cool.c_ext
        is_subclass = is_subclass
