import pytest
import frozendict as cool
from frozendict import frozendict
from collections import OrderedDict
from array import array
from types import MappingProxyType


@pytest.fixture
def before_cure():
    return {"x": [
        5, 
        frozendict(y = {5, "b", memoryview(b"b")}), 
        array("B", (0, 1, 2)), 
        OrderedDict(a=bytearray(b"a")),
        MappingProxyType({2: []})
    ]}
    

@pytest.fixture
def after_cure():
    return frozendict(x = (
        5, 
        frozendict(y = frozenset({5, "b", memoryview(b"b")})), 
        (0, 1, 2), 
        frozendict(a = b'a'),
        MappingProxyType({2: ()})
    ))

def test_deepfreeze(before_cure, after_cure):
    assert cool.deepfreeze(before_cure) == after_cure
