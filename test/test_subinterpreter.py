import pytest

interpreters = pytest.importorskip("_xxsubinterpreters")


def run_in_new_interpreter(code):
    interp = interpreters.create()

    try:
        interpreters.run_string(interp, code)
    finally:
        interpreters.destroy(interp)


# Tests for Valgrind - Start

# Regression test for an old, small, edge case memory leak
# This is also a unit test, not a Valgrind-only test
def test_fromkeys_first_empty():
    code = """
from frozendict import frozendict
e = frozendict.fromkeys([])
assert e is frozendict()
"""

    run_in_new_interpreter(code)


def test_constructor_first_empty():
    code = """
from frozendict import frozendict
e = frozendict()
"""

    run_in_new_interpreter(code)


def test_deepcopy():
    code = """
from copy import deepcopy
from frozendict import frozendict
deepcopy(frozendict({1: []}))
"""

    run_in_new_interpreter(code)
# Tests for Valgrind - End
