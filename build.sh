rm -rf build dist src/*.egg-info src/*/*.so
args="$*"

if [ "$args" == '' ]; then
    args="bdist_wheel"
fi

CIBUILDWHEEL=1 ./setup.py $args
