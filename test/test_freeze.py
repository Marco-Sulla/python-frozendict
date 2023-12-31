import pytest
import frozendict as cool
from frozendict import frozendict
from collections import OrderedDict
from array import array
from types import MappingProxyType
from frozendict import FreezeError, FreezeWarning


class A:
    def __init__(self, x):
        self.x = x


def custom_a_converter(a):
    return frozendict(**a.__dict__, y="mbuti")


@pytest.fixture
def a():
    a = A(3)
    
    return a


@pytest.fixture
def before_cure(a):
    return {"x": [
        5, 
        frozendict(y = {5, "b", memoryview(b"b")}), 
        array("B", (0, 1, 2)), 
        OrderedDict(a=bytearray(b"a")),
        MappingProxyType({2: []}),
        a
    ]}
    

@pytest.fixture
def after_cure():
    return frozendict(x = (
        5, 
        frozendict(y = frozenset({5, "b", memoryview(b"b")})), 
        (0, 1, 2), 
        frozendict(a = b'a'),
        MappingProxyType({2: ()}),
        frozendict(x = 3),
    ))


@pytest.fixture
def after_cure_a(a):
    return custom_a_converter(a)


def test_deepfreeze(before_cure, after_cure):
    assert cool.deepfreeze(before_cure) == after_cure

def test_register_bad_to_convert():
    with pytest.raises(ValueError):
        cool.register(5, 7)

def test_register_bad_converter():
    with pytest.raises(ValueError):
        cool.register(frozendict, 7)

def test_unregister_not_present():
    with pytest.raises(FreezeError):
        cool.unregister(frozendict)

def test_deepfreeze_bad_custom_converters_key():
    with pytest.raises(ValueError):
        cool.deepfreeze(before_cure, custom_converters={7:7})

def test_deepfreeze_bad_custom_converters_val():
    with pytest.raises(ValueError):
        cool.deepfreeze(before_cure, custom_converters={frozendict:7})

def test_deepfreeze_bad_custom_inverse_converters_key():
    with pytest.raises(ValueError):
        cool.deepfreeze(before_cure, custom_inverse_converters={7:7})

def test_deepfreeze_bad_custom_inverse_converters_val():
    with pytest.raises(ValueError):
        cool.deepfreeze(before_cure, custom_inverse_converters={frozendict:7})


def test_register_custom(a):
    cool.register(A, custom_a_converter)
    assert cool.deepfreeze(a) == custom_a_converter(a)
    cool.unregister(A)
    assert cool.deepfreeze(a) == frozendict(a.__dict__)
    
    
def test_deepfreeze_custom(a):
    assert cool.deepfreeze(
        a,
        custom_converters={A: custom_a_converter}
    ) == custom_a_converter(a)


def test_register_warning():
    with pytest.warns(FreezeWarning):
        cool.register(bytearray, bytes)
