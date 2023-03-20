from frozendict.core import frozendict as frozendict_class
from .common import FrozendictCommonTest

c_ext = False


class TestFrozendictPyCommon(FrozendictCommonTest):
    _c_ext = c_ext
    _frozendict_class = frozendict_class
    _subclass = False
