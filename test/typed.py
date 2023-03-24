from frozendict import frozendict  # error: Library stubs not installed for "frozendict" (or incompatible with Python 3.10)
d = frozendict(a=1, b=2)
reveal_type(dict.fromkeys("abc", 0))  # Revealed type is "builtins.dict[builtins.str*, builtins.int*]"
reveal_type(frozendict.fromkeys("abc", 0))  # Revealed type is "Any"
