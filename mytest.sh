pip install --force dist/*

if [ $? -ne 0 ]; then
    exit 1;
fi

cd test
rm core.*

./debug.py 100

if [ $? -ne 0 ]; then
    exit 1;
fi

pytest
