import subprocess
import sys
from pathlib import Path

py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor

if py_ver_major == 3 and py_ver_minor < 8:
    print(
        f"Python is version {py_ver_major}.{py_ver_minor}, not "
        "running type checker"
    )
    
    sys.exit(0)

curr_file = Path(__file__)
curr_dir = curr_file.parent

subprocess.run(
    "mypy typed.py",
    shell=True,
    check=True,
    cwd=str(curr_dir)
)
