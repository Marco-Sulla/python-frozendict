from copy import deepcopy


def _immutable(self, *args, **kwargs):
    r"""
    Function for not implemented method since the object is immutable
    """
    
    raise AttributeError(f"'{self.__class__.__name__}' object is read-only")


class frozendict(dict):
    r"""
    A simple immutable dictionary.
    
    The API is the same as `dict`, without methods that can change the 
    immutability. In addition, it supports __hash__().
    """
    
    __slots__ = (
        "_hash", 
    )
    
    @classmethod
    def fromkeys(cls, *args, **kwargs):
        r"""
        Identical to dict.fromkeys().
        """
        
        return cls(dict.fromkeys(*args, **kwargs))
    
    def __new__(e4b37cdf_d78a_4632_bade_6f0579d8efac, *args, **kwargs):
        r"""
        Almost identical to dict.__new__().
        """
        
        cls = e4b37cdf_d78a_4632_bade_6f0579d8efac


        has_kwargs = bool(kwargs)
        continue_creation = True
        
        # check if there's only an argument and it's of the same class
        if len(args) == 1 and not has_kwargs:
            it = args[0]
            
            # no isinstance, to avoid subclassing problems
            if it.__class__ == frozendict and cls == frozendict:
                self = it
                continue_creation = False
        
        if continue_creation:
            self = dict.__new__(cls, *args, **kwargs)
            
            dict.__init__(self, *args, **kwargs)
            
            # empty singleton - start
            
            if self.__class__ == frozendict and not len(self):
                try:
                    self = cls.empty
                    continue_creation = False
                except AttributeError:
                    cls.empty = self
            
            # empty singleton - end
            
            if continue_creation:
                object.__setattr__(self, "_hash", None)
        
        return self
    
    def __init__(self, *args, **kwargs):
        pass
    
    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise raises a 
        TypeError.
        """
        
        if self._hash != None:
            _hash = self._hash
        else:
            try:
                fs = frozenset(self.items())
            except TypeError:
                _hash = -1
            else:
                _hash = hash(fs)
            
            object.__setattr__(self, "_hash", _hash)
        
        if _hash == -1:
            raise TypeError("Not all values are hashable.")
        
        return _hash
    
    def __repr__(self, *args, **kwargs):
        r"""
        Identical to dict.__repr__().
        """
        
        body = super().__repr__(*args, **kwargs)
        
        return f"frozendict({body})"
    
    def copy(self):
        r"""
        Return the object itself, as it's an immutable.
        """
        
        return self
    
    def __copy__(self, *args, **kwargs):
        r"""
        See copy().
        """
        
        return self.copy()
    
    def __deepcopy__(self, *args, **kwargs):
        r"""
        As for tuples, if hashable, see copy(); otherwise, it returns a 
        deepcopy.
        """
        
        try:
            hash(self)
        except TypeError:
            tmp = deepcopy(dict(self))
            
            return self.__class__(tmp)
        
        return self.__copy__(*args, **kwargs)
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self), ))
    
    def __setitem__(self, key, val, *args, **kwargs):
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item "
            "assignment"
        )
    
    def __delitem__(self, key, *args, **kwargs):
        raise TypeError(
            f"'{self.__class__.__name__}' object doesn't support item "
            "deletion"
        )
        

frozendict.clear = _immutable
frozendict.pop = _immutable
frozendict.popitem = _immutable
frozendict.setdefault = _immutable
frozendict.update = _immutable
frozendict.__delattr__ = _immutable
frozendict.__setattr__ = _immutable
frozendict.__ior__ = _immutable

__all__ = (frozendict.__name__, )
