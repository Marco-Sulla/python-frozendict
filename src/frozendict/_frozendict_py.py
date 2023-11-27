from copy import deepcopy

def immutable(self, *args, **kwargs):
    r"""
    Function for not implemented method since the object is immutable
    """
    
    raise AttributeError(f"'{self.__class__.__name__}' object is read-only")

_empty_frozendict = None

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
                global _empty_frozendict

                if _empty_frozendict is None:
                    _empty_frozendict = self
                else:
                    self = _empty_frozendict
                    continue_creation = False
            
            # empty singleton - end
            
            if continue_creation:
                object.__setattr__(self, "_hash", -1)
        
        return self
    
    def __init__(self, *args, **kwargs):
        pass
    
    def __hash__(self, *args, **kwargs):
        r"""
        Calculates the hash if all values are hashable, otherwise raises a 
        TypeError.
        """
        
        if self._hash != -1:
            _hash = self._hash
        else:
            fs = frozenset(self.items())
            _hash = hash(fs)
            
            object.__setattr__(self, "_hash", _hash)
        
        return _hash
    
    def __repr__(self, *args, **kwargs):
        r"""
        Identical to dict.__repr__().
        """
        
        body = super().__repr__(*args, **kwargs)
        klass = self.__class__
        
        if klass == frozendict:
            name = f"frozendict.{klass.__name__}"
        else:
            name = klass.__name__
        
        return f"{name}({body})"
    
    def copy(self):
        r"""
        Return the object itself, as it's an immutable.
        """
        
        klass = self.__class__
        
        if klass == frozendict:
            return self
        
        return klass(self)
    
    def __copy__(self, *args, **kwargs):
        r"""
        See copy().
        """
        
        return self.copy()
    
    def __deepcopy__(self, memo, *args, **kwargs):
        r"""
        As for tuples, if hashable, see copy(); otherwise, it returns a 
        deepcopy.
        """
        
        klass = self.__class__
        return_copy = klass == frozendict
        
        if return_copy:
            try:
                hash(self)
            except TypeError:
                return_copy = False
        
        if return_copy:
            return self.copy()
            
        tmp = deepcopy(dict(self))
        
        return klass(tmp)
        
    
    def __reduce__(self, *args, **kwargs):
        r"""
        Support for `pickle`.
        """
        
        return (self.__class__, (dict(self), ))
    
    def set(self, key, val):
        new_self = deepcopy(dict(self))
        new_self[key] = val
        
        return self.__class__(new_self)
    
    def setdefault(self, key, default=None):
        if key in self:
            return self
        
        new_self = deepcopy(dict(self))
        
        new_self[key] = default
        
        return self.__class__(new_self)
    
    def delete(self, key):
        new_self = deepcopy(dict(self))
        del new_self[key]
        
        if new_self:
            return self.__class__(new_self)
        
        return self.__class__()
        
    def _get_by_index(self, collection, index):
        try:
            return collection[index]
        except IndexError:
            maxindex = len(collection) - 1
            name = self.__class__.__name__
            raise IndexError(f"{name} index {index} out of range {maxindex}") from None
    
    def key(self, index=0):
        collection = tuple(self.keys())
        
        return self._get_by_index(collection, index)
    
    def value(self, index=0):
        collection = tuple(self.values())
        
        return self._get_by_index(collection, index)
    
    def item(self, index=0):
        collection = tuple(self.items())
        
        return self._get_by_index(collection, index)
    
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

def frozendict_or(self, other, *args, **kwargs):
    res = {}
    res.update(self)
    res.update(other)
    
    return self.__class__(res)

frozendict.__or__ = frozendict_or
frozendict.__ior__ = frozendict_or

try:
    frozendict.__reversed__
except AttributeError:
    def frozendict_reversed(self, *args, **kwargs):
        return reversed(tuple(self))
    
    frozendict.__reversed__ = frozendict_reversed
    

frozendict.clear = immutable
frozendict.pop = immutable
frozendict.popitem = immutable
frozendict.update = immutable
frozendict.__delattr__ = immutable
frozendict.__setattr__ = immutable
frozendict.__module__ = 'frozendict'

_sentinel = object()
out_of_range_err_tpl = "{name} index {index} out of max range {sign}{maxpos}"
by_values = ("key", "value")

def sortByKey(x):
    return x[0]

def sortByValue(x):
    return x[1]

def checkPosition(obj, index):
    length = len(obj)
    
    if abs(index) >= length:
        name = obj.__class__.__name__
        maxpos = length - 1
        sign = "-" if index < 0 else ""
        err = out_of_range_err_tpl.format(
            name=name, 
            index=index, 
            sign=sign, 
            maxpos=maxpos
        )
        
        return IndexError(err)
    
    return None

class coold(frozendict):
    def __getitem__(self, key, *args, **kwargs):
        try:
            start = key.start
            stop = key.stop
            step = key.step
        except AttributeError:
            return dict.__getitem__(self, key)
        else:
            items = tuple(self.items())
            new_items = items[start:stop:step]
            return self.__class__(new_items)
    
    def delete_by_index(self, index=None):
        length = len(self)
        
        if index == None:
            index = length - 1
        
        err = checkPosition(self, index)
        
        if err != None:
            raise err
        
        if index < 0:
            index = length + index
        
        new_self = self[0:index]
        dict.update(new_self, self[index+1:None])
        
        if new_self:
            return new_self
        
        return self.__class__()
    
    def move(self, pos, end_pos=None):
        length = len(self)
        
        if end_pos == None:
            end_pos = length - 1
        
        bad1 = abs(pos) >= length
        
        if bad1 or abs(end_pos) >= length:
            err1 = checkPosition(self, pos)
            
            if err1 != None:
                raise err1
            
            err2 = checkPosition(self, end_pos)
            
            if err2 != None:
                raise err2
        
        if pos < 0:
            pos = length + pos
        
        if end_pos < 0:
            end_pos = length + end_pos
        
        item = self[pos:pos+1]
        
        if end_pos > pos:
            new_self = self[0:pos]
            dict.update(new_self, self[pos+1:end_pos+1])
            dict.update(new_self, item)
            dict.update(new_self, self[end_pos+1:None])
        else:
            new_self = self[0:end_pos]
            dict.update(new_self, item)
            dict.update(new_self, self[end_pos:pos])
            dict.update(new_self, self[pos+1:None])
        
        return new_self
    
    def insert(self, index, key, val):
        err = checkPosition(self, index)
        
        if err != None:
            raise err
        
        if key in self:
            name = self.__class__.__name__
            raise KeyError(f"Key `{key}` is already in the {name}")
        
        res = self[0:index]
        dict.update(res, {key: val})
        dict.update(res, self[index:None])
        
        return res
    
    def index(self, val, by="key"):
        if by == "key":
            obj = self
            Exc = KeyError
        elif by == "value":
            obj = self.values()
            Exc = ValueError
        else:
            by_values = ", ".join(by_values)
            
            raise ValueError(
                f"`by` parameter accept one of this values: {by_values}"
            )
        
        for i, v in enumerate(obj):
            if v == val:
                return i
        
        if by == "value":
            name = self.__class__.__name__
            raise Exc(f"{val} is not in {name} values")
        
        raise Exc(val)
        
    def _get_by_index(self, collection, index):
        try:
            return collection[index]
        except IndexError:
            maxindex = len(collection) - 1
            name = self.__class__.__name__
            raise IndexError(f"{name} index {index} out of range {maxindex}") from None
    
    def value(self, index=0):
        collection = tuple(self.values())
        
        return self._get_by_index(collection, index)
    
    def key(self, index=0):
        collection = tuple(self.keys())
        
        return self._get_by_index(collection, index)
    
    def item(self, index=0):
        collection = tuple(self.items())
        
        return self._get_by_index(collection, index)
    
    def sort(self, by=None, **kwargs):
        key = kwargs.get("key")
        
        if by != None and key != None:
            raise ValueError("You can't specify both `by` and `key` parameters")
        elif key == None:
            if by == None or by == "key":
                key = sortByKey
            elif by == "value":
                key = sortByValue
            else:
                by_values = ", ".join(by_values)
                
                raise ValueError(
                    f"`by` parameter accept one of this values: {by_values}"
                )
            
            kwargs["key"] = key
        
        new_self = list(self.items())
        new_self_sorted = sorted(new_self, **kwargs)
        
        return self.__class__(new_self_sorted)
    
def get_deep(self, *args, default=_sentinel):
    r"""
        Get a nested element of the dictionary.
        
        The method accepts multiple arguments or a single one. If a single
        argument is passed, it must be an iterable. This represents the
        keys or indexes of the nested element.
        
        The method first tries to get the value v1 of the dict using the
        first key. If it finds v1 and there's no other key, v1 is
        returned. Otherwise, the method tries to retrieve the value from v1
        associated with the second key/index, and so on.
        
        If in any point, for any reason, the value can't be retrieved, the
        `default` parameter is returned if specified. Otherwise, a
        KeyError or an IndexError is raised.
        """
    
    if len(args) == 1:
        single = True
        
        it_tpm = args[0]
        
        try:
            len(it_tpm)
            it = it_tpm
        except Exception:
            # maybe it's a generator
            try:
                it = tuple(it_tpm)
            except Exception:
                err = (
                    f"`{self.get_deep.__name__}` called with a single " + 
                    "argument supports only iterables"
                )
                
                raise TypeError(err) from None
    else:
        it = args
        single = False
    
    if not it:
        if single:
            raise ValueError(
                f"`{self.get_deep.__name__}` argument is empty"
            )
        else:
            raise TypeError(
                f"`{self.get_deep.__name__}` expects at least one argument"
            )
    
    obj = self
    
    for k in it:
        try:
            obj = obj[k]
        except (KeyError, IndexError) as e:
            if default is _sentinel:
                raise e from None
            
            return default
    
    return obj
    
    def __sub__(self, other, *args, **kwargs):
        r"""
        The method will create a new `coold`, result of the subtraction 
        by `other`. 
        
        If `other` is a `dict`-like, the result will have the items of the 
        `coold` that are *not* in common with `other`.
        
        If `other` is another type of iterable, the result will have the 
        items of `coold` without the keys that are in `other`.
        """
        
        try:
            iter(other)
        except Exception:
            err = (
                f"Unsupported operand type(s) for -: " + 
                "`{self.__class__.__name__}` and `{other.__class__.__name__}`"
            )
            
            raise TypeError(err) from None
        
        try:
            res = {k: v for k, v in self.items() if (k, v) not in other.items()}
        except Exception:
            if not hasattr(other, "gi_running"):
                true_other = other
            else:
                true_other = tuple(other)
            
            res = {k: v for k, v in self.items() if k not in true_other}
        
        return self.__class__(res)
    
    def __and__(self, other, *args, **kwargs):
        r"""
        Returns a new `coold`, that is the intersection between `self` 
        and `other`.
        
        If `other` is a `dict`-like object, the intersection will contain 
        only the *items* in common.
        
        If `other` is another iterable, the intersection will contain
        the items of `self` which keys are in `other`.
        
        Iterables of pairs are *not* managed differently. This is for 
        consistency.
        
        Beware! The final order is dictated by the order of `other`. This 
        allows the coder to change the order of the original `coold`.
        
        The last two behaviors breaks voluntarly the `dict.items()` API, for 
        consistency and practical reasons.
        """
        
        try:
            try:
                res = {k: v for k, v in other.items() if (k, v) in self.items()}
            except Exception:
                res = {k: self[k] for k in other if k in self}
        except Exception:
            err = (
                f"Unsupported operand type(s) for &: " + 
                "`{self.__class__.__name__}` and `{other.__class__.__name__}`"
            )
            
            raise TypeError(err) from None
        
        return self.__class__(res)
    
    def isdisjoint(self, other):
        r"""
        Returns True if `other` dict-like object has no items in common, 
        otherwise False. Equivalent to `not (coold & dict_like)`
        """
        
        try:
            other.items
        except AttributeError:
            err = (
                f"Unsupported operand type(s) for &: " + 
                f"`{self.__class__.__name__}` and `{other.__class__.__name__}`"
            )
            
            raise TypeError(err) from None
        else:
            res = self & other
        
        return not res

__all__ = (frozendict.__name__, )
