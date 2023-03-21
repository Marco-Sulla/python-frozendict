from frozendict.core import frozendict as FrozendictPyClass
from .common import FrozendictCommonTest
from .frozendict_only import FrozendictOnlyTest
import frozendict as cool
from frozendict import frozendict as FrozendictClass


is_subclass = False


class TestPyFrozendict(FrozendictCommonTest, FrozendictOnlyTest):
    FrozendictClass = FrozendictPyClass
    c_ext = False
    is_subclass = is_subclass

if cool.c_ext:
    class TestCFrozendict(FrozendictCommonTest, FrozendictOnlyTest):
        FrozendictClass = FrozendictClass
        c_ext = cool.c_ext
        is_subclass = is_subclass
