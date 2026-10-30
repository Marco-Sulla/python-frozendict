import gc
import pickle
import sys
import weakref
from collections.abc import MutableMapping
from copy import copy, deepcopy

import pytest

from frozendict import frozendict
from .base import FrozendictSubclass, FrozendictTestBase


pyversion = sys.version_info
dict_ior_skip = pyversion < (3, 9)
dict_ior_skip_reason = "dict |= frozendict do not mutate dict inplace in 3.8-"


class Map(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]
    
    def __iter__(self):
        return iter(self._dict)
    
    def __len__(self):
        return len(self._dict)


class DictSubclass(dict):
    pass


class Key:
    pass


# noinspection PyMethodMayBeStatic
class FrozendictCommonTest(FrozendictTestBase):
    @property
    def is_mapping_implemented(self):
        return self.c_ext or pyversion > (3, 7)
    
    @property
    def is_reversed_implemented(self):
        return self.c_ext or pyversion > (3, 9)

    def assert_same_unless_sub(self, res, orig):
        if self.is_subclass:
            assert res is not orig
        else:
            assert res is orig

    ####################################################################
    # main tests

    def test_bool_false(self, fd_empty):
        assert not fd_empty

    def test_constructor_kwargs(self, fd2, fd_dict_2):
        assert self.FrozendictClass(**fd_dict_2) == fd2

    def test_constructor_self(self, fd):
        assert fd == self.FrozendictClass(fd, Guzzanti="Corrado")

    def test_constructor_generator(self, fd, generator_seq2):
        assert fd == self.FrozendictClass(
            generator_seq2,
            Guzzanti="Corrado"
        )

    def test_constructor_hole(self, fd_hole, fd_dict_hole):
        assert fd_hole == self.FrozendictClass(fd_dict_hole)

    def test_constructor_map(self, fd_dict):
        assert self.FrozendictClass(Map(fd_dict)) == fd_dict

    def test_normalget(self, fd):
        assert fd["Guzzanti"] == "Corrado"

    def test_keyerror(self, fd):
        with pytest.raises(KeyError):
            # noinspection PyStatementEffect
            fd["Brignano"]

    def test_len(self, fd, fd_dict):
        assert len(fd) == len(fd_dict)

    def test_in_true(self, fd):
        assert "Guzzanti" in fd

    def test_not_in_false(self, fd):
        assert not ("Guzzanti" not in fd)

    def test_in_false(self, fd):
        assert not ("Brignano" in fd)

    def test_not_in_true(self, fd):
        assert "Brignano" not in fd

    def test_bool_true(self, fd):
        assert fd

    def test_deepcopy_unhashable(self, fd_unhashable):
        fd_copy = deepcopy(fd_unhashable)
        assert fd_copy == fd_unhashable
        assert fd_copy is not fd_unhashable

    def test_deepcopy_unhashable_memo(self, fd_unhashable):
        fd_unhashable[1].append(fd_unhashable)
        fd_copy_2 = deepcopy(fd_unhashable)

        if self.is_subclass:
            # subclasses doesn't call deepcopy but __reduce_ex__, that makes one more copy
            assert type(fd_copy_2[1][0]) is self.FrozendictClass
            assert fd_copy_2[1][0][1] is fd_copy_2[1]
        else:
            # memo works
            assert fd_copy_2 is fd_copy_2[1][0]

    def test_deepcopy_memo(self, unhashable):
        orig = [unhashable, self.FrozendictClass(a=unhashable)]
        res = deepcopy(orig)
        unashable2 = res[0]
        fd = res[1]
        assert fd["a"] is unashable2
        assert unashable2 is not unhashable
        assert type(fd) is self.FrozendictClass

    def test_not_equal(self, fd, fd2, fd_sabina):
        assert fd != fd_sabina
        assert fd != fd2
        assert not (fd == fd_sabina)
        assert not (fd == fd2)

    def test_equals_dict(self, fd, fd_dict):
        assert fd == fd_dict

    @pytest.mark.parametrize(
            "protocol",
            range(pickle.HIGHEST_PROTOCOL + 1)
    )
    def test_pickle(self, fd, protocol):
        # noinspection PyTypeChecker
        dump = pickle.dumps(fd, protocol=protocol)
        assert dump
        assert pickle.loads(dump) == fd

    def test_constructor_iterator(self, fd, fd_items):
        assert self.FrozendictClass(fd_items) == fd

    def test_todict(self, fd, fd_dict):
        assert dict(fd) == fd_dict

    def test_get(self, fd):
        assert fd.get("Guzzanti") == "Corrado"

    def test_get_fail(self, fd):
        default = object()
        assert fd.get("Brignano", default) is default

    def test_keys(self, fd, fd_dict):
        assert tuple(fd.keys()) == tuple(fd_dict.keys())

    def test_values(self, fd, fd_dict):
        assert tuple(fd.values()) == tuple(fd_dict.values())

    def test_items(self, fd, fd_dict):
        assert tuple(fd.items()) == tuple(fd_dict.items())

    def test_fromkeys(self, fd_sabina):
        keys = ["Corrado", "Sabina"]
        f = self.FrozendictClass.fromkeys(keys, "Guzzanti")
        assert f == fd_sabina

    def test_fromkeys_dict(self, fd_sabina, fd_dict_sabina):
        f = self.FrozendictClass.fromkeys(fd_dict_sabina, "Guzzanti")
        assert f == fd_sabina

    def test_fromkeys_set(self, fd_sabina, fd_dict_sabina):
        f = self.FrozendictClass.fromkeys(
            set(fd_dict_sabina),
            "Guzzanti"
        )
        
        assert f == fd_sabina

    @pytest.fixture
    def build_fds(self, fd_dict_sabina, fd_sabina_seq2):
        # one frozendict for every path that builds its keys from d
        def build_fds(d):
            [(key, value)] = d.items()
            d_hole = {**fd_dict_sabina, **d}
            del d_hole["Sabina"]

            return {
                "dict": self.FrozendictClass(d),
                "dict with holes": self.FrozendictClass(d_hole),
                "seq2": self.FrozendictClass(d.items()),
                "mapping": self.FrozendictClass(Map(d)),
                "fromkeys": self.FrozendictClass.fromkeys(list(d)),
                "fromkeys dict": self.FrozendictClass.fromkeys(d),
                "fromkeys set": self.FrozendictClass.fromkeys(set(d)),
                "|": fd_sabina_seq2 | d,
                "set": fd_sabina_seq2.set(key, value),
                "setdefault": fd_sabina_seq2.setdefault(key, value),
            }

        return build_fds

    def test_str_lookup_with_non_str_key(self, build_fds, fd_dict_zero):
        assert hash("") == hash(0)

        for name, fd in build_fds(fd_dict_zero).items():
            assert "" not in fd, name

    def test_gc_cycle_through_key(self, build_fds):
        for name in list(build_fds({Key(): None})):
            key = Key()
            key.fd = build_fds({key: None})[name]
            ref = weakref.ref(key)
            del key
            gc.collect()
            assert ref() is None, name

    def test_iter(self, fd):
        items = []

        for x in iter(fd):
            items.append((x, fd[x]))

        assert tuple(items) == tuple(fd.items())

    def test_sum(self, fd, fd_dict, fd_dict_sabina):
        new_fd = fd | fd_dict_sabina
        assert type(new_fd) is self.FrozendictClass
        new_dict = dict(fd_dict)
        new_dict.update(fd_dict_sabina)
        assert new_fd == new_dict

    def test_union(self, fd_dict, fd_sabina):
        new_fd = self.FrozendictClass(fd_dict)
        id_fd = id(new_fd)
        new_fd |= fd_sabina
        assert type(new_fd) is self.FrozendictClass
        assert id_fd != id(new_fd)
        new_dict = dict(fd_dict)
        new_dict.update(fd_sabina)
        assert new_fd == new_dict

    def test_reversed(self, fd, fd_dict):
        assert (tuple(reversed(fd)) == tuple(reversed(tuple(fd_dict))))

    def test_iter_len(self, fd):
        assert iter(fd).__length_hint__() >= 0

    def test_keys_len(self, fd):
        assert len(fd.keys()) == len(fd)

    def test_keys_bool_false(self, fd_empty):
        assert not fd_empty.keys()

    def test_keys_bool_true(self, fd):
        assert fd.keys()

    def test_items_len(self, fd):
        assert len(fd.items()) == len(fd)

    def test_values_len(self, fd):
        assert len(fd.values()) == len(fd)

    def test_equal_keys(self, fd, fd_dict):
        assert fd.keys() == fd_dict.keys()

    def test_equal_items(self, fd, fd_dict):
        assert fd.items() == fd_dict.items()

    def test_in_keys(self, fd):
        assert "Guzzanti" in fd.keys()

    def test_in_items(self, fd):
        assert ("Guzzanti", "Corrado") in fd.items()

    def test_disjoint_true_keys(self, fd, fd_sabina):
        assert fd.keys().isdisjoint(fd_sabina)

    def test_disjoint_true_items(self, fd, fd_sabina):
        assert fd.items().isdisjoint(fd_sabina.items())

    def test_disjoint_false_keys(self, fd):
        assert not fd.keys().isdisjoint(fd)

    def test_disjoint_false_items(self, fd):
        assert not fd.items().isdisjoint(fd.items())

    def test_sub_keys(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.keys()) - frozenset(fd_dict_2.keys())
        assert fd.keys() - fd2.keys() == res

    def test_sub_items(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.items()) - frozenset(fd_dict_2.items())
        assert fd.items() - fd2.items() == res

    def test_and_keys(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.keys()) & frozenset(fd_dict_2.keys())
        assert fd.keys() & fd2.keys() == res

    def test_and_items(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.items()) & frozenset(fd_dict_2.items())
        assert fd.items() & fd2.items() == res

    def test_or_keys(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.keys()) | frozenset(fd_dict_2.keys())
        assert fd.keys() | fd2.keys() == res

    def test_or_items(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.items()) | frozenset(fd_dict_2.items())
        assert fd.items() | fd2.items() == res

    def test_or_dict(self, fd, fd_dict, fd_dict_2):
        expected = {**fd_dict, **fd_dict_2}
        res = fd | fd_dict_2
        assert list(res.items()) == list(expected.items())
        assert type(res) is type(fd)

    def test_or_not_dict(self, fd):
        with pytest.raises(TypeError):
            fd | ["Brignano", "Enrico"]

    def test_ior_dict(self, fd, fd_dict, fd_dict_2):
        expected = {**fd_dict, **fd_dict_2}
        res = fd
        res |= fd_dict_2
        assert list(res.items()) == list(expected.items())
        assert type(res) is type(fd)

    def test_dict_or(self, fd, fd_dict, fd_dict_2):
        expected = {**fd_dict_2, **fd_dict}
        res = fd_dict_2 | fd
        assert list(res.items()) == list(expected.items())
        assert type(res) is type(fd_dict_2)

    @pytest.mark.skipif(dict_ior_skip, reason=dict_ior_skip_reason)
    def test_dict_ior(self, fd, fd_dict, fd_dict_2):
        expected = {**fd_dict_2, **fd_dict}
        res = fd_dict_2
        res |= fd
        assert list(res.items()) == list(expected.items())
        assert res is fd_dict_2

    def test_or_dict_empty_left(self, fd_empty, fd_dict_2):
        res = fd_empty | fd_dict_2
        assert type(res) is type(fd_empty)
        assert res == fd_dict_2
        assert res is not fd_dict_2

    def test_ior_dict_empty_left(self, fd_empty, fd_dict_2):
        res = fd_empty
        res |= fd_dict_2
        assert type(res) is type(fd_empty)
        assert res == fd_dict_2
        assert res is not fd_dict_2

    def test_or_empty_right_subclass(self, fd):
        res = fd | DictSubclass()
        assert type(res) is type(fd)
        assert res == fd
        assert res is not fd

    def test_or_tracked(self, fd_unhashable):
        assert gc.is_tracked(fd_unhashable | {3: 4})

    def test_dict_or_empty_left(self, fd, fd_dict, dict_empty):
        res = dict_empty | fd
        assert type(res) is type(dict_empty)
        assert res == fd
        assert res is not fd

    def test_dict_or_empty_right(self, fd_empty, fd_dict_2):
        res = fd_dict_2 | fd_empty
        assert type(res) is type(fd_dict_2)
        assert res == fd_dict_2
        assert res is not fd_dict_2

    @pytest.mark.skipif(dict_ior_skip, reason=dict_ior_skip_reason)
    def test_dict_ior_empty_right(self, fd_empty, fd_dict_2):
        fd_dict_2_copy = fd_dict_2.copy()
        res = fd_dict_2
        res |= fd_empty
        assert res == fd_dict_2_copy
        assert res is fd_dict_2

    @pytest.mark.skipif(dict_ior_skip, reason=dict_ior_skip_reason)
    def test_dict_ior_empty_left(self, fd, fd_dict, dict_empty):
        res = dict_empty
        res |= fd
        assert res == fd
        assert res is dict_empty

    def test_xor_keys(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.keys()) ^ frozenset(fd_dict_2.keys())
        assert fd.keys() ^ fd2.keys() == res

    def test_xor_items(self, fd, fd_dict, fd2, fd_dict_2):
        res = frozenset(fd_dict.items()) ^ frozenset(fd_dict_2.items())
        assert fd.items() ^ fd2.items() == res

    @pytest.mark.parametrize(
            "protocol",
            range(pickle.HIGHEST_PROTOCOL + 1)
    )
    def test_pickle_iter_key(self, fd, protocol):
        orig = iter(fd.keys())
        # noinspection PyTypeChecker
        dump = pickle.dumps(orig, protocol=protocol)
        assert dump
        assert tuple(pickle.loads(dump)) == tuple(orig)

    @pytest.mark.parametrize(
            "protocol",
            range(pickle.HIGHEST_PROTOCOL + 1)
    )
    def test_pickle_iter_item(self, fd, protocol):
        orig = iter(fd.items())
        # noinspection PyTypeChecker
        dump = pickle.dumps(orig, protocol=protocol)
        assert dump
        assert tuple(pickle.loads(dump)) == tuple(orig)

    @pytest.mark.parametrize(
            "protocol",
            range(pickle.HIGHEST_PROTOCOL + 1)
    )
    def test_pickle_iter_value(self, fd, protocol):
        orig = iter(fd.values())
        # noinspection PyTypeChecker
        dump = pickle.dumps(orig, protocol=protocol)
        assert dump
        assert tuple(pickle.loads(dump)) == tuple(orig)

    def test_lt_key(self, fd, fd_hole):
        assert fd_hole.keys() < fd.keys()

    def test_gt_key(self, fd, fd_hole):
        assert fd.keys() > fd_hole.keys()

    def test_le_key(self, fd, fd_hole):
        assert fd_hole.keys() <= fd.keys()
        assert fd.keys() <= fd.keys()

    def test_ge_key(self, fd, fd_hole):
        assert fd.keys() >= fd_hole.keys()
        assert fd.keys() >= fd.keys()

    def test_lt_item(self, fd, fd_hole):
        assert fd_hole.items() < fd.items()

    def test_gt_item(self, fd, fd_hole):
        assert fd.items() > fd_hole.items()

    def test_le_item(self, fd, fd_hole):
        assert fd_hole.items() <= fd.items()
        assert fd.items() <= fd.items()

    def test_ge_item(self, fd, fd_hole):
        assert fd.items() >= fd_hole.items()
        assert fd.items() >= fd.items()
    
    def test_mapping_keys(self, fd):
        if not self.is_mapping_implemented:
            pytest.skip("mapping not implemented")
        
        assert fd.keys().mapping == fd
    
    def test_mapping_items(self, fd):
        if not self.is_mapping_implemented:
            pytest.skip("mapping not implemented")
        
        assert fd.items().mapping == fd
    
    def test_mapping_values(self, fd):
        if not self.is_mapping_implemented:
            pytest.skip("mapping not implemented")
        
        assert fd.values().mapping == fd

    def test_reversed_keys(self, fd, fd_dict):
        if not self.is_reversed_implemented:
            pytest.skip("reversed not implemented")
            
        fd_keys = tuple(reversed(fd.keys()))
        dict_keys = tuple(reversed(tuple(fd_dict.keys())))
        assert fd_keys == dict_keys

    def test_reversed_items(self, fd, fd_dict):
        if not self.is_reversed_implemented:
            pytest.skip("reversed not implemented")
            
        fd_items = tuple(reversed(fd.items()))
        dict_items = tuple(reversed(tuple(fd_dict.items())))
        assert fd_items == dict_items

    def test_reversed_values(self, fd, fd_dict):
        if not self.is_reversed_implemented:
            pytest.skip("reversed not implemented")
            
        fd_values = tuple(reversed(fd.values()))
        dict_values = tuple(reversed(tuple(fd_dict.values())))
        assert fd_values == dict_values

    ####################################################################
    # same object for frozendict, a new one for subclasses

    @pytest.fixture
    def fd_repr(self, fd_dict):
        name = self.FrozendictClass.__name__

        if not self.is_subclass:
            name = f"{self.FrozendictClass.__module__}.{name}"

        return f"{name}({fd_dict!r})"

    def test_empty(self, fd_empty, dict_empty):
        fd_empty_set = self.FrozendictClass(dict_empty)
        fd_empty_list = self.FrozendictClass([])
        fd_empty_dict = self.FrozendictClass(dict_empty, **dict_empty)

        assert fd_empty == fd_empty_set == fd_empty_list == fd_empty_dict
        self.assert_same_unless_sub(fd_empty_set, fd_empty)
        self.assert_same_unless_sub(fd_empty_list, fd_empty_set)
        self.assert_same_unless_sub(fd_empty_dict, fd_empty)

    def test_constructor_self_1(self, fd):
        res = self.FrozendictClass(fd)
        assert res == fd
        self.assert_same_unless_sub(res, fd)

    def test_copy(self, fd):
        # noinspection PyTestUnpassedFixture
        res = fd.copy()
        assert res == fd
        self.assert_same_unless_sub(res, fd)

    def test_copycopy(self, fd, fd_unhashable):
        for orig in (fd, fd_unhashable):
            res = copy(orig)
            assert res == orig
            self.assert_same_unless_sub(res, orig)

    def test_deepcopy(self, fd):
        res = deepcopy(fd)
        assert res == fd
        assert res is not fd

    def test_init(self, fd):
        # noinspection PyTestUnpassedFixture
        fd_copy = fd.copy()
        fd_clone = self.FrozendictClass(dict(fd))
        fd.__init__({"Trump": "Donald"})
        assert fd_copy == fd
        assert fd_clone == fd
        self.assert_same_unless_sub(fd_copy, fd)

    def test_del_empty(self, fd_empty):
        fd = self.FrozendictClass({1: 2})
        res = fd.delete(1)
        assert res == fd_empty
        assert res != fd
        self.assert_same_unless_sub(res, fd_empty)

    def test_or_empty_right(self, fd, dict_empty):
        res = fd | dict_empty
        assert res == fd
        assert type(res) is type(fd)
        self.assert_same_unless_sub(res, fd)

    def test_or_empty_left(self, fd, fd_empty):
        res = fd_empty | fd
        assert res == fd
        assert type(res) is type(fd_empty)
        self.assert_same_unless_sub(res, fd)

    def test_ior_dict_empty_right(self, fd, dict_empty):
        res = fd
        res |= dict_empty
        assert res == fd
        assert type(res) is type(fd)
        self.assert_same_unless_sub(res, fd)

    def test_or_empty_left_other_class(self, fd_dict, fd_empty):
        other_class = frozendict if self.is_subclass else FrozendictSubclass
        other = other_class(fd_dict)
        res = fd_empty | other
        assert res == other
        assert res is not other
        assert type(res) is type(fd_empty)

    def test_or_empty_both_subclass(self, fd_empty):
        res = fd_empty | DictSubclass()
        assert res == fd_empty
        assert type(res) is type(fd_empty)
        self.assert_same_unless_sub(res, fd_empty)

    def test_repr(self, fd, fd_repr):
        assert repr(fd) == fd_repr

    def test_str(self, fd, fd_repr):
        assert str(fd) == fd_repr

    def test_format(self, fd, fd_repr):
        assert format(fd) == fd_repr

    ####################################################################
    # frozendict-only tests

    def test_hash(self, fd, fd_eq):
        assert hash(fd)
        assert hash(fd) == hash(fd_eq)

    def test_unhashable_value(self, fd_unhashable):
        with pytest.raises(TypeError):
            hash(fd_unhashable)

        # hash is cached
        with pytest.raises(TypeError):
            hash(fd_unhashable)

    def test_set_replace(self, fd_dict, generator_seq2):
        items = tuple(generator_seq2)
        d2 = dict(items)
        assert fd_dict != d2
        fd2 = self.FrozendictClass(items)
        fd3 = fd2.set("Guzzanti", "Corrado")
        assert fd3 == fd_dict
        assert fd3 != fd2

    def test_set_add(self, fd_dict):
        d2 = dict(fd_dict, a="b")
        assert fd_dict != d2
        fd2 = self.FrozendictClass(fd_dict)
        fd3 = fd2.set("a", "b")
        assert fd3 == d2
        assert fd3 != fd2

    def test_set_empty(self, fd_empty, dict_empty):
        fd_empty.set("a", "b")
        assert fd_empty == dict_empty

    def test_set_tracked(self, fd_unhashable):
        assert gc.is_tracked(fd_unhashable.set(3, 4))

    def test_setdefault_notinsert(self, fd, fd_dict):
        assert fd.setdefault("Hicks") is fd

    def test_setdefault_insert_default(self, fd, fd_dict):
        fd_dict.setdefault("Allen")
        fd_new = fd.setdefault("Allen")
        assert fd_dict == fd_new
        assert fd_new != fd

    def test_setdefault_insert(self, fd, fd_dict):
        fd_dict.setdefault("Allen", "Woody")
        fd_new = fd.setdefault("Allen", "Woody")
        assert fd_dict == fd_new
        assert fd_new != fd

    def test_setdefault_unhashable(self, fd, unhashable):
        with pytest.raises(TypeError):
            fd.setdefault(unhashable, "Woody")

    def test_setdefault_empty(self, fd_empty, dict_empty):
        fd_empty.setdefault("a", "b")
        assert fd_empty == dict_empty

    def test_setdefault_tracked(self, fd_unhashable):
        assert gc.is_tracked(fd_unhashable.setdefault(3, 4))

    def test_del(self, fd_dict):
        d2 = dict(fd_dict)
        d2["a"] = "b"
        fd2 = self.FrozendictClass(d2)
        fd3 = fd2.delete("a")
        assert fd3 == fd_dict
        assert fd3 != fd2

    def test_del_tracked(self, fd_unhashable):
        assert gc.is_tracked(fd_unhashable.delete(2))

    def test_key(self, fd):
        assert fd.key() == fd.key(0) == "Guzzanti"
        assert fd.key(1) == fd.key(-2) == "Hicks"

    def test_key_out_of_range(self, fd):
        with pytest.raises(IndexError):
            fd.key(3)
        
        with pytest.raises(IndexError):
            fd.key(-4)

    def test_value(self, fd):
        assert fd.value() == fd.value(0) == "Corrado"
        assert fd.value(1) == fd.value(-2) == "Bill"

    def test_value_out_of_range(self, fd):
        with pytest.raises(IndexError):
            fd.value(3)
        
        with pytest.raises(IndexError):
            fd.value(-4)

    def test_item(self, fd):
        assert fd.item() == fd.item(0) == ("Guzzanti", "Corrado")
        assert fd.item(1) == fd.item(-2) == ("Hicks", "Bill")

    def test_item_out_of_range(self, fd):
        with pytest.raises(IndexError):
            fd.item(3)
        
        with pytest.raises(IndexError):
            fd.item(-4)

    ####################################################################
    # immutability tests

    def test_normalset(self, fd):
        with pytest.raises(TypeError):
            fd["Guzzanti"] = "Caterina"

    def test_del_error(self, fd):
        with pytest.raises(TypeError):
            del fd["Guzzanti"]

    def test_clear(self, fd):
        with pytest.raises(AttributeError):
            fd.clear()

    def test_pop(self, fd):
        with pytest.raises(AttributeError):
            fd.pop("Guzzanti")

    def test_popitem(self, fd):
        with pytest.raises(AttributeError):
            fd.popitem()

    def test_update(self, fd):
        with pytest.raises(AttributeError):
            fd.update({"Brignano": "Enrico"})

    def test_delattr(self, fd):
        with pytest.raises(AttributeError):
            del fd.items

    def test_size(self):
        """Regression test for inflated dict sizes"""

        if not self.c_ext:
            pytest.skip("This can be fixed only in the C Extension")

        sizes = [
            sys.getsizeof(self.FrozendictClass(**{f"{i}": i for i in range(n)}))
            for n in range(1, 22)
        ]

        assert sizes == sorted(sizes)
