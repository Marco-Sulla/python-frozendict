import inspect

class frozendictbase(dict):
    """
    This class is identical to frozendict, but without the slots. Useful for
    inheriting.
    """

    @classmethod
    def fromkeys(cls, seq, value=None, *args, **kwargs):
        return cls(dict.fromkeys(seq, value, *args, **kwargs))

    def __init__(self, *args, **kwargs):
        """
        Identical to dict.__init__(). It can't be reinvoked
        """
        
        self._klass = type(self)
        self._klass_name = self._klass.__name__

        self._immutable_err = "'{klass}' object is immutable".format(klass=self._klass_name)

        if hasattr(self, "_initialized") and self._initialized:
            raise NotImplementedError(self._immutable_err)

        mysuper = super()

        if len(args) == 1 and type(args[0]) == self._klass and not kwargs:
            old = args[0]
            mysuper.__init__(old)
            self._hash = old._hash
            self._repr = old._repr
        else:
            mysuper.__init__(*args, **kwargs)

            self._hash = hash(frozenset(mysuper.items()))
            self._repr = None

        self._initialized = True

    def __hash__(self, *args, **kwargs):
        return self._hash
    
    def __repr__(self, *args, **kwargs):
        if self._repr is None:
            self._repr = "{klass}({body})".format(
                klass = self._klass_name, 
                body = super().__repr__(*args, **kwargs)
            )
        return self._repr
    
    def copy(self, *args, **kwargs):
        return self._klass(self)

    def __copy__(self, *args, **kwargs):
        return self.copy()

    def __deepcopy__(self, *args, **kwargs):
        return self.copy()

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

    def __reduce__(self, *args, **kwargs):
        return (self._klass, (dict(self), ))


    def __setattr__(self, *args, **kwargs):
        """
        not implemented
        """
        
        if not hasattr(self, "_initialized"):
            super().__setattr__("_initialized", False)

        if not self._initialized or inspect.stack()[1].filename == __file__:
            super().__setattr__(*args, **kwargs)
        else :
            raise NotImplementedError(self._immutable_err)


    def __delattr__(self, *args, **kwargs):
        """
        not implemented
        """

        raise NotImplementedError(self._immutable_err)

    def __delitem__(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def __setitem__(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def clear(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def pop(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def popitem(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def setdefault(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

    def update(self, *args, **kwargs):
        """
        not implemented
        """
        
        raise NotImplementedError(self._immutable_err)

class frozendict(frozendictbase):
    """
    A simple immutable dictionary.

    The API is the same as `dict`, without methods that can change the 
    immutability.
    In addition, it supports the __add__ and __sub__ operands.
    """

    __slots__ = ("_initialized", "_hash", "_repr", "_immutable_err", "_klass", "_klass_name")


__all__ = (frozendict.__name__, frozendictbase.__name__)
