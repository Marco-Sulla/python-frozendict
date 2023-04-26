rm -rf build dist *.egg-info
CIBUILDWHEEL=1 ./setup.py $*
