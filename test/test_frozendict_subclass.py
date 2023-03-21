import pytest
from frozendict.core import frozendict

c_ext = False
frozendict_superclass = frozendict

from pathlib import Path

curr_path = Path(__file__)
curr_dir = curr_path.parent

with open(curr_dir / "init_subclass.py") as f:
    init_subclass_code = f.read()

exec(init_subclass_code)

common_path = curr_dir / "common.py"

with open(curr_dir / "subclass_only.py") as f:
    subclass_only_code = f.read()

exec(subclass_only_code)

with open(common_path) as f:
    common_code = f.read()

exec(common_code)
