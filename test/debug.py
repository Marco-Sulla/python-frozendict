#!/usr/bin/env python3

import frozendict

assert frozendict.c_ext

from frozendict import frozendict
from uuid import uuid4
import pickle
import sys
from pathlib import Path

def getUuid():
    return str(uuid4())

class F(frozendict):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

argv = sys.argv
iterations = None
args_num = 1
right_len = args_num + 1
len_argv = len(argv)

if len_argv == right_len:
    try:
        iterations = int(argv[1])
    except Exception:
        pass

if len_argv != right_len or iterations == None:
    err = (
        f"{Path(__file__).name} should have {args_num} and only " + 
        f"{args_num} integer parameter"
    )
    
    print(err, file=sys.stderr)
    exit(1)

dict_1 = {getUuid(): i for i in range(1000)}
dict_2 = {getUuid(): i for i in range(1000)}
dict_3 = {i: i for i in range(1000)}
dict_unashable = dict_1.copy()
dict_unashable.update({getUuid(): []})
dict_1_items = tuple(dict_1.items())
dict_1_keys = tuple(dict_1.keys())
dict_1_keys_set = set(dict_1_keys)

expressions = (
    'frozendict_class(dict_1)',
    'frozendict_class(dict_3)',
    'frozendict_class()',
    'frozendict_class({})',
    'frozendict_class([])',
    'frozendict_class({}, **{})',
    'frozendict_class(**dict_1)',
    'frozendict_class(dict_1, **dict_2)',
    'frozendict_class(fd_1)',
    'fd_1.copy()',
    'fd_1 == dict_1',
    'fd_1 == fd_1',
    'pickle.loads(pickle.dumps(fd_1))',
    'frozendict_class(dict_1_items)',
    'fd_1.keys()',
    'fd_1.values()',
    'fd_1.items()',
    'frozendict_class.fromkeys(dict_1)',
    'frozendict_class.fromkeys(dict_1, 1)',
    'frozendict_class.fromkeys(dict_1_keys)',
    'frozendict_class.fromkeys(dict_1_keys, 1)',
    'frozendict_class.fromkeys(dict_1_keys_set)',
    'frozendict_class.fromkeys(dict_1_keys_set, 1)',
    'repr(fd_1)',
    'fd_1 | dict_2',
    'hash(fd_1)',
)

codes = (
"""
for x in fd_1:
    pass
""",
"""
for x in fd_1.keys():
    pass
""",
"""
for x in fd_1.values():
    pass
""",
"""
for x in fd_1.items():
    pass
""",
"""
try:
    hash(fd_unashable)
except TypeError:
    pass
""",
)

for frozendict_class in (frozendict, F):
    fd_1 = frozendict_class(dict_1)
    fd_unashable = frozendict_class(dict_unashable)
    
    for expression in expressions:
        print(expression)
        
        for j in range(iterations):
            eval(expression)
    
    for code in codes:
        print(code)
        
        for j in range(iterations):
            exec(code)
