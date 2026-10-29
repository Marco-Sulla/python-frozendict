import sys


def immutable(self, *_args, **_kwargs):
    r"""
    Function for not implemented method since the object is immutable
    """
    
    raise AttributeError(f"'{self.__class__.__name__}' object is read-only")


_empty_frozendict = None
_module_name = "frozendict"


def _to_seq():
    return list if sys.version_info >= (3, 14) else tuple


# noinspection PyPep8Naming
class frozendict(dict):
    r"""
    A simple immutable dictionary.

    The API is the same as `dict`, without methods that can change the
    immutability. In addition, it supports __hash__() and other handy methods.
    """
    
    __slots__ = ("_hash",)
    
    @classmethod
    def fromkeys(cls, *args, **kwargs):
        r"""
        Identical to dict.fromkeys().
        """
        
        return cls(dict.fromkeys(*args, **kwargs))
    
    # noinspection PyMethodParameters
    def __new__(e4b37cdf_d78a_4632_bade_6f0579d8efac, *args, **kwargs):
        cls = e4b37cdf_d78a_4632_bade_6f0579d8efac
        
        # check if there's only an argument and it's of the same class
        if len(args) == 1 and not kwargs:
            it = args[0]
            
            # no isinstance, to avoid subclassing problems
            if it.__class__ is frozendict and cls is frozendict:
                return it
        
        # noinspection PyTypeChecker
        self = dict.__new__(cls, *args, **kwargs)
        dict.__init__(self, *args, **kwargs)
        
        # empty singleton - start

        if not self and self.__class__ is frozendict:
            global _empty_frozendict
            
            if _empty_frozendict is None:
                _empty_frozendict = self
            else:
                return _empty_frozendict
        
        # empty singleton - end
        
        object.__setattr__(self, "_hash", -1)
        
        return self

    def _clone(self, *args, **kwargs):
        r"""
        Creates a new instance of the same object, without the fast path optimization and singleton
        """

        new_self = dict.__new__(self.__class__, *args, **kwargs)
        dict.__init__(new_self, self, **kwargs)
        object.__setattr__(new_self, "_hash", -1)
        return new_self

    # noinspection PyMissingConstructor
    def __init__(self, *args, **kwargs):
        pass
    
    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise
        raises a TypeError.
        """
        
        if self._hash != -1:
            return self._hash
        
        fs = frozenset(self.items())
        _hash = hash(fs)
        object.__setattr__(self, "_hash", _hash)
        
        return _hash
    
    def __repr__(self, *args, **kwargs):
        r"""
        Identical to dict.__repr__().
        """
        
        body = dict.__repr__(self)

        if self.__class__ is frozendict:
            name = f"{_module_name}.{frozendict.__name__}"
        else:
            name = self.__class__.__name__

        return f"{name}({body})"
    
    def copy(self):
        r"""
        Return the object itself, as it's an immutable.
        """

        if self.__class__ is frozendict:
            return self

        return self.__class__(self)

    def __copy__(self, *args, **kwargs):
        r"""
        See copy().
        """
        
        return self.copy()
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self),))
    
    def set(self, key, val):
        new_self = self._clone()
        dict.__setitem__(new_self, key, val)
        
        return new_self
    
    def setdefault(self, key, default = None):
        if key in self:
            return self

        new_self = self._clone()
        dict.__setitem__(new_self, key, default)
        
        return new_self
    
    def delete(self, key):
        new_self = self._clone()
        dict.__delitem__(new_self, key)
        
        if new_self:
            return new_self
        
        return self.__class__()
    
    def _get_by_index(self, collection, index):
        try:
            return collection[index]
        except IndexError:
            maxindex = len(collection) - 1
            name = self.__class__.__name__
            raise IndexError(f"{name} index {index} out of range {maxindex}") from None

    def key(self, index = 0):
        collection = _to_seq()(self.keys())
        
        return self._get_by_index(collection, index)
    
    def value(self, index = 0):
        collection = _to_seq()(self.values())
        
        return self._get_by_index(collection, index)
    
    def item(self, index = 0):
        collection = _to_seq()(self.items())
        
        return self._get_by_index(collection, index)
    
    def __setitem__(self, key, val, *args, **kwargs):
        raise TypeError(f"'{self.__class__.__name__}' object doesn't support item assignment")
    
    def __delitem__(self, key, *args, **kwargs):
        raise TypeError(f"'{self.__class__.__name__}' object doesn't support item deletion")


def frozendict_or(self, other, *_args, **_kwargs):
    if not isinstance(other, dict):
        return NotImplemented

    klass = self.__class__

    if klass is frozendict:
        klass_other = other.__class__

        if not other and (klass_other is dict or klass_other is frozendict):
            return self

        if not self and klass_other is frozendict:
            return other

    new_self = self._clone()
    dict.update(new_self, other)

    if klass is frozendict and not new_self:
        return self

    return new_self


frozendict.__or__ = frozendict_or
frozendict.__ior__ = frozendict_or

if getattr(dict, '__or__', None) is None:  # pragma: no cover
    def frozendict_ror(self, other, *_args, **_kwargs):
        if not isinstance(other, dict):
            return NotImplemented

        return {**other, **self}


    frozendict.__ror__ = frozendict_ror

try:
    # noinspection PyStatementEffect
    frozendict.__reversed__
except AttributeError:  # pragma: no cover
    def frozendict_reversed(self, *_args, **_kwargs):
        return reversed(tuple(self))
    
    
    frozendict.__reversed__ = frozendict_reversed

frozendict.clear = immutable
frozendict.pop = immutable
frozendict.popitem = immutable
frozendict.update = immutable
frozendict.__delattr__ = immutable
frozendict.__setattr__ = immutable
frozendict.__module__ = _module_name

__all__ = (frozendict.__name__,)
