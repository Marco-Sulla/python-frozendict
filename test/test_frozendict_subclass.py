import pytest
from frozendict.core import frozendict

class F(frozendict):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

frozendict_class = F

from pathlib import Path

curr_path = Path(__file__)
curr_dir = curr_path.parent

common_path = curr_dir / "common.py"

with open(common_path) as f:
    common_code = f.read()

exec(common_code)

with open(curr_dir / "subclass_only.py") as f:
    subclass_only_code = f.read()

exec(subclass_only_code)
