r"""
Provides frozendict, a simple immutable dictionary.
"""


class LoudImportWarning(RuntimeWarning):
    r"""
    An ImportWarning that is shown by default.
    """


try:   # pragma: no cover
    from ._frozendict import *
    c_ext = True
    # noinspection PyUnresolvedReferences
    del _frozendict
except ImportError as e:
    if not isinstance(e, ModuleNotFoundError):  # pragma: no cover
        import traceback
        import warnings

        # the 3-argument form works also on Python < 3.10
        tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))

        warnings.warn(
            "frozendict C extension failed to load, "
            f"using the pure Python implementation:\n{tb}",
            LoudImportWarning
        )

        del traceback
        del warnings
        del tb

    from ._frozendict_py import *
    c_ext = False

from . import cool
from . import monkeypatch
from .cool import *
from .version import version as __version__


def _getFrozendictJsonEncoder(BaseJsonEncoder = None):
    if BaseJsonEncoder is None:  # pragma: no cover
        from json.encoder import JSONEncoder
        
        BaseJsonEncoder = JSONEncoder
    
    class FrozendictJsonEncoderInternal(BaseJsonEncoder):
        def default(self, obj):
            if isinstance(obj, frozendict):  # pragma: no cover
                # TODO create a C serializer
                return dict(obj)
            
            return BaseJsonEncoder.default(
                self,
                obj
            )  # pragma: no cover
    
    return FrozendictJsonEncoderInternal


FrozendictJsonEncoder = _getFrozendictJsonEncoder()
monkeypatch.patchOrUnpatchAll(patch = True, warn = False)


from collections.abc import Mapping

# noinspection PyUnresolvedReferences
Mapping.register(frozendict)
del Mapping


import copy as _copy


def _deepcopy_frozendict(x, memo, deepcopy=_copy.deepcopy):
    y = {}

    for key, value in x.items():
        y[deepcopy(key, memo)] = deepcopy(value, memo)

    # a recursive frozendict already copied it in memo
    try:
        return memo[id(x)]
    except KeyError:
        pass

    return frozendict(y)

_deepcopy_dispatch = getattr(_copy, "_deepcopy_dispatch", None)

if _deepcopy_dispatch is None:  # pragma: no cover
    monkeypatch.warn_not_applied("copy._deepcopy_dispatch")
else:
    _deepcopy_dispatch[frozendict] = _deepcopy_frozendict

del _copy
del _deepcopy_frozendict
del _deepcopy_dispatch

if c_ext:  # pragma: no cover
    __all__ = (frozendict.__name__, )
else:
    __all__ = _frozendict_py.__all__
    del _frozendict_py

# TODO deprecated, to remove in future versions
FrozenOrderedDict = frozendict

__all__ += cool.__all__
__all__ += ("FrozendictJsonEncoder", "FrozenOrderedDict")
