r"""
Provides frozendict, a simple immutable dictionary.
"""
try:
    from ._frozendict import *
    c_ext = True
except ImportError:
    from .core import *
    c_ext = False

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

version_filename = "VERSION"

curr_path = Path(__file__)
curr_dir = curr_path.parent
version_path = curr_dir / version_filename

with open(version_path) as f:
    __version__ = f.read()

if c_ext:
    __all__ = ("frozendict", "__version__", )
else:
    __all__ = core.__all__ + ("__version__", )

# TODO deprecated, to remove in future versions
FrozenOrderedDict = frozendict
__all__ += ("FrozenOrderedDict", )

del Path
del version_filename
del curr_path
del curr_dir
del version_path
del f
del _abc

if not c_ext:
    del core
