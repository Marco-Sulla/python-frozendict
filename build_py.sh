rm -rf build dist src/*.egg-info src/*/*.so
args="$*"

if [ "$args" == '' ]; then
    args="build_ext --inplace"
fi

FROZENDICT_PURE_PY=1 uv pip install -e .
