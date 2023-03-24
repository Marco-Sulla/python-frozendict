import pytest
import frozendict as cool
from frozendict import frozendict
from collections import OrderedDict
from array import array


@pytest.fixture
def before_cure():
    return {"x": [5, {"y": {5, 7}}, array("B", (0, 1, 2)), OrderedDict(a=bytearray(b"a"))]}
    

@pytest.fixture
def after_cure():
    return frozendict({'x': (5, frozendict({'y': frozenset({5, 7})}), (0, 1, 2), frozendict({'a': b'a'}))})

def test_deepfreeze(before_cure, after_cure):
    assert cool.deepfreeze(before_cure) == after_cure
