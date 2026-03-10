rm -rf build dist src/*.egg-info src/*/*.so
args="$*"

if [ "$args" == '' ]; then
    args="build_ext --inplace"
fi

CIBUILDWHEEL=1 ./setup.py $args
