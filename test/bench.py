#!/usr/bin/env python3

import argparse
import timeit
from copy import copy
from random import Random
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


def get_str_key(rng):
    return f"k{rng.getrandbits(128):032x}"


object_types = {
    "dict": dict,
    "fd": frozendict,
    "map": immutables.Map,
}

key_kinds = ("str", "int")


def build_objects(mapping, skip):
    objects = []

    for name, klass in object_types.items():
        if name in skip:
            continue

        objects.append(mapping if klass is dict else klass(mapping))

    return tuple(objects)


bench_constr_kwargs_name = "init(kwargs)"
bench_constr_holes_name = "init(holes)"
bench_hash_name = "hash"
bench_set_name = "set"
bench_delete_name = "delete"
bench_copy_name = "copy"
bench_fromkeys_name = "fromkeys"


def get_benchmarks():
    return (
        {
            "id": "init_d",
            "name": "init(d)",
            "code": "klass(x)",
            "setup": "klass = type(o); x = d",
        },
        {
            "id": "init_kwargs",
            "name": bench_constr_kwargs_name,
            "code": None,
            "setup": "klass = type(o)",
        },
        {
            "id": "init_seq2",
            "name": "init(seq2)", 
            "code": "klass(v)", 
            "setup": "klass = type(o); v = list(d.items())",
        },
        {
            "id": "init_o",
            "name": "init(o)",
            "code": "klass(x)",
            "setup": "klass = type(o); x = o",
        },
        {
            "id": "init_holes",
            "name": bench_constr_holes_name,
            "code": "klass(x)",
            "setup": "klass = type(o); x = d",
        },
        {
            "id": "copy",
            "name": bench_copy_name,
            "code": None,
            "setup": None,
        },
        {
            "id": "iter_keys",
            "name": "iter keys",
            "code": "for _ in keys: pass", 
            "setup": "keys = o.keys()", 
        },
        {
            "id": "iter_values",
            "name": "iter values",
            "code": "for _ in values: pass", 
            "setup": "values = o.values()", 
        },
        {
            "id": "iter_items",
            "name": "iter items",
            "code": "for _ in items: pass", 
            "setup": "items = o.items()", 
        },
        {
            "id": "dumps",
            "name": "pickle.dumps", 
            "code": "dumps(x, protocol=-1)",
            "setup": "from pickle import dumps; x = o",
        },
        {
            "id": "loads",
            "name": "pickle.loads", 
            "code": "loads(dump)", 
            "setup": (
                "from pickle import loads, dumps; " +
                "dump = dumps(o, protocol=-1)"
            ),
        },
        {
            "id": "fromkeys",
            "name": bench_fromkeys_name, 
            "code": "fromkeys(keys)", 
            "setup": "fromkeys = type(o).fromkeys; keys = o.keys()", 
        },
        {
            "id": "set",
            "name": bench_set_name,
            "code": None,
            "setup": None,
        },
        {
            "id": "delete",
            "name": bench_delete_name,
            "code": None, 
            "setup": "pass", 
        },
        {
            "id": "hash",
            "name": bench_hash_name,
            "code": "hash_(x)",
            "setup": "hash_ = hash; x = o",
        },
    )


def main(number, skip, keys, sizes, run, seed):
    dictionary_sizes = sizes
    print()
    sep_n = 80
    sep_major = "#"
    print(sep_major * sep_n)
    print(f"Seed: {seed}", flush=True)
    
    # seeded, so the keys are the same at every run with the same seed
    rng = Random(seed)

    print_tpl = (
        "{name: <12}; Size: {size: >4}; Keys: {keys: >3}; " +
        "Type: {type: >10}; Time: {time:.2e}; CV: {cv:.0e}"
    )
    
    benchmarks = get_benchmarks()
    
    dict_collection = []
    holes_suffix = "_holes"
    
    for n in dictionary_sizes:
        dict_entry = {}

        if "str" in keys:
            d1 = {}

            for i in range(n):
                str_key = get_str_key(rng)
                d1[str_key] = get_str_key(rng)

            d1_holes = d1.copy()
            del d1_holes[str_key]

            dict_entry["str"] = (d1, build_objects(d1, skip), str_key)
            dict_entry[f"str{holes_suffix}"] = (
                d1_holes, build_objects(d1_holes, skip), str_key
            )

        if "int" in keys:
            # seed 0 keeps the old keys, so the results stay comparable
            if seed == 0:
                int_keys = range(n)
            else:
                # one 30 bit digit, like small ints; already in random order
                int_keys = rng.sample(range(1 << 30), n)

            d2 = {}

            for int_key in int_keys:
                d2[int_key] = int_key

            d2_holes = d2.copy()
            del d2_holes[int_key]

            dict_entry["int"] = (d2, build_objects(d2, skip), int_key)
            dict_entry[f"int{holes_suffix}"] = (
                d2_holes, build_objects(d2_holes, skip), int_key
            )

        dict_collection.append(dict_entry)

    for benchmark in benchmarks:
        if benchmark["id"] not in run:
            continue

        print(sep_major * sep_n)
        bench_name = benchmark["name"]
        is_bench_holes = bench_name == bench_constr_holes_name
        
        for dict_entry in dict_collection:
            for (dict_keys, (source, dicts, one_key)) in dict_entry.items():
                if not dicts:
                    continue

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
                            benchmark["code"] = "set_(k, val)"
                            benchmark["setup"] = "set_ = o.set; k = one_key; val = 42"

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
                    
                    d = source

                    if bench_name == bench_constr_kwargs_name:
                        kwargs = ", ".join(f"{e[0]}={e[1]!r}" for e in d.items())
                        benchmark["code"] = f'klass({kwargs})'

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
    print()


def positive_int(text):
    value = int(text)

    if value < 1:
        raise ValueError(f"{text!r} is not a positive integer")

    return value


def comma_separated(choices=None, cast=str):
    """An argparse type for `a,b,c`, checked against `choices` if given."""
    def parse(text):
        values = tuple(v.strip() for v in text.split(",") if v.strip())

        if not values:
            raise argparse.ArgumentTypeError("the list is empty")

        if choices is not None:
            allowed = ", ".join(repr(c) for c in choices)

            for value in values:
                if value not in choices:
                    raise argparse.ArgumentTypeError(
                        f"invalid choice: {value!r} (choose from {allowed})"
                    )

            return values

        try:
            return tuple(cast(value) for value in values)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e)) from None

    return parse


def parse_args():
    benchmark_ids = tuple(b["id"] for b in get_benchmarks())

    parser = argparse.ArgumentParser(
        description="Benchmark dict against frozendict and immutables.Map."
    )

    parser.add_argument(
        "number",
        nargs = "?",
        type = positive_int,
        default = None,
        help = "loops per measurement. Without it the number is calibrated automatically",
    )

    parser.add_argument(
        "--skip",
        type = comma_separated(object_types),
        default = (),
        metavar = "TYPE[,TYPE...]",
        help = f"object types to leave out: {', '.join(object_types)}",
    )

    parser.add_argument(
        "--keys",
        type = comma_separated(key_kinds),
        default = key_kinds,
        metavar = "KIND[,KIND...]",
        help = f"key kinds to benchmark: {', '.join(key_kinds)} "
               "(default: all of 'em)",
    )

    parser.add_argument(
        "--sizes",
        type = comma_separated(cast=positive_int),
        default = (5, 5000),
        metavar = "N[,N...]",
        help = "dictionary sizes to benchmark",
    )

    parser.add_argument(
        "--run",
        type = comma_separated(benchmark_ids),
        default = benchmark_ids,
        metavar = "ID[,ID...]",
        help = f"benchmarks to run, by id: {', '.join(benchmark_ids)}",
    )

    parser.add_argument(
        "--seed",
        type = int,
        default = 0,
        help = "seed for the keys. With 0, the int keys are 0..n-1",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(**vars(parse_args()))
