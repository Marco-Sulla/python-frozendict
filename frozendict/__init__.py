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
    __all__ = (frozendict.__name__, "__version__", )
else:
    __all__ = core.__all__ + ("__version__", )

# TODO deprecated, to remove in future versions
FrozenOrderedDict = frozendict
__all__ += (FrozenOrderedDict.__name__, )

del Path
del version_filename
del curr_path
del curr_dir
del version_path
del f

if not c_ext:
    del core

# util

from copy import copy as _copy
from types import MappingProxyType as _MappingProxyType
from collections import OrderedDict as _OrderedDict
from array import array as _array


def isIterableNotString(o):
    return (
        isinstance(o, _abc.Iterable) and 
        not isinstance(o, memoryview) and 
        not hasattr(o, "isalpha")
    )

def getItems(o):
    if not isinstance(o, _abc.Iterable):
        raise TypeError("object must be an iterable")
    
    if isinstance(o, _abc.Mapping):
        return dict.items
    
    return enumerate

_deepfreeze_conversion_map = frozendict({
    dict: frozendict, 
    _OrderedDict: frozendict, 
    list: tuple, 
    _array: tuple, 
    set: frozenset, 
    bytearray: bytes, 
})

_deepfreeze_conversion_map_custom = {}

def getDeepfreezeConversionMap():
    return _deepfreeze_conversion_map | _deepfreeze_conversion_map_custom

_deepfreeze_conversion_inverse_map = frozendict({
    frozendict: dict, 
    _MappingProxyType: dict, 
    tuple: list, 
})

_deepfreeze_conversion_inverse_map_custom = {}

def getDeepfreezeConversionInverseMap():
    return _deepfreeze_conversion_inverse_map | _deepfreeze_conversion_inverse_map_custom

_deepfreeze_unhashable_types = (_MappingProxyType, )
_deepfreeze_unhashable_types_custom = []

def getDeepfreezeUnhashableTypes():
    return _deepfreeze_unhashable_types + _deepfreeze_unhashable_types_custom

_deepfreeze_types = (
    frozenset({x for x in _deepfreeze_conversion_map if isinstance(x, type)}) |
    {x for x in _deepfreeze_conversion_inverse_map if isinstance(x, type)}
)

def getDeepfreezeTypes():
    return (
        _deepfreeze_types | 
        {x for x in _deepfreeze_conversion_map_custom if isinstance(x, type)} | 
        {x for x in _deepfreeze_conversion_inverse_map_custom if isinstance(x, type)}
    )

_deepfreeze_types_plain = (set, bytearray, _array)

def deepfreeze(o):
    try:
        hash(o)
        return o
    except TypeError:
        pass
    
    type_o = type(o)
    
    deepfreeze_types = getDeepfreezeTypes()
    
    if type_o not in deepfreeze_types:
        supported_types = ", ".join((x.__name__ for x in deepfreeze_types))
        err = f"type {type_o} is not hashable or is not one of the supported types: {supported_types}"
        raise TypeError(err)
    
    deepfreeze_conversion_map = getDeepfreezeConversionMap()
    
    if type_o in _deepfreeze_types_plain:
        return deepfreeze_conversion_map[type_o](o)
    
    if not isIterableNotString(o):
        return deepfreeze_conversion_map[type_o](o)
    
    deepfreeze_conversion_inverse_map = getDeepfreezeConversionInverseMap()
    
    frozen_type = type_o in deepfreeze_conversion_inverse_map
    
    if frozen_type:
        o = deepfreeze_conversion_inverse_map[type_o](o)
    
    o_copy = _copy(o)
    
    for k, v in getItems(o)(o_copy):
        o[k] = deepfreeze(v)
    
    if frozen_type and not type_o in getDeepfreezeUnhashableTypes():
        return type_o(o)
    
    return deepfreeze_conversion_map[type(o)](o)

__all__ += (deepfreeze.__name__, )
