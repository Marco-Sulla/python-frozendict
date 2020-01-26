class frozendict(dict):
    """
    A simple immutable dictionary.
    
    The API is the same as `dict`, without methods that can change the 
    immutability.
    In addition, it supports __hash__() and the operands __add__() and 
    __sub__().
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
    
    def __new__(klass, *args, **kwargs):
        r"""
        Almost identical to dict.__new__().
        """
        
        # enable attribute setting for __init__,
        # only for the first time
        klass.__setattr__ = object.__setattr__
        
        has_kwargs = bool(kwargs)
        
        if len(args) == 1 and not has_kwargs:
            it = args[0]
            
            if hasattr(it, "is_frozendict"):
                it.initialized = 2
                return it
        
        use_empty = False
        
        if hasattr(klass, "empty") and not has_kwargs:
            use_empty = True
            
            for arg in args:
                if arg:
                    use_empty = False
                    break
            
        if not use_empty:
            self = super().__new__(klass)
            self.initialized = False
        else:
            self = klass.empty
        
        return self
    
    def __init__(self, *args, **kwargs):
        r"""
        Almost identical to dict.__init__(). It can't be reinvoked.
        """
        
        if self.initialized == 2:
            self.initialized = True
            return
        
        klass = self.__class__
        
        if hasattr(klass, "empty") and self is klass.empty:
            return
        
        if self.initialized:
            # object is immutable, can't be initialized twice
            raise NotImplementedError(f"`{klass.__name__}` object is immutable.")
        
        super().__init__(*args, **kwargs)
        
        self._hash = None
        self.initialized = True
        self.is_frozendict = True
        
        # create the empty object singleton if does not exists yet
        if not self and not hasattr(klass, "empty"):
            klass.empty = self
        
        # object is created, now inhibit `__setattr__()`
        klass.__setattr__ = klass.notimplemented
    
    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise raises a 
        TypeError.
        """
        
        _hash = self._hash
        
        if _hash is None:
            try:
                # try to cache the hash. You have to use `object.__setattr__()`
                # because the `__setattr__` of the class is inhibited 
                _hash = hash(tuple(self.items()))
            except Exception:
                # object is not hashable
                object.__setattr__(self, "_hash", "unhashable")
                raise TypeError("Not all values are hashable.")
            else:
                object.__setattr__(self, "_hash", _hash)
        elif _hash == "unhashable":
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
        See copy().
        """
        
        return self.copy()
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self), ))
    
    def __add__(self, other, *args, **kwargs):
        """
        If you add a dict-like object, a new frozendict will be returned, equal 
        to the old frozendict updated with the other object.
        """
        
        tmp = dict(self)
        
        try:
            tmp.update(other)
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for +: `{self.__class__.__name__}` and `{type(other).__name__}`")
        
        return self.__class__(tmp)
    
    def __sub__(self, iterable, *args, **kwargs):
        """
        You can subtract an iterable from a frozendict. A new frozendict will 
        be returned, without the keys that are in the iterable.
        """
        
        try:
            iter(iterable)
        except Exception:
            raise TypeError(f"Unsupported operand type(s) for -: `{self.__class__.__name__}` and `{type(iterable).__name__}`")
        
        if not hasattr(iterable, "gi_running"):
            true_iterable = iterable
        else:
            true_iterable = tuple(iterable)
        
        return self.__class__(
            {k: v for k, v in self.items() if k not in true_iterable}
        )
    
    def notimplemented(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        raise NotImplementedError(f"`{self.__class__.__name__}` object is immutable.")
    
    def __delattr__(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def __delitem__(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def __setitem__(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def clear(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def pop(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def popitem(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def setdefault(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()
    
    def update(self, *args, **kwargs):
        """
        Not implemented.
        """
        
        self.notimplemented()

__all__ = (frozendict.__name__, )
