#!/usr/bin/env python3
from typing import Callable, Union

import frozendict

assert frozendict.c_ext

from frozendict import frozendict
from uuid import UUID
import pickle
from copy import copy, deepcopy
from collections.abc import MutableMapping
import tracemalloc
import gc
import sys
from random import Random
import argparse
import functools


parser = argparse.ArgumentParser()
parser.add_argument(
    "--seed",
    type=int,
    help="shuffle the functions and generate the keys with this seed"
)
args = parser.parse_args()

# seeded, so the keys are the same at every run with the same seed
rng = Random(args.seed)


def getUuid():
    return str(UUID(int=rng.getrandbits(128)))


class F(frozendict):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)


class FMissing(frozendict):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)
    
    def __missing__(self, key):
        return key


class Map(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]
    
    def __iter__(self):
        return iter(self._dict)
    
    def __len__(self):
        return len(self._dict)


def print_info(klass, iterations, func: Union[Callable, str]):
    try:
        name = func.__name__
    except AttributeError:
        name = func
    
    print(
        (
            f"Class = {klass.__name__} - Loops: {iterations} - " +
            f"Evaluating: {name}"
        ),
        flush=True
    )


def print_sep():
    print("-" * 72, flush=True)


def trace(iterations = 100, mult = 10.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            header1 = (
                f"Loops: {iterations} - Multiplier: {mult} " +
                f"Evaluating: {func.__name__}"
            )
            
            err = False

            for i in range(7):
                print(header1, flush=True)
                
                tracemalloc.start()
                
                gc.collect()
                
                snapshot1 = tracemalloc.take_snapshot().filter_traces(
                    (tracemalloc.Filter(True, __file__),)
                )
                
                for j in range(iterations):
                    func()
                
                gc.collect()
                
                snapshot2 = tracemalloc.take_snapshot().filter_traces(
                    (tracemalloc.Filter(True, __file__),)
                )
                
                top_stats = snapshot2.compare_to(snapshot1, 'lineno')
                tracemalloc.stop()
                err = False
                
                for stat in top_stats:
                    if stat.count_diff * mult > iterations:
                        header = (
                            f"Error. count diff: {stat.count_diff}, " +
                            f"stat: {stat}"
                        )
                        
                        print(header, flush=True)
                        err = True
                
                if not err:
                    break
            
            if err:
                sys.exit(1)
            
        return wrapper
    
    return decorator


key_in = getUuid()
dict_1 = {key_in: 0}
dict_tmp = {getUuid(): i for i in range(1, 1000)}
dict_1.update(dict_tmp)
key_notin = getUuid()
dict_2 = {getUuid(): i for i in range(1000)}
dict_3 = {i: i for i in range(1000)}
dict_hole = dict_1.copy()
del dict_hole[key_in]
dict_unashable = dict_1.copy()
unashable_key = getUuid()
dict_unashable.update({unashable_key: []})
dict_1_items = tuple(dict_1.items())
dict_1_keys = tuple(dict_1.keys())
dict_1_keys_set = set(dict_1_keys)

functions = []


def get_generator_1():
    return ((key, val) for key, val in dict_1.items())


@trace(mult = 1.4)
def loads_fd():
    pickle.loads(pickle.dumps(fd_1))


functions.append(loads_fd)


@trace(mult = 1.4)
def loads_iter_keys():
    pickle.loads(pickle.dumps(iter(fd_1.keys())))


functions.append(loads_iter_keys)


@trace(mult = 1.4)
def loads_iter_items():
    pickle.loads(pickle.dumps(iter(fd_1.items())))


functions.append(loads_iter_items)


@trace(mult = 1.4)
def loads_iter_values():
    pickle.loads(pickle.dumps(iter(fd_1.values())))


functions.append(loads_iter_values)


@trace()
def constr_empty_dict():
    frozendict_class({})


functions.append(constr_empty_dict)


@trace()
def constr_empty_list():
    frozendict_class([])


functions.append(constr_empty_list)


@trace()
def constr_empty_kwargs():
    frozendict_class({}, **{})


functions.append(constr_empty_kwargs)


@trace()
def constr_kwargs():
    frozendict_class(**dict_1)


functions.append(constr_kwargs)


@trace()
def constr_dict_kwargs():
    frozendict_class(dict_1, **dict_2)


functions.append(constr_dict_kwargs)


@trace()
def constr_fd():
    frozendict_class(fd_1)


functions.append(constr_fd)


@trace()
def constr_gen():
    frozendict_class(get_generator_1())


functions.append(constr_gen)


@trace()
def constr_hole():
    frozendict_class(dict_hole)


functions.append(constr_hole)


@trace()
def copy_method():
    fd_1.copy()


functions.append(copy_method)


@trace()
def eq_dict():
    # noinspection PyStatementEffect
    fd_1 == dict_1


functions.append(eq_dict)


@trace()
def eq_fd():
    # noinspection PyStatementEffect
    fd_1 == fd_1


functions.append(eq_fd)


@trace()
def neq_dict2():
    # noinspection PyStatementEffect
    fd_1 != dict_2


functions.append(neq_dict2)


@trace()
def eq_hole():
    # noinspection PyStatementEffect
    fd_1 == dict_hole


functions.append(eq_hole)


@trace()
def eq_dict2():
    # noinspection PyStatementEffect
    fd_1 == dict_2


functions.append(eq_dict2)


@trace()
def constr_dict():
    frozendict_class(dict_1)


functions.append(constr_dict)


@trace()
def constr_items():
    frozendict_class(dict_1_items)


functions.append(constr_items)


@trace()
def materialize_keys():
    list(fd_1.keys())


functions.append(materialize_keys)


@trace()
def materialize_values():
    list(fd_1.values())


functions.append(materialize_values)


@trace()
def materialize_items():
    list(fd_1.items())


functions.append(materialize_items)


@trace()
def fromkeys_dict():
    frozendict_class.fromkeys(dict_1)


functions.append(fromkeys_dict)


@trace()
def fromkeys_dict_val():
    frozendict_class.fromkeys(dict_1, 1)


functions.append(fromkeys_dict_val)


@trace()
def fromkeys_keys():
    frozendict_class.fromkeys(dict_1_keys)


functions.append(fromkeys_keys)


@trace()
def fromkeys_keys_val():
    frozendict_class.fromkeys(dict_1_keys, 1)


functions.append(fromkeys_keys_val)


@trace()
def fromkeys_set():
    frozendict_class.fromkeys(dict_1_keys_set)


functions.append(fromkeys_set)


@trace()
def fromkeys_set_val():
    frozendict_class.fromkeys(dict_1_keys_set, 1)


functions.append(fromkeys_set_val)


@trace()
def repr_fd():
    repr(fd_1)


functions.append(repr_fd)


@trace()
def or_dict():
    fd_1 | dict_2


functions.append(or_dict)


@trace()
def hash_fd():
    hash(fd_1)


functions.append(hash_fd)


@trace()
def eq_empty():
    # noinspection PyStatementEffect
    frozendict_class() == frozendict_class()


functions.append(eq_empty)


@trace()
def reversed_fd():
    list(reversed(fd_1))


functions.append(reversed_fd)


@trace()
def reversed_keys():
    list(reversed(fd_1.keys()))


functions.append(reversed_keys)


@trace()
def reversed_items():
    list(reversed(fd_1.items()))


functions.append(reversed_items)


@trace()
def reversed_values():
    list(reversed(fd_1.values()))


functions.append(reversed_values)


@trace()
def length_hint():
    iter(fd_1).__length_hint__()


functions.append(length_hint)


@trace()
def len_fd():
    len(fd_1)


functions.append(len_fd)


@trace()
def len_keys():
    len(fd_1.keys())


functions.append(len_keys)


@trace()
def len_items():
    len(fd_1.items())


functions.append(len_items)


@trace()
def len_values():
    len(fd_1.values())


functions.append(len_values)


@trace()
def mapping_keys():
    # noinspection PyStatementEffect,PyUnresolvedReferences
    fd_1.keys().mapping == fd_1


functions.append(mapping_keys)


@trace()
def mapping_items():
    # noinspection PyStatementEffect, PyUnresolvedReferences
    fd_1.items().mapping == fd_1


functions.append(mapping_items)


@trace()
def mapping_values():
    # noinspection PyStatementEffect, PyUnresolvedReferences
    fd_1.values().mapping == fd_1


functions.append(mapping_values)


@trace()
def getitem():
    # noinspection PyStatementEffect
    fd_1[key_in]


functions.append(getitem)


@trace()
def get_in():
    fd_1.get(key_in)


functions.append(get_in)


@trace()
def get_notin():
    fd_1.get(key_notin)


functions.append(get_notin)


@trace()
def get_notin_default():
    fd_1.get(key_notin, 1)


functions.append(get_notin_default)


@trace()
def contains_in():
    # noinspection PyStatementEffect
    key_in in fd_1


functions.append(contains_in)


@trace()
def contains_notin():
    # noinspection PyStatementEffect
    key_notin in fd_1


functions.append(contains_notin)


@trace()
def copy_fd():
    copy(fd_1)


functions.append(copy_fd)


@trace()
def deepcopy_fd():
    deepcopy(fd_1)


functions.append(deepcopy_fd)


@trace()
def deepcopy_recursive():
    deepcopy(fd_recursive)


functions.append(deepcopy_recursive)


@trace()
def eq_keys():
    # noinspection PyStatementEffect
    fd_1.keys() == dict_1.keys()


functions.append(eq_keys)


@trace()
def eq_items():
    # noinspection PyStatementEffect
    fd_1.items() == dict_1.items()


functions.append(eq_items)


@trace()
def contains_keys_notin():
    # noinspection PyStatementEffect
    key_notin in fd_1.keys()


functions.append(contains_keys_notin)


@trace()
def contains_items_notin():
    # noinspection PyStatementEffect
    (key_notin, 0) in fd_1.items()


functions.append(contains_items_notin)


@trace()
def missing():
    # noinspection PyStatementEffect
    FMissing(fd_1)[0]


functions.append(missing)


@trace()
def constr_map():
    mp = Map(dict_1)
    # noinspection PyStatementEffect
    frozendict_class(mp) == dict_1


functions.append(constr_map)


@trace()
def isdisjoint_keys():
    fd_1.keys().isdisjoint(dict_3)


functions.append(isdisjoint_keys)


@trace()
def isdisjoint_keys_self():
    fd_1.keys().isdisjoint(fd_1)


functions.append(isdisjoint_keys_self)


@trace()
def isdisjoint_items():
    fd_1.items().isdisjoint(dict_3.items())


functions.append(isdisjoint_items)


@trace()
def isdisjoint_items_self():
    fd_1.items().isdisjoint(fd_1.items())


functions.append(isdisjoint_items_self)


@trace()
def sub_keys():
    fd_unashable.keys() - fd_1.keys()


functions.append(sub_keys)


@trace()
def sub_items():
    fd_1.items() - frozendict_class(dict_hole).items()


functions.append(sub_items)


@trace()
def and_keys():
    fd_1.keys() & frozendict_class(dict_hole).keys()


functions.append(and_keys)


@trace()
def and_items():
    fd_1.items() & frozendict_class(dict_hole).items()


functions.append(and_items)


@trace()
def or_keys():
    fd_1.keys() | frozendict_class(dict_2).keys()


functions.append(or_keys)


@trace()
def or_items():
    fd_1.items() | frozendict_class(dict_2).items()


functions.append(or_items)


@trace()
def xor_keys():
    fd_1.keys() ^ frozendict_class(dict_hole).keys()


functions.append(xor_keys)


@trace()
def xor_items():
    fd_1.items() ^ frozendict_class(dict_hole).items()


functions.append(xor_items)


@trace()
def constr_unhashable():
    frozendict_class(dict_unashable)


functions.append(constr_unhashable)


@trace()
def constr_int_keys():
    frozendict_class(dict_3)


functions.append(constr_int_keys)


@trace()
def constr_empty():
    frozendict_class()


functions.append(constr_empty)


@trace()
def lt_keys():
    # noinspection PyStatementEffect
    frozendict_class(dict_hole).keys() < fd_1.keys()


functions.append(lt_keys)


@trace()
def le_keys():
    # noinspection PyStatementEffect
    frozendict_class(dict_hole).keys() <= fd_1.keys()


functions.append(le_keys)


@trace()
def lt_items():
    # noinspection PyStatementEffect
    frozendict_class(dict_hole).items() < fd_1.items()


functions.append(lt_items)


@trace()
def gt_keys():
    # noinspection PyStatementEffect
    fd_1.keys() > frozendict_class(dict_hole).keys()


functions.append(gt_keys)


@trace()
def ge_keys():
    # noinspection PyStatementEffect
    fd_1.keys() >= frozendict_class(dict_hole).keys()


functions.append(ge_keys)


@trace()
def gt_items():
    # noinspection PyStatementEffect
    fd_1.items() > frozendict_class(dict_hole).items()


functions.append(gt_items)


@trace()
def ge_items():
    # noinspection PyStatementEffect
    fd_1.items() >= frozendict_class(dict_hole).items()


functions.append(ge_items)


@trace()
def set_in():
    fd_1.set(key_in, 1000)


functions.append(set_in)


@trace()
def set_notin():
    fd_1.set(key_notin, 1000)


functions.append(set_notin)


@trace()
def delete():
    fd_1.delete(key_in)


functions.append(delete)


@trace()
def setdefault_in():
    fd_1.setdefault(key_in)


functions.append(setdefault_in)


@trace()
def setdefault_notin():
    fd_1.setdefault(key_notin)


functions.append(setdefault_notin)


@trace()
def setdefault_notin_default():
    fd_1.setdefault(key_notin, 1000)


functions.append(setdefault_notin_default)


@trace()
def key_noarg():
    fd_1.key()


functions.append(key_noarg)


@trace()
def key_0():
    fd_1.key(0)


functions.append(key_0)


@trace()
def key_neg():
    fd_1.key(-1)


functions.append(key_neg)


@trace()
def value_noarg():
    fd_1.value()


functions.append(value_noarg)


@trace()
def value_0():
    fd_1.value(0)


functions.append(value_0)


@trace()
def value_neg():
    fd_1.value(-1)


functions.append(value_neg)


@trace()
def item_noarg():
    fd_1.item()


functions.append(item_noarg)


@trace()
def item_0():
    fd_1.item(0)


functions.append(item_0)


@trace()
def item_neg():
    fd_1.item(-1)


functions.append(item_neg)


@trace()
def for_fd():
    for _ in fd_1:
        pass


functions.append(for_fd)


@trace()
def for_iter():
    for _ in iter(fd_1):
        pass


functions.append(for_iter)


@trace()
def for_keys():
    for _ in fd_1.keys():
        pass


functions.append(for_keys)


@trace()
def for_values():
    for _ in fd_1.values():
        pass


functions.append(for_values)


@trace()
def for_items():
    for _ in fd_1.items():
        pass


functions.append(for_items)


@trace()
def hash_unhashable():
    try:
        hash(fd_unashable)
    except TypeError:
        pass


functions.append(hash_unhashable)


@trace()
def getitem_notin():
    try:
        fd_1[key_notin]
    except KeyError:
        pass


functions.append(getitem_notin)


@trace()
def key_oob():
    try:
        fd_1.key(len(fd_1))
    except IndexError:
        pass


functions.append(key_oob)


@trace()
def value_oob():
    try:
        fd_1.value(len(fd_1))
    except IndexError:
        pass


functions.append(value_oob)


@trace()
def item_oob():
    try:
        fd_1.item(len(fd_1))
    except IndexError:
        pass


functions.append(item_oob)


@trace()
def fromkeys_empty():
    frozendict_class.fromkeys({})


functions.append(fromkeys_empty)


@trace()
def or_empty():
    fd_1 | {}


functions.append(or_empty)


@trace()
def or_empty_left():
    frozendict_class() | fd_1


functions.append(or_empty_left)


@trace()
def ior_dict():
    fd = fd_1
    fd |= dict_2


functions.append(ior_dict)


@trace()
def or_dict_empty_left():
    frozendict_class() | dict_2


functions.append(or_dict_empty_left)


@trace()
def ior_dict_empty_left():
    fd = frozendict_class()
    fd |= dict_2


functions.append(ior_dict_empty_left)


@trace()
def ior_dict_empty_right():
    fd = fd_1
    fd |= {}


functions.append(ior_dict_empty_right)


# dict | from Python 3.9
if sys.version_info >= (3, 9):
    @trace()
    def dict_or():
        dict_2 | fd_1


    functions.append(dict_or)


    @trace()
    def dict_ior():
        d = dict_2.copy()
        d |= fd_1


    functions.append(dict_ior)


    @trace()
    def dict_or_empty_left():
        {} | fd_1


    functions.append(dict_or_empty_left)


    @trace()
    def dict_ior_empty_left():
        d = {}
        d |= fd_1


    functions.append(dict_ior_empty_left)


    @trace()
    def dict_or_empty_right():
        dict_2 | frozendict_class()


    functions.append(dict_or_empty_right)


    @trace()
    def dict_ior_empty_right():
        d = dict_2.copy()
        d |= frozendict_class()


    functions.append(dict_ior_empty_right)


print_sep()

# short names, used also in the printed order
classes = {"fd": frozendict, "F": F}
instances = {}
seed_present = args.seed is not None

if seed_present:
    print(f"Seed: {args.seed}", flush=True)
    print_sep()

for class_name, frozendict_class in classes.items():
    print_info(
        frozendict_class, 
        1, 
        "frozendict_class(dict_1)"
    )
    
    fd_1 = frozendict_class(dict_1)
    print_info(
        frozendict_class, 
        1, 
        "frozendict_class(dict_unashable)"
    )
    
    fd_unashable = frozendict_class(dict_unashable)
    fd_recursive = frozendict_class(dict_unashable)
    fd_recursive[unashable_key].append(fd_recursive)
    instances[class_name] = (fd_1, fd_unashable, fd_recursive)

pairs = [
    (class_name, function)
    for class_name in classes
    for function in functions
]

if seed_present:
    rng.shuffle(pairs)

for class_name, function in pairs:
    frozendict_class = classes[class_name]
    fd_1, fd_unashable, fd_recursive = instances[class_name]
    
    print(
        f"Class = {frozendict_class.__name__} - ", 
        flush = True,
        end = ""
    )
    
    function()
    
print_sep()
print()
