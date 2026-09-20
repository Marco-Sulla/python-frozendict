rm -f core.*

PY_VERSION=$(python -c 'import sys; print("%d_%d" % sys.version_info[:2])')

./test/debug.py \
    && pytest \
    && PYTHONMALLOC=malloc valgrind \
        --tool=memcheck \
        --leak-check=full \
        --show-leak-kinds=definite \
        --errors-for-leak-kinds=definite \
        --num-callers=30 \
        -s \
        --error-exitcode=1 \
        --suppressions="src/frozendict/c_src/$PY_VERSION/valgrind-python.supp" \
        python -m pytest -q
