from collections.abc import Mapping
from types import MappingProxyType
import copy

_unashable_err_tpl = "unhashable {klass}"
_undeletable_err_tpl = "'{klass}' object does not support attribute deletion"
_unsettable_err_tpl = "'{klass}' object does not support attribute setting"
_add_err_tpl = "unsupported operand type(s) for +: '{klass1}' and '{klass2}'"
_sub_err_tpl = "unsupported operand type(s) for -: '{klass1}' and '{klass2}'"
_reinit_err_msg = "you can't reinitialize the object"

class frozendict(Mapping):
    """
    A simple immutable dictionary.

    The API is the same as `dict`, without methods that can change the 
    immutability.
    In addition, it supports the __add__ and __sub__ operands.
    """
    
    @classmethod
    def fromkeys(cls, seq, value=None, *args, **kwargs):
        return cls(dict.fromkeys(seq, value, *args, **kwargs))
    
    __inizialized = False
    _dict_name = "_dict"
    
    def __init__(self, *args, **kwargs):
        """
        Identical to dict.__init__(). It can't be reinvoked
        """

        if self.__inizialized:
            raise NotImplementedError(_reinit_err_msg)
        else:
            tmp_dict = dict(*args, **kwargs)
            self._dict = MappingProxyType(tmp_dict)
            
            self._repr = "{klass}({body})".format(
                klass = type(self).__name__, 
                body = tmp_dict
            )
            
            self._hash = None
            hashable = True
            
            for v in tmp_dict.values():
                try:
                    hash(v)
                except Exception:
                    hashable = False
                    break
            
            if hashable:
                self._hash = hash(frozenset(tmp_dict.items()))
        
            self.__inizialized = True
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def copy(self):
        return self.__class__(self)
    
    def __copy__(self, *args, **kwargs):
        return self.copy()
    
    def __deepcopy__(self, *args, **kwargs):
        tmp = dict(self._dict)
        return self.__class__(copy.deepcopy(tmp))

    def __iter__(self):
        return iter(self._dict)
    
    def __len__(self):
        return len(self._dict)
    
    def __repr__(self):
        return self._repr
    
    def __hash__(self):
        """
        Hash will be calculated if all the values are immutable, otherwise
        TypeError is raised.
        """

        if self._hash is None:
            raise TypeError(
                _unashable_err_tpl.format(klass=type(self).__name__)
            )
        
        return self._hash
    
    def __add__(self, other):
        """
        If you add a dict-like object, a new frozendict will be returned, equal 
        to the old frozendict updated with the other object.
        """

        tmp = dict(self)

        try:
            tmp.update(other)
        except Exception:
            raise TypeError(_add_err_tpl.format(
                klass1 = type(self).__name__, 
                klass2 = type(other).__name__
            ))
        
        return self.__class__(tmp)

    def __sub__(self, iterable):
        """
        You can subtract an iterable from a frozendict. A new frozendict
        will be returned, without the keys that are in the iterable.
        """
        
        tmp = dict(self)

        try:
            iter(iterable)

            if isinstance(iterable, (str, bytes, bytearray)):
                raise TypeError()
        except Exception:
            raise TypeError(_sub_err_tpl.format(
                klass1 = type(self).__name__, 
                klass2 = type(iterable).__name__
            ))

        for x in iterable:
            try:
                del tmp[x]
            except KeyError:
                pass


        return self.__class__(tmp)

    def __getstate__(self):
        orig = vars(self)
        key = self._dict_name
        tmp = dict(orig)
        tmp[key] = dict(orig[key])

        return tmp

    def __setstate__(self, state):
        orig = vars(self)
        orig.update(state)
        key = self._dict_name
        orig[key] = MappingProxyType(state[key])

    def __setattr__(self, *args, **kwargs):
        if self.__inizialized:
            raise NotImplementedError(
                _unsettable_err_tpl.format(klass=type(self).__name__)
            )
        else:
            super().__setattr__(*args, **kwargs)
        
    def __delattr__(self, *args, **kwargs):
        raise NotImplementedError(
            _undeletable_err_tpl.format(klass=type(self).__name__)
        )

__all__ = (frozendict.__name__, )
