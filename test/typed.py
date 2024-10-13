#!/usr/bin/env python3

import copy
from collections.abc import Hashable
from typing import (
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
    Union,
    Tuple,
)

from frozendict import frozendict
from typing_extensions import assert_type, Never

fd = frozendict(a=1, b=2)

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
assert_type(fd.items(), ItemsView[str, int])
assert_type(fd.keys(), KeysView[str])
assert_type(fd.values(), ValuesView[int])
assert_type(copy.copy(fd), frozendict[str, int])
assert_type(copy.deepcopy(fd), frozendict[str, int])
# noinspection PyUnresolvedReferences
assert_type(reversed(fd), reversed[str])
assert_type(fd.delete("a"), frozendict[str, int])

assert_type(fd | {"c": 2}, frozendict[str, int])
assert_type(fd | {1: 2}, frozendict[Union[str, int], int])
assert_type(fd | {"c": "c"}, frozendict[str, Union[str, int]])
assert_type(fd | {1: "c"}, frozendict[Union[str, int], Union[str, int]])

assert_type(fd.setdefault("a", 0), frozendict[str, int])
assert_type(fd.setdefault("a", "a"), frozendict[str, Union[str, int]])
assert_type(fd.setdefault(0, 0), frozendict[Union[str, int], int])

assert_type(
    fd.setdefault(0, "a"),
    frozendict[Union[str, int], Union[str, int]]
)

assert_type(fd.set("abc", 1), frozendict[str, int])

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
