r"""
Provides frozendict, a simple immutable dictionary.
"""

from .core import *
from .core import frozendict as f
from .core import notimplemented
from pathlib import Path

f.empty = f()
f.clear = notimplemented
f.pop = notimplemented
f.popitem = notimplemented
f.setdefault = notimplemented
f.update = notimplemented
f.__delitem__ = notimplemented
f.__setitem__ = notimplemented
f.__delattr__ = notimplemented
f.__setattr__ = notimplemented

version_filename = "VERSION"

curr_path = Path(__file__)
curr_dir = curr_path.parent
version_path = curr_dir / version_filename

with open(version_path) as f:
    __version__ = f.read()

__all__ = core.__all__ + ("__version__", )
