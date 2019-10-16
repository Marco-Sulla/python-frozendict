import immutables
from frozendict import frozendict
import timeit
import uuid
import copy

dictionary_sizes = (5, 1000, )

def getUuid():
    return str(uuid.uuid4())

statements = (
    {"code": "x.get(key)", "setup": "key = getUuid()", "iterations": 10000000, "name": "d.get(key)"}, 
    {"code": "x['12323f29-c31f-478c-9b15-e7acc5354df9']", "setup": "key = getUuid()", "iterations": 10000000, "name": "d[key]"}, 
    {"code": "key in x", "setup": "key = getUuid()","iterations": 10000000, "name": "key in d"},  
    {"code": "key not in x", "setup": "key = getUuid()","iterations": 10000000, "name": "key not in d"},  
    {"code": "pickle.loads(pickle.dumps(x))", "setup": "import pickle","iterations": 1000, "name": "pickle"},  
    {"code": "hash(x)", "setup": "pass","iterations": 10000000, "name": "hash(d)"},   
    {"code": "len(x)", "setup": "pass","iterations": 10000000, "name": "len(d)"},  
    {"code": "for _ in x.keys(): pass", "setup": "pass","iterations": 100000, "name": "d.keys()"},  
    {"code": "for _ in x.values(): pass", "setup": "pass","iterations": 100000, "name": "d.values()"},  
    {"code": "for _ in x.items(): pass", "setup": "pass","iterations": 100000, "name": "d.items()"},   
    {"code": "for _ in iter(x): pass", "setup": "pass","iterations": 100000, "name": "iter(d)"}, 
    {"code": "klass(d)", "setup": "klass = type(x)","iterations": 10000, "name": "constructor(dict)"},
    {"code": "klass(v)", "setup": "klass = type(x); v = tuple(d.items())","iterations": 10000, "name": "constructor(tuple(d.items()))"},  
    {"code": "klass(**d)", "setup": "klass = type(x)","iterations": 10000, "name": "constructor(**d)"},
    {"code": "klass(x)", "setup": "klass = type(x)","iterations": 100000, "name": "constructor(self)"},
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

            t = timeit.Timer(
                stmt=statement["code"], 
                setup=statement["setup"], 
                globals={"x": x, "getUuid": getUuid, "d": d}
            ).timeit(number=statement["iterations"])

            print("Dictionary size: {}; Type: {}; Statement: `{}`; time: {}".format(n, type(x).__name__, statement["name"], t))
