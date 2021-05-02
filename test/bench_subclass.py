#!/usr/bin/env python3

try:
    frozendict
    print("builtin")
except NameError:
    from frozendict import coold

class F(coold):
    def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

frozendict = F

def main(number):
    import timeit
    import uuid
    from time import time
    from math import sqrt
    
    def mindev(data, xbar = None):
        if not data:
            raise ValueError("No data")
        
        if xbar == None:
            xbar = min(data)
        
        sigma2 = 0
        
        for x in data:
            sigma2 += (x - xbar) ** 2
        
        N = len(data) - 1
        
        if N < 1:
            N = 1
        
        return sqrt(sigma2 / N)
    
    def autorange(stmt, setup="pass", globals=None, ratio=1000, bench_time=10, number=None):
        if setup == None:
            setup = "pass"
        
        t = timeit.Timer(stmt=stmt, setup=setup, globals=globals)
        break_immediately = False
        
        if number == None:
            a = t.autorange()
            
            num = a[0]
            number = int(num / ratio)
            
            if number < 1:
                number = 1
            
            repeat = int(num / number)
            
            if repeat < 1:
                repeat = 1
        
        else:
            repeat = 1
            break_immediately = True
        
        results = []
        
        data_tmp = t.repeat(number=number, repeat=repeat)
        min_value = min(data_tmp)
        data_min = [min_value]
        
        bench_start = time()
        
        while 1:
            data_min.extend(t.repeat(number=number, repeat=repeat))
            
            if break_immediately or time() - bench_start > bench_time:
                break
        
        data_min.sort()
        xbar = data_min[0]
        i = 0
        
        while i < len(data_min):
            i = len(data_min)
            sigma = mindev(data_min, xbar=xbar)
            
            for i in range(2, len(data_min)):
                if data_min[i] - xbar > 3 * sigma:
                    break
            
            k = i
            
            if i < 5:
                k = 5
            
            del data_min[k:]
        
        return (min(data_min) / number, mindev(data_min, xbar=xbar) / number)
    
    
    def getUuid():
        return str(uuid.uuid4())
    
    
    dictionary_sizes = (5, 1000)
    
    print_tpl = "Name: {name: <25} Size: {size: >4}; Keys: {keys: >3}; Type: {type: >10}; Time: {time:.2e}; Sigma: {sigma:.0e}"
    str_key = '12323f29-c31f-478c-9b15-e7acc5354df9'
    int_key = dictionary_sizes[0] - 2
    
    if int_key < 0:
        int_key = 0

    benchmarks = (
        {"name": "constructor(d)", "code": "klass(d)", "setup": "klass = type(o)", },
        {"name": "constructor(kwargs)", "code": "klass(**d)", "setup": "klass = type(o)", },
        {"name": "constructor(seq2)", "code": "klass(v)", "setup": "klass = type(o); v = tuple(d.items())", },  
        {"name": "constructor(o)", "code": "klass(o)", "setup": "klass = type(o)", },
        {"name": "o.copy()", "code": "o.copy()", "setup": "pass", },
        {"name": "o == o", "code": "o == o", "setup": "pass", }, 
        {"name": "for x in o", "code": "for _ in o: pass", "setup": "pass", },
        {"name": "for x in o.values()", "code": "for _ in values: pass", "setup": "values = o.values()", },  
        {"name": "for x in o.items()", "code": "for _ in items: pass", "setup": "items = o.items()", }, 
        {"name": "pickle.dumps(o)", "code": "dumps(o, protocol=-1)", "setup": "from pickle import dumps", },  
        {"name": "pickle.loads(dump)", "code": "loads(dump)", "setup": "from pickle import loads, dumps; dump = dumps(o, protocol=-1)", },  
        {"name": "class.fromkeys()", "code": "fromkeys(keys)", "setup": "fromkeys = type(o).fromkeys; keys = o.keys()", },  
        {"name": "for x in o.keys()", "code": "for _ in keys: pass", "setup": "keys = o.keys()", },   
        {"name": "for x in iter(o)", "code": "for _ in iter(o): pass", "setup": "pass", }, 
        {"name": "o == d", "code": "o == d", "setup": "pass", },
        {"name": "o.get(key)", "code": "get(key)", "setup": "key = getUuid(); get = o.get", }, 
        {"name": "o[key]", "code": "o[one_key]","setup": "pass", }, 
        {"name": "key in o", "code": "key in o", "setup": "key = getUuid()", },
        {"name": "key not in o", "code": "key not in o", "setup": "key = getUuid()", },
        {"name": "hash(o)", "code": "hash(o)", "setup": "pass", },   
        {"name": "len(o)", "code": "len(o)", "setup": "pass", },  
        {"name": "o.keys()", "code": "keys()", "setup": "keys = o.keys", },  
        {"name": "o.values()", "code": "values()", "setup": "values = o.values", },  
        {"name": "o.items()", "code": "items()", "setup": "items = o.items", },   
        {"name": "iter(o)", "code": "iter(o)", "setup": "pass", }, 
        {"name": "repr(o)", "code": "repr(o)", "setup": "pass", },
        {"name": "str(o)", "code": "str(o)", "setup": "pass", },
        {"name": "set", "code": None, "setup": "val = getUuid()", },
    )
    
    dict_collection = []
    
    for n in dictionary_sizes:
        d1 = {}
        d2 = {}

        for i in range(n-1):
            d1[getUuid()] = getUuid()
            d2[i] = i
        
        d1[str_key] = getUuid()
        d2[999] = 999

        fd1 = frozendict(d1)
        fd2 = frozendict(d2)
        
        dict_collection.append({"str": ((d1, fd1), str_key), "int": ((d2, fd2), int_key)})
        
    for benchmark in benchmarks:
        print("################################################################################")
        
        for dict_collection_entry in dict_collection:
            for (dict_keys, (dicts, one_key)) in dict_collection_entry.items():
        
                if benchmark["name"] == "constructor(kwargs)" and dict_keys == "int":
                    continue

                print("////////////////////////////////////////////////////////////////////////////////")
                
                for o in dicts:
                    if benchmark["name"] == "hash(o)" and type(o) == dict:
                        continue
                    
                    if benchmark["name"] == "set":
                        if type(o) == dict:
                            benchmark["code"] = "o[one_key] = val"
                        else:
                            benchmark["code"] = "o.set(one_key, val)"

                    d = dicts[0]
                    
                    bench_res = autorange(
                        stmt = benchmark["code"], 
                        setup = benchmark["setup"], 
                        globals = {"o": o.copy(), "getUuid": getUuid, "d": d.copy(), "one_key": one_key},
                        number = number, 
                    )

                    print(print_tpl.format(
                        name = "`{}`;".format(benchmark["name"]), 
                        keys = dict_keys, 
                        size = len(o), 
                        type = type(o).__name__, 
                        time = bench_res[0],
                        sigma = bench_res[1],  
                    ))
    
    print("################################################################################")

if __name__ == "__main__":
    import sys

    number = None
    argv = sys.argv
    len_argv = len(argv)
    max_positional_args = 1
    max_len_argv = max_positional_args + 1
    
    if len_argv > max_len_argv:
        raise ValueError(
            ("{name} must not accept more than {nargs} positional " + 
            "command-line parameters").format(name=__name__, nargs=max_positional_args)
        )
    
    number_arg_pos = 1
    
    if len_argv == number_arg_pos + 1:
        number = int(argv[number_arg_pos])
    
    main(number)
