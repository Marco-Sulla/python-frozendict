r"""
Provides frozendict, a simple immutable dictionary.
"""
try:
    from ._frozendict import *
    c_ext = True
    del _frozendict
except ImportError:
    from .core import *
    c_ext = False

from .version import version as __version__
import collections.abc as _abc

# Horrible tricks - Start

if c_ext:
    import json
    
    OriginalJsonEncoder = json.encoder.JSONEncoder

    class FrozendictEncoder(OriginalJsonEncoder):
        def default(self, obj):
            if isinstance(obj, frozendict) and not isinstance(obj, dict):
                # TODO create a C serializer
                return dict(obj)
            
            return OriginalJsonEncoder.default(self, obj)

    json.JSONEncoder = FrozendictEncoder
    json.encoder.JSONEncoder = FrozendictEncoder

    json._default_encoder = FrozendictEncoder(
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        indent=None,
        separators=None,
        default=None,
    )
    
    del OriginalJsonEncoder
    del json
    
    def monkeypatchOrjson():
        import orjson
        
        oldOrjsonDumps = orjson.dumps

        def myOrjsonDumps(obj, *args, **kwargs):
            if isinstance(obj, frozendict):
                obj = dict(obj)
            
            return oldOrjsonDumps(obj, *args, **kwargs)

        orjson.dumps = myOrjsonDumps
        orjson.orjson.dumps = myOrjsonDumps
    
    try:
        import orjson
    except ImportError:
        pass
    else:
        monkeypatchOrjson()
else:
    @classmethod
    def _my_subclasshook(klass, subclass):
        if issubclass(subclass, frozendict):
            return False
        
        return NotImplemented
    
    _abc.MutableMapping.__subclasshook__ = _my_subclasshook
    
    del _my_subclasshook

# Horrible tricks - End

_abc.Mapping.register(frozendict)

from pathlib import Path

curr_path = Path(__file__)
curr_dir = curr_path.parent

if c_ext:
    __all__ = ("frozendict", )
else:
    __all__ = core.__all__

# TODO deprecated, to remove in future versions
FrozenOrderedDict = frozendict
__all__ += ("FrozenOrderedDict", )

del Path
del curr_path
del curr_dir
del _abc

if not c_ext:
    del core
