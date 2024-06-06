import json

import frozendict as cool
import pytest
from frozendict import frozendict
from frozendict.monkeypatch import MonkeypatchWarning


class A:
    pass


@pytest.fixture
def object_to_serialize():
    return frozendict()


@pytest.fixture
def object_to_serialize_2():
    return A()


@pytest.fixture
def serialized_object():
    return "{}"


def test_get_json_encoder(
    object_to_serialize,
    object_to_serialize_2,
    serialized_object,
):
    if cool.c_ext:
        cool.monkeypatch.patchOrUnpatchJson(patch=True)
    else:
        with pytest.warns(MonkeypatchWarning):
            cool.monkeypatch.patchOrUnpatchJson(patch=True, warn=True)
    
    assert json.dumps(object_to_serialize) == serialized_object
    
    with pytest.raises(TypeError):
        json.dumps(object_to_serialize_2)
    
    cool.monkeypatch.patchOrUnpatchJson(patch=False, warn=False)
    
    if cool.c_ext:
        with pytest.raises(TypeError):
            json.dumps(object_to_serialize)
