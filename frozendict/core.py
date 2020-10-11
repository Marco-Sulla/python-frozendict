from copy import deepcopy


def _immutable(self, *args, **kwargs):
    r"""
    Function for not implemented method since the object is immutable
    """
    
    raise NotImplementedError(f"`{self.__class__.__name__}` object is immutable.")


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
    
    def __new__(cls, *args, **kwargs):
        r"""
        Almost identical to dict.__new__().
        """
        
        has_kwargs = bool(kwargs)
        continue_creation = True
        
        # check if there's only an argument and it's of the same class
        if len(args) == 1 and not has_kwargs:
            it = args[0]
            
            # no isinstance, to avoid subclassing problems
            if it.__class__ == cls:
                self = it
                continue_creation = False
        
        if continue_creation:
            self = super().__new__(cls)
            
            super(cls, self).__init__(*args, **kwargs)
            
            # empty singleton - start
            
            if self.__class__ == cls and not len(self):
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
    
    def _hash_no_errors(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise returns -1
        """
        
        _hash = self._hash
        
        if _hash is None:
            # try to cache the hash. You have to use `object.__setattr__()`
            # because the `__setattr__` of the class is inhibited 
            hash1 = 0

            for v in self.values():
                try:
                    hash_v = v.__hash__()
                except Exception:
                    hash_res = -1
                    object.__setattr__(self, "_hash", hash_res)
                    return hash_res
                
                hash1 ^= ((hash_v ^ 89869747) ^ (hash_v << 16)) * 3644798167

            hash2 = hash1 ^ ((len(self) + 1) * 1927868237)
            hash3 = (hash2 ^ ((hash2 >> 11) ^ (hash2 >> 25))) * 69069 + 907133923

            if hash3 == -1:
                hash_res = 590923713
            else:
                hash_res = hash3
            
            object.__setattr__(self, "_hash", hash_res)
        else:
            hash_res = _hash
        
        return hash_res
    
    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise raises a 
        TypeError.
        """
        
        _hash = self._hash_no_errors(*args, **kwargs)
        
        if _hash == -1:
            raise TypeError("Not all values are hashable.")
        
        return _hash
    
    def __repr__(self, *args, **kwargs):
        r"""
        Identical to dict.__repr__().
        """
        
        body = super().__repr__(*args, **kwargs)
        
        return f"{self.__class__.__name__}({body})"
    
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
        If hashable, see copy(). Otherwise it returns a deepcopy.
        """
        
        _hash = self._hash_no_errors(*args, **kwargs)
        
        if _hash == -1:
            tmp = deepcopy(dict(self))
            
            return self.__class__(tmp)
        
        return self.copy()
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self), ))
        

frozendict.clear = _immutable
frozendict.pop = _immutable
frozendict.popitem = _immutable
frozendict.setdefault = _immutable
frozendict.update = _immutable
frozendict.__delitem__ = _immutable
frozendict.__setitem__ = _immutable
frozendict.__delattr__ = _immutable
frozendict.__setattr__ = _immutable

__all__ = (frozendict.__name__, )
