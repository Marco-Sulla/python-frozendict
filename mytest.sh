pip install --force dist/*

if [ $? -ne 0 ]; then
    exit 1;
fi

cd test
pytest

if [ $? -ne 0 ]; then
    exit 1;
fi

rm core.*
./debug.py 100
