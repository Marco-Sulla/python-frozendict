rm test/core.*

./test/debug.py && python -X faulthandler -m pytest -p no:faulthandler
