from frozendict.core import frozendict as frozendict_py_class
from .common import FrozendictCommonTest
from .frozendict_only import FrozendictOnlyTest
import frozendict as cool
from frozendict import frozendict as frozendict_class

is_subclass = False

# class TestPyFrozendict(FrozendictCommonTest, FrozendictOnlyTest):
#     frozendict_class = frozendict_py_class
#     c_ext = False
#     is_subclass = is_subclass

print("SSSSSSSSSSSSSSSSSSSSS", cool.c_ext, cool)

if cool.c_ext:
    class TestCFrozendict(FrozendictCommonTest, FrozendictOnlyTest):
        frozendict_class = frozendict_class
        c_ext = cool.c_ext
        is_subclass = is_subclass
