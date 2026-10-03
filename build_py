rm -rf build dist src/*.egg-info src/*/*.so
args="$*"

if [ "$args" == '' ]; then
    args="bdist_wheel"
fi

FROZENDICT_PURE_PY=1 ./setup.py $args
