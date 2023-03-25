from types import MappingProxyType
from collections import OrderedDict
from array import array
from frozendict import frozendict


def isIterableNotString(o):
    from collections import abc
    
    return (
        isinstance(o, abc.Iterable) and 
        not isinstance(o, memoryview) and 
        not hasattr(o, "isalpha")
    )


def getItems(o):
    from collections import abc
    
    if not isinstance(o, abc.Iterable):
        raise TypeError("object must be an iterable")
    
    if isinstance(o, abc.Mapping):
        return dict.items
    
    return enumerate


_freeze_conversion_map = frozendict({
    dict: frozendict, 
    OrderedDict: frozendict, 
    list: tuple, 
    array: tuple, 
    set: frozenset, 
    bytearray: bytes, 
})

_freeze_conversion_map_custom = {}


class FreezeError(Exception):  pass


def register(to_convert, converter, *, inverse = False, force = False):
    r"""
    Adds a `converter` for a type `to_convert`. `to_convert` and `converter`
    must be callable. The new converter will be used by deepfreeze(). 
    
    If `to_covert` has already a converter and `force` is False, a
    `FreezeError` is raised.
    
    If `inverse` is True, the conversion is considered from an immutable 
    type to a mutable one. This is useful for temporarily convert an 
    immutable object to a mutable o_tmp, convert all its values to 
    immutable types, assign them to o_tmp and then convert back o_tmp into 
    its immutable counterpart.
    """
    
    try:
        to_convert.__call__
    except AttributeError:
        raise ValueError("`to_convert` parameter must be a callable")
    
    try:
        converter.__call__
    except AttributeError:
        raise ValueError("`converter` parameter must be a callable")
    
    if inverse:
        freeze_conversion_map = getFreezeConversionInverseMap()
    else:
        freeze_conversion_map = getFreezeConversionMap()
    
    if not force and to_convert in freeze_conversion_map:
        raise FreezeError(
            f"{to_convert.__name__} is already in the conversion map, " + 
            "and `force` is False"
        )
    
    if inverse:
        freeze_conversion_map = _freeze_conversion_inverse_map_custom
    else:
        freeze_conversion_map = _freeze_conversion_map_custom
    
    freeze_conversion_map[to_convert] = converter


def getFreezeConversionMap():
    return _freeze_conversion_map | _freeze_conversion_map_custom


_freeze_conversion_inverse_map = frozendict({
    frozendict: dict, 
    MappingProxyType: dict, 
    tuple: list, 
})

_freeze_conversion_inverse_map_custom = {}


def getFreezeConversionInverseMap():
    return _freeze_conversion_inverse_map | _freeze_conversion_inverse_map_custom


_freeze_unhashable_types = (MappingProxyType, )
_freeze_unhashable_types_custom = []


def getFreezeUnhashableTypes():
    return _freeze_unhashable_types + tuple(_freeze_unhashable_types_custom)


_freeze_types = (
    frozenset({x for x in _freeze_conversion_map if isinstance(x, type)}) |
    {x for x in _freeze_conversion_inverse_map if isinstance(x, type)}
)


def getFreezeTypes():
    return (
        _freeze_types | 
        {x for x in _freeze_conversion_map_custom if isinstance(x, type)} | 
        {x for x in _freeze_conversion_inverse_map_custom if isinstance(x, type)}
    )

_freeze_types_plain = (set, bytearray, array)


def deepfreeze(o):
    fr"""
    Converts the object and all the objects nested in it in its immutable
    counterparts.
    The conversion map is in {getFreezeConversionMap.__name__}
    """
    
    try:
        hash(o)
        return o
    except TypeError:
        pass
    
    type_o = type(o)
    
    freeze_types = getFreezeTypes()
    
    if type_o not in freeze_types:
        supported_types = ", ".join((x.__name__ for x in freeze_types))
        err = f"type {type_o} is not hashable or is not one of the supported types: {supported_types}"
        raise TypeError(err)
    
    freeze_conversion_map = getFreezeConversionMap()
    
    if type_o in _freeze_types_plain:
        return freeze_conversion_map[type_o](o)
    
    if not isIterableNotString(o):
        return freeze_conversion_map[type_o](o)
    
    freeze_conversion_inverse_map = getFreezeConversionInverseMap()
    
    frozen_type = type_o in freeze_conversion_inverse_map
    
    if frozen_type:
        o = freeze_conversion_inverse_map[type_o](o)
    
    from copy import copy
    
    o_copy = copy(o)
    
    for k, v in getItems(o)(o_copy):
        o[k] = deepfreeze(v)
    
    if frozen_type: #and not type_o in getFreezeUnhashableTypes():
        return type_o(o)
    
    return freeze_conversion_map[type(o)](o)


__all__ = (
    deepfreeze.__name__, 
    register.__name__, 
    getFreezeConversionMap.__name__
)

del MappingProxyType
del OrderedDict
del array
del frozendict
