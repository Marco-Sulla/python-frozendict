r"""
Provides frozendict, a simple immutable dictionary.
"""

from .core import *
from pathlib import Path

version_filename = "VERSION"

__all__ = core.__all__

curr_path = Path(__file__)
curr_dir = curr_path.parent
version_path = curr_dir / version_filename

with open(version_path) as f:
	__version__ = f.read()
