from frozendict.core import frozendict as frozendict_class
from .common import FrozendictCommonTest

c_ext = False
is_subclass = False

class TestFrozendictPyCommon(FrozendictCommonTest):
    frozendict_class = frozendict_class
    c_ext = c_ext
    is_subclass = is_subclass
