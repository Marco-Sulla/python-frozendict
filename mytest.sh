cd test
rm core.*

./debug.py 100 && pytest
