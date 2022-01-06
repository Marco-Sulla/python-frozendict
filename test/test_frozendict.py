import pytest
from frozendict.core import frozendict as frozendict_class
from pathlib import Path

c_ext = False

curr_path = Path(__file__)
curr_dir = curr_path.parent

with open(curr_dir / "common.py") as f:
    common_code = f.read()

exec(common_code)

with open(curr_dir / "frozendict_only.py") as f:
    frozendict_only_code = f.read()

exec(frozendict_only_code)
