from frozendict.core import frozendict as frozendict_class
from .common import FrozendictCommonTest

c_ext = False
is_subclass = False

class TestFrozendictPyCommon(FrozendictCommonTest):
    _c_ext = c_ext
    _frozendict_class = frozendict_class
    _is_subclass = is_subclass
