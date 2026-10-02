import pytest

interpreters = pytest.importorskip("_xxsubinterpreters")


# Each source must create the very first empty frozendict of a fresh
# interpreter: the leak only shows up under valgrind (mytest.sh all).
@pytest.mark.parametrize("source", ("[]", "{}", "set()"))
def test_fromkeys_first_empty(source):
    code = f"""
from frozendict import frozendict
e = frozendict.fromkeys({source})
assert e is frozendict()
assert len(e) == 0
"""

    interp = interpreters.create()

    try:
        interpreters.run_string(interp, code)
    finally:
        interpreters.destroy(interp)
