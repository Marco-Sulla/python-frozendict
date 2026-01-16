from __future__ import annotations

from typing import (
    TypeVar,
    overload,
    Optional,
    Union,
    Any,
    Dict,
    Callable,
)

from collections.abc import Hashable

try:
    from typing import Mapping, Iterable, Iterator, Tuple, Type
except ImportError:
    from collections.abc import Mapping, Iterable, Iterator
    Tuple = tuple
    Type = type

try:
    from typing import Self
except ImportError:
    Self = TypeVar("Self", bound=frozendict[K, V])

K = TypeVar("K")
V = TypeVar("V", covariant=True)
K2 = TypeVar("K2")
V2 = TypeVar("V2", covariant=True)

# noinspection PyPep8Naming
class frozendict(Mapping[K, V]):
    @overload
    def __new__(cls: Type[Self]) -> Self: ...
    @overload
    def __new__(cls: Type[Self], **kwargs: V) -> frozendict[str, V]: ...
    @overload
    def __new__(cls: Type[Self], mapping: Mapping[K, V]) -> Self: ...
    @overload
    def __new__(cls: Type[Self], iterable: Iterable[Tuple[K, V]]) -> Self: ...
    
    def __getitem__(self: Self, key: K) -> V: ...
    def __len__(self: Self) -> int: ...
    def __iter__(self: Self) -> Iterator[K]: ...
    def __hash__(self: Self) -> int: ...
    def __reversed__(self: Self) -> Iterator[K]: ...
    def copy(self: Self) -> Self: ...
    def __copy__(self: Self) -> Self: ...
    def __deepcopy__(self: Self) -> Self: ...
    def delete(self: Self, key: K) -> Self: ...
    @overload
    def key(self: Self, index: int) -> K: ...
    @overload
    def key(self: Self) -> K: ...
    @overload
    def value(self: Self, index: int) -> V: ...
    @overload
    def value(self: Self) -> V: ...
    @overload
    def item(self: Self, index: int) -> Tuple[K, V]: ...
    @overload
    def item(self: Self) -> Tuple[K, V]: ...
    @overload
    def __or__(self: Self, other: Mapping[K, V]) -> Self: ...
    @overload
    def __or__(self: Self, other: Mapping[K2, V]) -> frozendict[Union[K, K2], V]: ...
    @overload
    def __or__(self: Self, other: Mapping[K, V2]) -> frozendict[K, Union[V, V2]]: ...
    @overload
    def __or__(self: Self, other: Mapping[K2, V2]) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    @overload
    def set(self: Self, key: K, value: V) -> Self: ...
    @overload
    def set(self: Self, key: K2, value: V) -> frozendict[Union[K, K2], V]: ...
    @overload
    def set(self: Self, key: K, value: V2) -> frozendict[K, Union[V, V2]]: ...
    @overload
    def set(self: Self, key: K2, value: V2) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    @overload
    def setdefault(self: Self, key: K) -> Self: ...
    @overload
    def setdefault(self: Self, key: K2) -> Self: ...
    @overload
    def setdefault(self: Self, key: K, default: V) -> Self: ...
    @overload
    def setdefault(self: Self, key: K2, default: V) -> frozendict[Union[K, K2], V]: ...
    @overload
    def setdefault(self: Self, key: K, default: V2) -> frozendict[K, Union[V, V2]]: ...
    @overload
    def setdefault(self: Self, key: K2, default: V2) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    
    @classmethod
    def fromkeys(
        cls: Type[Self], 
        seq: Iterable[K], 
        value: Optional[V] = None
    ) -> Self: ...


FrozenOrderedDict = frozendict
c_ext: bool

class FreezeError(Exception):  pass


class FreezeWarning(UserWarning):  pass

# PyCharm complains about returning Hashable, because
# it's not subscriptable
def deepfreeze(
        o: Any,
        custom_converters: Optional[Dict[Any, Callable[[Any], Hashable]]] = None,
        custom_inverse_converters: Optional[Dict[Any, Callable[[Any], Any]]] = None
) -> Any: ...

def register(
    to_convert: Any,
    converter: Callable[[Any], Any],
    *,
    inverse: bool = False
) -> None: ...

def unregister(
    type: Any,
    inverse: bool = False
) -> None: ...
