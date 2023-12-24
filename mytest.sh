rm test/core.*

./test/debug.py && pytest

if command -v mypy &> /dev/null
then
    pushd src
    mypy ../test/typed.py
    popd
fi

if command -v pyright &> /dev/null
then
    pyright test/typed.py
fi
