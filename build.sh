rm -rf build dist ./*.egg-info
args="$*"

if [ "$args" == '' ]; then
    args="bdist_wheel"
fi

CIBUILDWHEEL=1 ./setup.py "$args"
