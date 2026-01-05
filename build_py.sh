rm -rf build dist *.egg-info
FROZENDICT_PURE_PY=1 ./setup.py $*
