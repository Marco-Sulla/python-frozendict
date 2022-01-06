import pytest
import frozendict as frozendict_module
from frozendict import coold as frozendict_class
from pathlib import Path

c_ext = True

curr_path = Path(__file__)
curr_dir = curr_path.parent

common_path = curr_dir / "common.py"

with open(common_path) as f:
    common_code = f.read()

exec(common_code)

c_only_path = curr_dir / "c_only.py"

with open(c_only_path) as f:
    c_only_code = f.read()

exec(c_only_code)

with open(curr_dir / "frozendict_only.py") as f:
    frozendict_only_code = f.read()

exec(frozendict_only_code)

def test_coold_set_replace(fd_dict, generator_seq2):
    items = tuple(generator_seq2)
    d2 = dict(items)
    assert fd_dict != d2
    fd2 = frozendict_class(items)
    fd3 = fd2.set("Sulla", "Marco")
    assert fd3 == fd_dict

def test_coold_set_add(fd_dict):
    d2 = dict(fd_dict, a="b")
    assert fd_dict != d2
    fd2 = frozendict_class(fd_dict)
    fd3 = fd2.set("a", "b")
    assert fd3 == d2

def test_coold_del(fd_dict):
    d2 = dict(fd_dict)
    d2["a"] = "b"
    fd2 = frozendict_class(d2)
    fd3 = fd2.delete("a")
    assert fd3 == fd_dict
