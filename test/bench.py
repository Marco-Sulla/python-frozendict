#!/usr/bin/env python3

import timeit
import uuid
from copy import copy
from statistics import stdev, StatisticsError, median, mean
from time import time

import immutables
from frozendict import frozendict


def autorange(
    stmt,
    setup="pass",
    globals=None,
    bench_time=100,
    number=None
):
    if setup is None:
        setup = "pass"
    
    t = timeit.Timer(stmt=stmt, setup=setup, globals=globals)
    break_immediately = False
    
    if number is None:
        # get automatically the number of needed loops
        a = t.autorange()
        number = a[0]
        
        if number < 1:
            number = 1
        
        repeat = 5
    
    else:
        repeat = 1
        break_immediately = True
    
    data = t.repeat(number=number, repeat=repeat)
    xbar = min(data)
    
    bench_start = time()
    
    while not break_immediately:
        if time() - bench_start > bench_time:
            break
        
        # get additional benchs until `bench_time` seconds passes
        data.extend(t.repeat(number=number, repeat=repeat))
    
        # sort the data...
        data.sort()
        # ... so the minimum is the fist datum
        xbar = data[0]
        
        i = 0
        
        # repeat until no data is removed
        while i < len(data):
            i = len(data)
            
            # calculate the sigma using MAD
            avg = mean(data)
            sigma = median([abs(x - avg) for x in data])
            
            for i in range(2, len(data)):
                # find the point where the data are greater than
                # 3 sigma. Data are sorted
                if data[i] - xbar > 3 * sigma:
                    break
            
            # remove the data with sigma > 3
            del data[i:]
    
    sigma = float("nan")
    
    try:
        sigma = stdev(data, xbar=xbar) / number
    except StatisticsError:
        if not break_immediately:
            raise
    
    # return the minimum as real value, with the sigma
    # calculated around the minimum
    return (
        xbar / number,
        sigma
    )


def getUuid():
    return str(uuid.uuid4())


def main(number):
    dictionary_sizes = (5, 1000)
    
    print_tpl = (
        "{name: <12}; Size: {size: >4}; Keys: {keys: >3}; " +
        "Type: {type: >10}; Time: {time:.2e}; σ: {sigma:.0e}"
    )
    
    str_key = '12323f29-c31f-478c-9b15-e7acc5354df9'
    int_key = dictionary_sizes[0] - 2
    
    if int_key < 0:
        int_key = 0
    
    bench_constr_kwargs_name = "init(kwargs)"
    bench_constr_holes_name = "init(holes)"
    bench_hash_name = "hash"
    bench_set_name = "set"
    bench_delete_name = "delete"
    bench_copy_name = "copy"
    bench_fromkeys_name = "fromkeys"
    
    benchmarks = (
        {
            "name": "init(d)", 
            "code": "klass(d)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": bench_constr_kwargs_name,
            "code": "klass(**d)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": "init(seq2)", 
            "code": "klass(v)", 
            "setup": "klass = type(o); v = tuple(d.items())", 
        },
        {
            "name": "init(o)",
            "code": "klass(o)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": bench_constr_holes_name, 
            "code": "klass(o)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": bench_copy_name, 
            "code": None, 
            "setup": "pass", 
        },
        {
            "name": "o == o", 
            "code": "o == o", 
            "setup": "pass", 
        },
        {
            "name": "iter o",
            "code": "for _ in o: pass", 
            "setup": "pass", 
        },
        {
            "name": "iter values",
            "code": "for _ in values: pass", 
            "setup": "values = o.values()", 
        },
        {
            "name": "iter items",
            "code": "for _ in items: pass", 
            "setup": "items = o.items()", 
        },
        {
            "name": "pickle.dumps", 
            "code": "dumps(o, protocol=-1)", 
            "setup": "from pickle import dumps", 
        },
        {
            "name": "pickle.loads", 
            "code": "loads(dump)", 
            "setup": (
                "from pickle import loads, dumps; " +
                "dump = dumps(o, protocol=-1)"
            ),
        },
        {
            "name": bench_fromkeys_name, 
            "code": "fromkeys(keys)", 
            "setup": "fromkeys = type(o).fromkeys; keys = o.keys()", 
        },
        {
            "name": bench_set_name, 
            "code": None, 
            "setup": "val = getUuid()", 
        },
        {
            "name": bench_delete_name, 
            "code": None, 
            "setup": "pass", 
        },
        {
            "name": bench_hash_name,
            "code": "hash(o)",
            "setup": "pass",
        },
    )
    
    dict_collection = []
    holes_suffix = "_holes"
    
    for n in dictionary_sizes:
        d1 = {}
        d2 = {}

        for i in range(n-1):
            d1[getUuid()] = getUuid()
            d2[i] = i
        
        d1[str_key] = getUuid()
        d2[999] = 999
        
        d1_holes = d1.copy()
        d2_holes = d2.copy()
        
        del d1_holes[str_key]
        del d2_holes[999]
        
        d1_holes[str_key] = getUuid()
        d2_holes[999] = 999

        fd1 = frozendict(d1)
        fd2 = frozendict(d2)
        m1 = immutables.Map(d1)
        m2 = immutables.Map(d2)
        
        fd1_holes = frozendict(d1_holes)
        fd2_holes = frozendict(d2_holes)
        m1_holes = immutables.Map(d1_holes)
        m2_holes = immutables.Map(d2_holes)
        
        dict_collection.append({
            "str": ((d1, fd1, m1), str_key),
            "int": ((d2, fd2, m2), int_key),
            f"str{holes_suffix}": ((d1_holes, fd1_holes, m1_holes), str_key),
            f"int{holes_suffix}": ((d2_holes, fd2_holes, m2_holes), int_key),
        })
    
    sep_n = 79
    sep_major = "#"
    
    for benchmark in benchmarks:
        print(sep_major * sep_n)
        bench_name = benchmark["name"]
        is_bench_holes = bench_name == bench_constr_holes_name
        
        for dict_entry in dict_collection:
            for (dict_keys, (dicts, one_key)) in dict_entry.items():
                if dict_keys.endswith(holes_suffix) != is_bench_holes:
                    continue
                
                if is_bench_holes:
                    dict_keys = dict_keys.removesuffix(holes_suffix)
        
                if (
                    bench_name == bench_constr_kwargs_name and
                    dict_keys == "int"
                ):
                    continue

                print("/" * sep_n)
                
                for o in dicts:
                    if (
                        bench_name == bench_hash_name and
                        type(o) is dict
                    ):
                        continue
                    
                    if bench_name == bench_set_name:
                        if type(o) is dict:
                            benchmark["code"] = (
                                "o.copy()[one_key] = val"
                            )
                        else:
                            benchmark["code"] = "o.set(one_key, val)"
                    
                    if bench_name == bench_delete_name:
                        if type(o) is dict:
                            benchmark["code"] = "del o.copy()[one_key]"
                        else:
                            benchmark["code"] = "o.delete(one_key)"
                    
                    if bench_name == bench_copy_name:
                        if type(o) is immutables.Map:
                            benchmark["code"] = "copy(o)"
                        else:
                            benchmark["code"] = "o.copy()"
                    
                    if (
                        bench_name == bench_fromkeys_name and 
                        type(o) is immutables.Map
                    ):
                        continue
                    
                    d = dicts[0]
                    
                    bench_res = autorange(
                        stmt = benchmark["code"], 
                        setup = benchmark["setup"], 
                        globals = {
                            "o": copy(o),
                            "getUuid": getUuid,
                            "d": d.copy(),
                            "one_key": one_key,
                            "copy": copy,
                        },
                        number = number,
                    )

                    print(print_tpl.format(
                        name = bench_name,
                        keys = dict_keys, 
                        size = len(o), 
                        type = type(o).__name__, 
                        time = bench_res[0],
                        sigma = bench_res[1],  
                    ))
    
    print(sep_major * sep_n)


if __name__ == "__main__":
    import sys

    num = None
    argv = sys.argv
    len_argv = len(argv)
    max_positional_args = 1
    max_len_argv = max_positional_args + 1
    
    if len_argv > max_len_argv:
        raise ValueError(
            f"{__name__} must not accept more than " +
            f"{max_positional_args} positional command-line parameters"
        )
    
    number_arg_pos = 1
    
    if len_argv == number_arg_pos + 1:
        num = int(argv[number_arg_pos])
    
    main(num)
