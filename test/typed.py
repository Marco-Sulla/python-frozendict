#!/usr/bin/env python3

import copy
from _collections_abc import dict_items, dict_keys, dict_values
from collections.abc import Hashable
from typing import Iterator, Mapping, Optional, Tuple, Union

from frozendict import frozendict
from typing_extensions import assert_type, Never

fd = frozendict(a=1, b=2)

assert_type(frozendict({1: 2}), frozendict[int, int])
assert_type(frozendict([(1, 2)]), frozendict[int, int])
assert_type(len(fd), int)
assert_type(hash(fd), int)
assert_type("a" in fd, bool)
assert_type(fd == {}, bool)
assert_type(str(fd), str)
assert_type(repr(fd), str)
assert_type(format(fd), str)
assert_type(reversed(fd.items()), Iterator[Tuple[str, int]])
assert_type(frozendict(), frozendict[Never, Never])
assert_type(fd, frozendict[str, int])
assert_type(fd["a"], int)
assert_type(iter(fd), Iterator[str])
assert_type(frozendict.fromkeys("abc", 0), frozendict[str, int])
assert_type(fd.copy(), frozendict[str, int])
assert_type(fd.item(0), Tuple[str, int])
assert_type(fd.item(), Tuple[str, int])
assert_type(fd.key(0), str)
assert_type(fd.key(), str)
assert_type(fd.value(0), int)
assert_type(fd.value(), int)
assert_type(fd.get("a"), Union[int, None])
assert_type(fd.items(), dict_items[str, int])
assert_type(fd.keys(), dict_keys[str, int])
assert_type(fd.values(), dict_values[str, int])
assert_type(copy.copy(fd), frozendict[str, int])
assert_type(copy.deepcopy(fd), frozendict[str, int])
assert_type(reversed(fd), Iterator[str])
assert_type(fd.delete("a"), frozendict[str, int])

assert_type(fd | {"c": 2}, frozendict[str, int])
assert_type(fd | {1: 2}, frozendict[Union[str, int], int])
assert_type(fd | {"c": "c"}, frozendict[str, Union[str, int]])
assert_type(fd | {1: "c"}, frozendict[Union[str, int], Union[str, int]])

assert_type({"c": 2} | fd, dict[str, int])
assert_type({1: 2} | fd, dict[Union[str, int], int])
assert_type({"c": "c"} | fd, dict[str, Union[str, int]])
assert_type({1: "c"} | fd, dict[Union[str, int], Union[str, int]])

assert_type(fd.setdefault("a", 0), frozendict[str, int])
assert_type(fd.setdefault("a", "a"), frozendict[str, Union[str, int]])
assert_type(fd.setdefault(0, 0), frozendict[Union[str, int], int])
assert_type(fd.setdefault(0), frozendict[Union[str, int], Optional[int]])

assert_type(
    fd.setdefault(0, "a"),
    frozendict[Union[str, int], Union[str, int]]
)

assert_type(fd.set("abc", 1), frozendict[str, int])
assert_type(fd.set(key="abc", val=1), frozendict[str, int])

assert_type(
    fd.set("abc", "abc"),
    frozendict[str, Union[str, int]]
)

assert_type(fd.set(1, 1), frozendict[Union[str, int], int])

assert_type(
    fd.set(1, "abc"),
    frozendict[Union[str, int], Union[str, int]]
)

# frozendict implements Mapping[K, V] and is covariant in V
vals: frozendict[str, Hashable] = fd
mapping: Mapping[str, Hashable] = fd
