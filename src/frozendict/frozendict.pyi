try:
    from ._frozendict import *
except ImportError:
    from .core import *

FrozenOrderedDict = frozendict
