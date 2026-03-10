rm -rf build dist ./*.egg-info
args="$*"

if [ "$args" == '' ]; then
    args="build_ext --inplace"
fi

CIBUILDWHEEL=1 ./setup.py $args
