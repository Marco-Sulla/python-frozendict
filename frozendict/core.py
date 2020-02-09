from copy import deepcopy


def notimplemented(self, *args, **kwargs):
    r"""
    Not implemented.
    """
    
    raise NotImplementedError(f"`{self.__class__.__name__}` object is immutable.")


def sortMapItemsByValue(item):
    return item[1]


_sentinel = object()


class frozendict(dict):
    r"""
    A simple immutable dictionary.
    
    The API is the same as `dict`, without methods that can change the 
    immutability.
    In addition, it supports __hash__(), a slightly modified version of the
    `set` API and some other useful method.
    """
    
    __slots__ = (
        "initialized", 
        "_hash", 
        "is_frozendict", 
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
        
        # enable attribute setting for __init__,
        # only for the first time
        cls.__setattr__ = object.__setattr__
        
        has_kwargs = bool(kwargs)
        
        if len(args) == 1 and not has_kwargs:
            it = args[0]
            
            if isinstance(it, cls):
                it.initialized = 2
                return it
        
        use_empty = False
        
        if not has_kwargs:
            use_empty = True
            
            for arg in args:
                if arg:
                    use_empty = False
                    break
            
        if use_empty:
            try:
                self = cls.empty
                return self
            except AttributeError:
                initialized = 3
        else:
            initialized = 0
        
        self = super().__new__(cls)
        self.initialized = initialized
                
        
        return self
    
    def __init__(self, *args, **kwargs):
        r"""
        Almost identical to dict.__init__(). It can't be reinvoked.
        """
        
        if self.initialized == 2:
            self.initialized = 1
            return
        
        klass = self.__class__
        
        if self.initialized != 3 and self is klass.empty:
            return
        
        if self.initialized == 1:
            # object is immutable, can't be initialized twice
            notimplemented(self)
        
        super().__init__(*args, **kwargs)
        
        self._hash = None
        self.initialized = 1
        self.is_frozendict = True
        
        # object is created, now inhibit its mutability
        klass.__setattr__ = notimplemented
    
    def get_deep(self, *args, default=_sentinel):
        r"""
        Get a nested element of the `frozendict`.
        
        The method accepts multiple arguments or a single one. If a single 
        arguments is passed, it must be an iterable. These represents the
        keys or indexes of the nested element.
        
        The method first tries to get the value v1 of `frozendict` using the 
        first key. If it found v1 and there's no other key, v1 is 
        returned. Otherwise, the method tries to retrieve the value from v1
        associated to the second key/index, and so on.
        
        If in any point, for any reason, the value can't be retrieved, if 
        `default` parameter is specified, its value is returned. Otherwise, a 
        KeyError or a IndexError is raised.
        """
        
        if len(args) == 1:
            single = True
            
            it_tpm = args[0]
            
            try:
                len(it_tpm)
                it = it_tpm
            except Exception:
                # maybe it's an iterator
                try:
                    it = tuple(it_tpm)
                except Exception:
                    raise TypeError(f"`{self.get_deep.__name__}` called with a single argument supports only iterables") from None
        else:
            it = args
            single = False
        
        if not it:
            if single:
                raise ValueError(f"`{self.get_deep.__name__}` argument is empty")
            else:
                raise TypeError(f"`{self.get_deep.__name__}` expects at least one argument")
        
        obj = self
        
        for k in it:
            try:
                obj = obj[k]
            except (KeyError, IndexError):
                if default is _sentinel:
                    raise
                
                return default
        
        return obj
    
    def hash_no_errors(self, *args, **kwargs):
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
        
        _hash = self.hash_no_errors(*args, **kwargs)
        
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
        
        _hash = self.hash_no_errors(*args, **kwargs)
        
        if _hash == -1:
            tmp = deepcopy(dict(self))
            
            return self.__class__(tmp)
        
        return self.copy()
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self), ))
    
    def sorted(self, *args, by="keys", **kwargs):
        r"""
        Return a new `frozendict`, with the element insertion sorted.
        The signature is the same of builtin `sorted()` function, except for 
        the additional parameter `by`, that is "keys" by default and can also
        be "values". So the resulting `frozendict` can be sorted by keys or
        values.
        If you want more complicated sorts, see the documentation of 
        `sorted()`.
        """
        
        if not self:
            return self
        
        sort_by_keys = by == "keys"
        
        if sort_by_keys:
            tosort = self.keys()
        elif by == "values":
            tosort = self.items()
        else:
            raise ValueError(f"Unexpected value for parameter `by`: {by}")
        
        if not sort_by_keys:
            kwargs.setdefault("key", sortMapItemsByValue)
        
        it_sorted = sorted(tosort, *args, **kwargs)
        
        if it_sorted == list(tosort):
            return self
        
        res = {}
        
        if sort_by_keys:
            for k in it_sorted:
                res[k] = self[k]
        else:
            for k, v in it_sorted:
                res[k] = v
        
        return self.__class__(res)
    
    def __add__(self, other, *args, **kwargs):
        r"""
        If you add a dict-like object, a new frozendict will be returned, equal 
        to the old frozendict updated with the other object.
        """
        
        tmp = dict(self)
        
        try:
            tmp.update(other)
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for +: `{self.__class__.__name__}` and `{other.__class__.__name__}`") from None
        
        return self.__class__(tmp)
    
    def __sub__(self, iterable, *args, **kwargs):
        r"""
        You can subtract an iterable from a frozendict. A new frozendict will 
        be returned, without the keys that are in the iterable.
        """
        
        try:
            iter(iterable)
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for -: `{self.__class__.__name__}` and `{iterable.__class__.__name__}`") from None
        
        if not hasattr(iterable, "gi_running"):
            true_iterable = iterable
        else:
            true_iterable = tuple(iterable)
        
        return self.__class__(
            {k: v for k, v in self.items() if k not in true_iterable}
        )
    
    def __and__(self, other, *args, **kwargs):
        r"""
        Returns a new `frozendict`, that is the intersection between `self` 
        and `other`.
        
        If `other` is a `dict`-like object, the intersection will contain 
        only the *items* in common.
        
        If `other` is another iterable, the intersection will contain
        the items of `self` which keys are in `other`.
        
        Iterables of pairs are *not* managed differently. This is for 
        consistency.
        
        Beware! The final order is dictated by the order of `other`. This 
        allows the coder to change the order of the original `frozendict`.
        
        The last two behaviors breaks voluntarly the `dict.items()` API, for 
        consistency and practical reasons.
        """
        
        try:
            try:
                res = {k: v for k, v in other.items() if (k, v) in self.items()}
            except Exception:
                res = {k: self[k] for k in other if k in self}
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for &: `{self.__class__.__name__}` and `{other.__class__.__name__}`") from None
        
        return self.__class__(res)
    
    def isdisjoint(self, other):
        r"""
        Returns True if `other` dict-like object has no keys in common, 
        otherwise False. Equivalent to `not bool(frozendict & dict_like)`
        """
        
        try:
            other.items
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for &: `{self.__class__.__name__}` and `{other.__class__.__name__}`") from None
        
        (little, big) = (
            (self, other) 
            if len(self) < len(other) 
            else (other, self)
        )
        
        for k in little:
            if k in big:
                return False
        
        return True
        


frozendict.clear = notimplemented
frozendict.pop = notimplemented
frozendict.popitem = notimplemented
frozendict.setdefault = notimplemented
frozendict.update = notimplemented
frozendict.__delitem__ = notimplemented
frozendict.__setitem__ = notimplemented
frozendict.__delattr__ = notimplemented
frozendict.__setattr__ = notimplemented
frozendict.empty = frozendict()

__all__ = (frozendict.__name__, )
