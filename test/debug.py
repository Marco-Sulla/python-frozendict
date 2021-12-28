#!/usr/bin/env python3

import frozendict

assert frozendict.c_ext

from frozendict import frozendict, coold
from uuid import uuid4
import pickle
import sys
from pathlib import Path

def getUuid():
    return str(uuid4())

class F(frozendict):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

class C(coold):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

def print_info(klass, iterations, stmt):
    if "\n" in stmt:
        sep = "\n"
    else:
        sep = " "
    
    print(
        f"Class = {klass.__name__} - Loops: {iterations} - Evaluating:{sep}{stmt}", 
        flush=True
    )

def print_sep():
    print(
        "------------------------------------------------------------------------------", 
        flush=True
    )

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

key_in = getUuid()
dict_1 = {key_in: 0}
dict_tmp = {getUuid(): i for i in range(1, 1000)}
dict_1.update(dict_tmp)
key_notin = getUuid()
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
    #'pickle.loads(pickle.dumps(fd_1))',
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
    #'hash(fd_1)',
    'frozendict_class() == frozendict_class()', 
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
# """
# for x in fd_1.items():
#     pass
# """,
# """
# try:
#     hash(fd_unashable)
# except TypeError:
#     pass
# """,
)

print_sep()

for frozendict_class in (frozendict, F):
    print_info(
        frozendict_class, 
        iterations, 
        "frozendict_class(dict_1)"
    )
    
    fd_1 = frozendict_class(dict_1)
    print_sep()
    print_info(
        frozendict_class, 
        iterations, 
        "frozendict_class(dict_unashable)"
    )
    
    fd_unashable = frozendict_class(dict_unashable)
    print_sep()
    
    for expression in expressions:
        print_info(frozendict_class, iterations, expression)
        
        for j in range(iterations):
            eval(expression)
        
        print_sep()
    
    for code in codes:
        print_info(frozendict_class, iterations, code)
        
        for j in range(iterations):
            exec(code)
        
        print_sep()

coold_expressions = (
    "c1.set(key_in, 1000)", 
    "c1.set(key_notin, 1000)", 
    "c1.delete(key_in)", 
)

for cooold_class in (coold, C):
    print_info(cooold_class, iterations, "cooold_class(dict_1)")
    c1 = cooold_class(dict_1)
    print_sep()
    
    for expression in coold_expressions:
        print_info(cooold_class, iterations, expression)
        
        for j in range(iterations):
            eval(expression)
        
        print_sep()
