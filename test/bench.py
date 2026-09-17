#!/usr/bin/env python3

import timeit
from copy import copy
from statistics import median
from time import time

import immutables

from frozendict import frozendict


def mad(data, xbar=None):
    if xbar is None:
        xbar = median(data)
    
    return median([abs(x - xbar) for x in data])


def autorange(
    stmt,
    setup="pass",
    globals=None,
    bench_time=5,
    number=None,
    repeat=5,
):
    t = timeit.Timer(stmt=stmt, setup=setup, globals=globals)
    break_bench = False
    
    if number is None:
        # get automatically the number of needed loops
        a = t.autorange()
        number = a[0]
        
        if number < 1:
            number = 1
    else:
        # if number is provided, we will not wait for the `bench_time` seconds
        break_bench = True

    bench_start = time()
    data = t.repeat(number=number, repeat=repeat)
    
    while not break_bench:
        if time() - bench_start > bench_time:
            break

        # get additional benchs until `bench_time` seconds passes
        data.extend(t.repeat(number=number, repeat=repeat))

    # the "true" value is the minimum
    xbar = min(data)
    cv = mad(data) * 100 / median(data)
    
    # return the minimum as real value, with the coefficient of variation
    return (xbar/number, cv)


def get_str_key(n):
    return f"{n:036d}"


def main(number):
    dictionary_sizes = (5, 5000)
    
    print_tpl = (
        "{name: <12}; Size: {size: >4}; Keys: {keys: >3}; " +
        "Type: {type: >10}; Time: {time:.2e}; CV: {cv:.0e}"
    )

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
            "code": "klass(x)",
            "setup": "klass = type(o); x = d",
        },
        {
            "name": bench_constr_kwargs_name,
            "code": "klass(**x)",
            "setup": "klass = type(o); x = d",
        },
        {
            "name": "init(seq2)", 
            "code": "klass(v)", 
            "setup": "klass = type(o); v = tuple(d.items())", 
        },
        {
            "name": "init(o)",
            "code": "klass(x)",
            "setup": "klass = type(o); x = o",
        },
        {
            "name": bench_constr_holes_name,
            "code": "klass(x)",
            "setup": "klass = type(o); x = d",
        },
        {
            "name": bench_copy_name,
            "code": None,
            "setup": None,
        },
        {
            "name": "iter keys",
            "code": "for _ in keys: pass", 
            "setup": "keys = o.keys()", 
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
            "code": "dumps(x, protocol=-1)",
            "setup": "from pickle import dumps; x = o",
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
            "setup": None,
        },
        {
            "name": bench_delete_name, 
            "code": None, 
            "setup": "pass", 
        },
        {
            "name": bench_hash_name,
            "code": "hash_(x)",
            "setup": "hash_ = hash; x = o",
        },
    )
    
    dict_collection = []
    holes_suffix = "_holes"
    
    for n in dictionary_sizes:
        d1 = {}
        d2 = {}

        for i in range(n):
            d1[get_str_key(i)] = get_str_key(i + n)
            d2[i] = i

        str_key = get_str_key(n - 1)
        
        d1_holes = d1.copy()
        d2_holes = d2.copy()

        val_str = d1_holes[str_key]
        del d1_holes[str_key]
        del d2_holes[n - 1]
        
        d1_holes[str_key] = val_str
        d2_holes[n - 1] = n - 1

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
    
    sep_n = 80
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
                                "copy_()[k] = val"
                            )
                            benchmark["setup"] = "copy_ = o.copy; k = one_key; val = 42"
                        else:
                            benchmark["code"] = "set(k, val)"
                            benchmark["setup"] = "set = o.set; k = one_key; val = 42"

                    if bench_name == bench_delete_name:
                        if type(o) is dict:
                            benchmark["code"] = "del copy_()[k]"
                            benchmark["setup"] = "copy_ = o.copy; k = one_key"
                        else:
                            benchmark["code"] = "delete(k)"
                            benchmark["setup"] = "delete = o.delete; k = one_key"
                    
                    if bench_name == bench_copy_name:
                        if type(o) is immutables.Map:
                            benchmark["code"] = "copy_(x)"
                            benchmark["setup"] = "copy_ = copy; x = o"
                        else:
                            benchmark["code"] = "copy_()"
                            benchmark["setup"] = "copy_ = o.copy"
                    
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
                        cv = bench_res[1],
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
