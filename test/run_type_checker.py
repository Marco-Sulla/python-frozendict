#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

version_info = sys.version_info

if version_info < (3, 10):
    print(
        f"Python is version {version_info[0]}.{version_info[1]}, not "
        "running type checker"
    )

    sys.exit(0)

curr_file = Path(__file__)
curr_dir = curr_file.parent

res = subprocess.run(
    "mypy typed.py",
    shell=True,
    cwd=str(curr_dir),
    check=True,
)
