import collections
import operator
import functools


class frozendict(collections.Mapping):
    dict_cls = dict

    def __init__(self, *args, **kwargs):
        self._dict = self.dict_cls(*args, **kwargs)
        self._hash = None

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        if self._hash is None:
            hashes = map(hash, self.items())
            self._hash = functools.reduce(operator.xor, hashes, 0)

        return self._hash


class FrozenOrderedDict(frozendict):
    """
    It is an immutable wrapper around ordered dictionaries that implements the complete :py:class:`collections.Mapping`
    interface. It can be used as a drop-in replacement for dictionaries where immutability and ordering are desired.
    """
    dict_cls = collections.OrderedDict
