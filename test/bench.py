#!/usr/bin/env python3

import timeit
import uuid
from copy import copy
from time import time

import immutables
from frozendict import frozendict
from math import sqrt


def mindev(data, xbar=None):
    """
    This function calculates the stdev around the _minimum_ data,
    and not the mean
    """
    
    if not data:
        raise ValueError("No data")
    
    if xbar is None:
        xbar = min(data)
    
    sigma2 = 0
    
    for x in data:
        sigma2 += (x - xbar) ** 2
    
    N = len(data) - 1
    
    if N < 1:
        N = 1
    
    return sqrt(sigma2 / N)


def autorange(
    stmt,
    setup="pass",
    globals=None,
    ratio=1000,
    bench_time=10,
    number=None
):
    if setup is None:
        setup = "pass"
    
    t = timeit.Timer(stmt=stmt, setup=setup, globals=globals)
    break_immediately = False
    
    if number is None:
        # get automatically the number of needed loops
        a = t.autorange()
        
        number_temp = a[0]
        # the number of loops
        number = int(number_temp / ratio)
        
        if number < 1:
            number = 1
        
        # the number of repeat of loops
        repeat = int(number_temp / number)
        
        if repeat < 1:
            repeat = 1
    
    else:
        repeat = 1
        break_immediately = True
    
    data_tmp = t.repeat(number=number, repeat=repeat)
    min_value = min(data_tmp)
    # create a list with minimum values
    data_min = [min_value]
    
    bench_start = time()
    
    while 1:
        # get additional benchs until `bench_time` seconds passes
        data_min.extend(t.repeat(number=number, repeat=repeat))
        
        if break_immediately or time() - bench_start > bench_time:
            break
    
    # sort the data...
    data_min.sort()
    # ... so the minimum is the fist datum
    xbar = data_min[0]
    i = 0
    
    # repeat until no data is removed
    while i < len(data_min):
        i = len(data_min)
        
        # calculate the sigma using the minimum as "real" value,
        # and not the mean
        sigma = mindev(data_min, xbar=xbar)
        
        for i2 in range(2, len(data_min)):
            # find the point where the data are greater than
            # 3 sigma. Data are sorted
            if data_min[i2] - xbar > 3 * sigma:
                break
        
        k = i
        
        # do not remove too much data
        if i < 5:
            k = 5
        
        # remove the data with sigma > 3
        del data_min[k:]
    
    # return the minimum as real value, with the sigma
    # calculated around the minimum
    return (
        min(data_min) / number,
        mindev(data_min, xbar=xbar) / number
    )


def getUuid():
    return str(uuid.uuid4())


def main(number):
    dictionary_sizes = (5, 1000)
    
    print_tpl = (
        "Name: {name: <25} Size: {size: >4}; Keys: {keys: >3}; " +
        "Type: {type: >10}; Time: {time:.2e}; Sigma: {sigma:.0e}"
    )
    
    str_key = '12323f29-c31f-478c-9b15-e7acc5354df9'
    int_key = dictionary_sizes[0] - 2
    
    if int_key < 0:
        int_key = 0
    
    bench_constr_kwargs_name = "constructor(kwargs)"
    bench_hash_name = "hash"
    bench_set_name = "set"
    bench_delete_name = "set"
    bench_copy_name = "copy"
    bench_fromkeys_name = "fromkeys"
    
    benchmarks = (
        {
            "name": "constructor(d)", 
            "code": "klass(d)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": bench_constr_kwargs_name,
            "code": "klass(**d)", 
            "setup": "klass = type(o)", 
        },
        {
            "name": "constructor(seq2)", 
            "code": "klass(v)", 
            "setup": "klass = type(o); v = tuple(d.items())", 
        },
        {
            "name": "constructor(o)", 
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
            "name": "for x in o", 
            "code": "for _ in o: pass", 
            "setup": "pass", 
        },
        {
            "name": "for x in o.values()", 
            "code": "for _ in values: pass", 
            "setup": "values = o.values()", 
        },
        {
            "name": "for x in o.items()", 
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
        m1 = immutables.Map(d1)
        m2 = immutables.Map(d2)
        
        dict_collection.append({
            "str": ((d1, fd1, m1), str_key),
            "int": ((d2, fd2, m2), int_key)
        })
    
    sep_n = 72
    sep_major = "#"
    
    for benchmark in benchmarks:
        print(sep_major * sep_n)
        
        for dict_entry in dict_collection:
            for (dict_keys, (dicts, one_key)) in dict_entry.items():
        
                if (
                    benchmark["name"] == bench_constr_kwargs_name and
                    dict_keys == "int"
                ):
                    continue

                print("/" * sep_n)
                
                for o in dicts:
                    if (
                        benchmark["name"] == bench_hash_name and
                        type(o) is dict
                    ):
                        continue
                    
                    if benchmark["name"] == bench_set_name:
                        if type(o) is dict:
                            benchmark["code"] = (
                                "o.copy()[one_key] = val"
                            )
                        else:
                            benchmark["code"] = "o.set(one_key, val)"
                    
                    if benchmark["name"] == bench_delete_name:
                        if type(o) is dict:
                            benchmark["code"] = "del o.copy()[one_key]"
                        else:
                            benchmark["code"] = "o.delete(one_key)"
                    
                    if benchmark["name"] == bench_copy_name:
                        if type(o) is immutables.Map:
                            benchmark["code"] = "copy(o)"
                        else:
                            benchmark["code"] = "o.copy()"
                    
                    if (
                        benchmark["name"] == bench_fromkeys_name and 
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
                        name = "`{}`;".format(benchmark["name"]), 
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
