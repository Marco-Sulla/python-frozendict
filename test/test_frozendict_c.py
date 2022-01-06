import pytest
import frozendict as frozendict_module
from frozendict import frozendict as frozendict_class
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
