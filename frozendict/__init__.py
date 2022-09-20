r"""
Provides frozendict, a simple immutable dictionary.
"""
try:
    from ._frozendict import *
    c_ext = True
except ImportError:
    from .core import *
    c_ext = False

from .version import version as __version__
import collections.abc as _abc

if not c_ext:
    @classmethod
    def _my_subclasshook(klass, subclass):
        if issubclass(subclass, frozendict):
            return False
        
        return NotImplemented
    
    _abc.MutableMapping.__subclasshook__ = _my_subclasshook

_abc.Mapping.register(frozendict)

from pathlib import Path

curr_path = Path(__file__)
curr_dir = curr_path.parent

if c_ext:
    __all__ = ("frozendict", "__version__", )
else:
    __all__ = core.__all__ + ("__version__", )

# TODO deprecated, to remove in future versions
FrozenOrderedDict = frozendict
__all__ += ("FrozenOrderedDict", )

del Path
del curr_path
del curr_dir
del _abc

if not c_ext:
    del core
