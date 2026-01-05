import frozendict as cool
from frozendict import frozendict as FrozendictClass

from .common import FrozendictCommonTest
from .frozendict_only import FrozendictOnlyTest

is_subclass = False


class TestFrozendict(FrozendictCommonTest, FrozendictOnlyTest):
    FrozendictClass = FrozendictClass
    c_ext = cool.c_ext
    is_subclass = is_subclass
