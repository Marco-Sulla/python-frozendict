#!/usr/bin/env python3

import immutables
from frozendict import frozendict
import timeit
import uuid

dictionary_sizes = (5, 1000, )
max_size = max(dictionary_sizes)

def getUuid():
    return str(uuid.uuid4())

statements = (
    {"code": "get(key)", "setup": "key = getUuid(); get = x.get", "iterations": 13000000, "name": "d.get(key)", "size_affected": False}, 
    {"code": "x['12323f29-c31f-478c-9b15-e7acc5354df9']","setup": "pass", "iterations": 10000000, "name": "d[key]", "size_affected": False}, 
    {"code": "key in x", "setup": "key = getUuid()","iterations": 20000000, "name": "key in d", "size_affected": False},  
    {"code": "key not in x", "setup": "key = getUuid()","iterations": 20000000, "name": "key not in d", "size_affected": False},  
    {"code": "dumps(x, protocol=-1)", "setup": "from pickle import dumps","iterations": 5000, "name": "pickle.dumps(d)", "size_affected": True},  
    {"code": "loads(dump, buffers=buffers)", "setup": "from pickle import loads, dumps; buffers = []; dump = dumps(x, protocol=-1, buffer_callback=buffers.append)","iterations": 4000, "name": "pickle.loads(dump)", "size_affected": True},  
    {"code": "hash(x)", "setup": "pass","iterations": 10000000, "name": "hash(d)", "size_affected": False},   
    {"code": "len(x)", "setup": "pass","iterations": 20000000, "name": "len(d)", "size_affected": False},  
    {"code": "for _ in keys(): pass", "setup": "keys = x.keys","iterations": 100000, "name": "d.keys()", "size_affected": True},  
    {"code": "for _ in values(): pass", "setup": "values = x.values","iterations": 100000, "name": "d.values()", "size_affected": True},  
    {"code": "for _ in items(): pass", "setup": "items = x.items","iterations": 50000, "name": "d.items()", "size_affected": True},   
    {"code": "for _ in iter(x): pass", "setup": "pass","iterations": 100000, "name": "iter(d)", "size_affected": True}, 
    {"code": "klass(d)", "setup": "klass = type(x)","iterations": 10000, "name": "constructor(dict)", "size_affected": True},
    {"code": "klass(v)", "setup": "klass = type(x); v = tuple(d.items())","iterations": 10000, "name": "constructor(d.items())", "size_affected": True},  
    {"code": "klass(**d)", "setup": "klass = type(x)","iterations": 5000, "name": "constructor(**d)", "size_affected": True},
    {"code": "klass(x)", "setup": "klass = type(x)","iterations": 50000, "name": "constructor(self)", "size_affected": True},
    {"code": "x == d", "setup": "pass","iterations": 100000, "name": "d1 == d2", "size_affected": True},
    {"code": "x == x", "setup": "pass","iterations": 100000, "name": "self == self", "size_affected": True},
    {"code": "repr(x)", "setup": "pass","iterations": 3000, "name": "repr(d)", "size_affected": True},
    {"code": "str(x)", "setup": "pass","iterations": 3000, "name": "str(d)", "size_affected": True},
)

for n in dictionary_sizes:
    print("################################################################################")
    d = dict()

    for i in range(n-1):
        d[getUuid()] = getUuid()

    d['12323f29-c31f-478c-9b15-e7acc5354df9'] = getUuid()

    h = immutables.Map(d)
    fd = frozendict(d)

    for statement in statements:
        print("////////////////////////////////////////////////////////////////////////////////")

        for x in (d, h, fd):
            if statement["name"] == "hash(d)" and type(x) == type({}):
                continue

            if statement["size_affected"]:
                iterations = int(statement["iterations"] * max_size / n)
            else:
                iterations = statement["iterations"]

            t = timeit.timeit(
                stmt = statement["code"], 
                setup = statement["setup"], 
                globals = {"x": x, "getUuid": getUuid, "d": d},
                number = iterations
            )

            print("Dictionary size: {: >4}; Type: {: >10}; Statement: {: <25} time: {:.3f}; iterations: {: >8}".format(
                n, 
                type(x).__name__, 
                "`{}`;".format(statement["name"]), 
                t,
                iterations
            ))
