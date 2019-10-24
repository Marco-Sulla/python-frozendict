class frozendictbase(dict):
    """
    This class is identical to frozendict, but without the slots. Useful for
    inheriting.
    """

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        return cls(dict.fromkeys(*args, **kwargs))

    def __new__(klass, *args, **kwargs):
        empty = hasattr(klass, "_empty")

        if empty:
            if kwargs:
                empty = False
            else:
                for arg in args:
                    if arg:
                        empty = False
                        break

        if empty:
            self = klass._empty
        else:
            if hasattr(klass, "__setattr__"):
                klass.__setattr__ = object.__setattr__
            
            self = super().__new__(klass)
            self._initialized = False

        return self

    def __init__(self, *args, **kwargs):
        """
        Identical to dict.__init__(). It can't be reinvoked
        """
        
        _klass = type(self)

        if not (hasattr(_klass, "_empty") and self is _klass._empty):
            self._klass = _klass
            self._klass_name = self._klass.__name__

            self._immutable_err = "'{klass}' object is immutable".format(klass=self._klass_name)

            if self._initialized:
                raise NotImplementedError(self._immutable_err)
            
            super().__init__(*args, **kwargs)

            self._hash = None
            self._repr = None

            self._initialized = True

            if not hasattr(self._klass, "_empty") and not self:
                self._klass._empty = self
            
            self._klass.__setattr__ = self._klass._notimplemented

    def __hash__(self, *args, **kwargs):
        if self._hash is None:
            try:
                object.__setattr__(self, "_hash", hash(frozenset(self.items())))
            except Exception:
                object.__setattr__(self, "_hash", "unhashable")
                raise TypeError("not all values are hashable")
        elif self._hash is "unhashable":
            raise TypeError("not all values are hashable")

        return self._hash
    
    def __repr__(self, *args, **kwargs):
        if self._repr is None:
            object.__setattr__(self, "_repr", "{klass}({body})".format(
                klass = self._klass_name, 
                body = super().__repr__(*args, **kwargs)
            ))

        return self._repr
    
    def copy(self, *args, **kwargs):
        return self._klass(self)

    def __copy__(self, *args, **kwargs):
        return self.copy()

    def __deepcopy__(self, *args, **kwargs):
        return self.copy()

    def __reduce__(self, *args, **kwargs):
        return (self._klass, (dict(self), ))

    def __add__(self, other, *args, **kwargs):
        """
        If you add a dict-like object, a new frozendict will be returned, equal 
        to the old frozendict updated with the other object.
        """

        if not hasattr(other, "items"):
            raise TypeError("unsupported operand type for +: the second operand must be a dict-like object")


        tmp = dict(self)

        try:
            tmp.update(other)
        except Exception:
            raise TypeError("unsupported operand type(s) for +: '{klass1}' and '{klass2}'".format(
                klass1 = self._klass_name, 
                klass2 = type(other).__name__
            ))
        
        return self._klass(tmp)

    def __sub__(self, iterable, *args, **kwargs):
        """
        You can subtract an iterable from a frozendict. A new frozendict
        will be returned, without the keys that are in the iterable.
        """

        try:
            iter(iterable)

            if isinstance(iterable, (str, bytes, bytearray)):
                raise TypeError()
        except Exception:
            raise TypeError("unsupported operand type(s) for -: '{klass1}' and '{klass2}'".format(
                klass1 = self._klass_name, 
                klass2 = type(iterable).__name__
            ))

        return self._klass({k: v for k, v in self.items() if k not in iterable})
    
    def _notimplemented(self, *args, **kwargs):
        """
        not implemented
        """

        raise NotImplementedError(self._immutable_err)

    def __delattr__(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def __delitem__(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def __setitem__(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def clear(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def pop(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def popitem(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def setdefault(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

    def update(self, *args, **kwargs):
        """
        not implemented
        """
        
        self._notimplemented()

class frozendict(frozendictbase):
    """
    A simple immutable dictionary.

    The API is the same as `dict`, without methods that can change the 
    immutability.
    In addition, it supports the __add__ and __sub__ operands.
    """

    __slots__ = ("_initialized", "_hash", "_repr", "_immutable_err", "_klass", "_klass_name")

__all__ = (frozendict.__name__, frozendictbase.__name__)
