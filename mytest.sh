rm test/core.*

./test/debug.py && pytest

if command -v mypy &> /dev/null
then
    mypy test/typed.py
fi

if command -v pyright &> /dev/null
then
    pyright test/typed.py
fi
