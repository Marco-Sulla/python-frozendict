#include <Python.h>
#include "frozendictobject.h"
static PyObject* frozendict_iter(PyDictObject *dict);
static int frozendict_equal(PyDictObject* a, PyDictObject* b);
#ifndef PyFrozenDict_MAXFREELIST
#define PyFrozenDict_MAXFREELIST 80
#endif

typedef struct {
    PyObject *empty;
#if PyFrozenDict_MAXFREELIST > 0
    PyFrozenDictObject *free_list[PyFrozenDict_MAXFREELIST];
    int numfree;
    PyDictKeysObject *keys_free_list[PyFrozenDict_MAXFREELIST];
    int keys_numfree;
#endif
} frozendict_state;

static inline frozendict_state *frozendict_get_state(PyTypeObject *type) {
    assert(PyFrozenDict_TypeCheckExact(type));
    PyObject *module = ((PyHeapTypeObject *)type)->ht_module;

    if (module == NULL) {
        return NULL;
    }

    return (frozendict_state *)PyModule_GetState(module);
}

/* NULL for subclasses, and once the module is gone */
static inline frozendict_state *frozendict_state_of(PyObject *op) {
    PyTypeObject *type = Py_TYPE(op);

    if (PyFrozenDict_TypeCheckExact(type)) {
        return frozendict_get_state(type);
    }

    return NULL;
}

#include "other.c"
#include "dictobject.c"


static inline void
frozendict_keys_decref(PyDictKeysObject *dk)
{
    assert(dk->dk_refcnt > 0);
#ifdef Py_REF_DEBUG
    _Py_RefTotal--;
#endif
    if (--dk->dk_refcnt == 0) {
        PyObject_Free(dk);
    }
}

static PyDictKeysObject*
new_keys_object(PyObject *d, Py_ssize_t size)
{
    PyDictKeysObject *dk;
    Py_ssize_t es, usable;

    assert(size >= PyDict_MINSIZE);
    assert(IS_POWER_OF_2(size));

    usable = USABLE_FRACTION(size);
    if (size <= 0xff) {
        es = 1;
    }
    else if (size <= 0xffff) {
        es = 2;
    }
#if SIZEOF_VOID_P > 4
    else if (size <= 0xffffffff) {
        es = 4;
    }
#endif
    else {
        es = sizeof(Py_ssize_t);
    }

#if PyFrozenDict_MAXFREELIST > 0
    frozendict_state *state = frozendict_state_of(d);

    if (state != NULL && size == PyDict_MINSIZE && state->keys_numfree > 0) {
        dk = state->keys_free_list[--state->keys_numfree];
    }
    else
#endif
    {
        dk = PyObject_Malloc(sizeof(PyDictKeysObject)
                             + es * size
                             + sizeof(PyDictKeyEntry) * usable);
        if (dk == NULL) {
            PyErr_NoMemory();
            return NULL;
        }
    }
#ifdef Py_REF_DEBUG
    _Py_RefTotal++;
#endif
    dk->dk_refcnt = 1;
    dk->dk_size = size;
    dk->dk_usable = usable;
    dk->dk_lookup = lookdict_unicode_nodummy;
    dk->dk_nentries = 0;
    memset(&dk->dk_indices[0], 0xff, es * size);
    memset(DK_ENTRIES(dk), 0, sizeof(PyDictKeyEntry) * usable);
    return dk;
}

static inline PyDictKeysObject* frozendict_new_keys_object(PyObject *d, const Py_ssize_t size) {
    const Py_ssize_t newsize = calculate_keysize(size);

    if (newsize <= 0) {
        PyErr_NoMemory();
        return NULL;
    }

    assert(IS_POWER_OF_2(newsize));
    assert(newsize >= PyDict_MINSIZE);

    /* Allocate a new table. */
    return new_keys_object(d, newsize);
}

static int frozendict_resize(PyDictObject* mp, const Py_ssize_t size) {
    // size must not be a power of 2. This is done inside frozendict_new_keys_object
    PyDictKeysObject* new_keys = frozendict_new_keys_object((PyObject *)mp, size);

    if (new_keys == NULL) {
        return -1;
    }

    PyDictKeysObject* oldkeys = mp->ma_keys;

    // New table must be large enough.
    assert(new_keys->dk_usable >= mp->ma_used);

    new_keys->dk_lookup = oldkeys->dk_lookup;

    const Py_ssize_t numentries = mp->ma_used;
    PyDictKeyEntry* newentries = DK_ENTRIES(new_keys);

    memcpy(newentries, DK_ENTRIES(oldkeys), numentries * sizeof(PyDictKeyEntry));

    build_indices(new_keys, newentries, numentries);
    new_keys->dk_usable -= numentries;
    new_keys->dk_nentries = numentries;

    // do not decref the keys inside!
    frozendict_keys_decref(oldkeys);

    mp->ma_keys = new_keys;

    return 0;
}

static int frozendict_insert(PyDictObject *mp, 
                             PyObject *key,
                             const Py_hash_t hash,
                             PyObject *value,
                             int empty) {
    Py_ssize_t ix;
    PyObject *old_value;
    PyDictKeysObject *keys = mp->ma_keys;

    Py_INCREF(key);
    Py_INCREF(value);
    // if the dict is not tracked by GC and key or value can form a circular reference with it,
    // this will track it. Notice that it will track it before dict is completely constructed,
    // that could be a problem if the GIL is released
    MAINTAIN_TRACKING(mp, key, value);

    if (! empty) {
        ix = keys->dk_lookup(mp, key, hash, &old_value);

        if (ix == DKIX_ERROR) {
            Py_DECREF(value);
            Py_DECREF(key);
            return -1;
        }

        empty = (ix == DKIX_EMPTY);
    }

    if (empty) {
        /* Insert into new slot. */

        if (mp->ma_keys->dk_usable <= 0) {
            /* Need to resize. */
            if (frozendict_resize(mp, GROWTH_RATE(mp))) {
                Py_DECREF(value);
                Py_DECREF(key);
                return -1;
            }

            // resize changes keys
            keys = mp->ma_keys;
        }

        if (!PyUnicode_CheckExact(key) && keys->dk_lookup != lookdict) {
            keys->dk_lookup = lookdict;
        }

        const Py_ssize_t hashpos = find_empty_slot(keys, hash);
        const Py_ssize_t dk_nentries = keys->dk_nentries;
        PyDictKeyEntry* ep = &DK_ENTRIES(keys)[dk_nentries];
        dictkeys_set_index(keys, hashpos, dk_nentries);
        ep->me_key = key;
        ep->me_hash = hash;
        ep->me_value = value;
        mp->ma_used++;
        keys->dk_usable--;
        keys->dk_nentries++;
        assert(keys->dk_usable >= 0);
    }
    else {
        DK_ENTRIES(mp->ma_keys)[ix].me_value = value;
        Py_DECREF(old_value); /* which **CAN** re-enter (see issue #22653) */
        // but since this is an immutable map, it can't
        Py_DECREF(key);
    }

    ASSERT_CONSISTENT(mp);
    return 0;
}

static int frozendict_setitem(PyObject *op, 
                              PyObject *key,
                              PyObject *value,
                              const int empty) {
    Py_hash_t hash;

    assert(key);
    assert(value);

    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1) {
        hash = PyObject_Hash(key);

        if (hash == -1) {
            return -1;
        }
    }
    return frozendict_insert((PyDictObject*) op, key, hash, value, empty);
}

#define MINUSONE_HASH ((Py_hash_t) -1)


static PyObject *frozendict_new_barebone(PyTypeObject *type) {
    PyObject *self = NULL;
    const int exact = PyFrozenDict_TypeCheckExact(type);

#if PyFrozenDict_MAXFREELIST > 0
    if (exact) {
        frozendict_state *state = frozendict_get_state(type);

        if (state != NULL && state->numfree > 0) {
            self = (PyObject *)state->free_list[--state->numfree];
            assert(Py_IS_TYPE(self, type));
            PyObject_Init(self, type);
        }
    }
#endif

    if (self == NULL) {
        self = type->tp_alloc(type, 0);

        if (self == NULL) {
            return NULL;
        }

        /* The object has been implicitly tracked by tp_alloc */
        if (exact) {
            PyObject_GC_UnTrack(self);
        }
    }

    PyFrozenDictObject* mp = (PyFrozenDictObject*) self;

    mp->ma_keys = NULL;
    mp->ma_values = NULL;
    mp->ma_used = 0;
    mp->ma_version_tag = 0;
    mp->ma_hash = MINUSONE_HASH;

    return self;
}

// Returns the empty singleton or mp, NULL on error. Caller must not decref mp.
static PyObject* frozendict_create_empty(PyFrozenDictObject* mp, PyTypeObject* type) {
    PyObject *d = (PyObject *)mp;

    if (mp->ma_used != 0) {
        return d;
    }

    frozendict_state *state;

    if (PyFrozenDict_TypeCheckExact(type)) {
        state = frozendict_get_state(type);
    }
    else {
        state = NULL;
    }

    const int state_ok = state != NULL;

    if (state_ok && state->empty != NULL) {
        PyObject *empty = state->empty;

        Py_DECREF(mp);
        Py_INCREF(empty);

        return empty;
    }

    if (mp->ma_keys == NULL) {
        mp->ma_keys = frozendict_new_keys_object(d, 1);

        if (mp->ma_keys == NULL) {
            Py_DECREF(mp);
            return NULL;
        }
    }

    if (state_ok) {
        Py_INCREF(mp);
        state->empty = d;
        mp->ma_version_tag = DICT_NEXT_VERSION();

        if (! PyObject_GC_IsTracked(d)) {
            PyObject_GC_Track(d);
        }
    }

    return d;
}

static PyObject *
frozendict_fromkeys_impl(PyTypeObject *type, PyObject *iterable, PyObject *value)
{
    PyObject *it;       /* iter(iterable) */
    PyObject *key;
    PyObject *d;
    int status;

    d = frozendict_new_barebone(type);

    if (d == NULL)
        return NULL;

    Py_ssize_t size;
    PyDictObject *mp = (PyDictObject *)d;
    const int arg_is_dict = PyAnyDict_CheckExact(iterable);

    if (arg_is_dict) {
        PyObject *oldvalue;
        Py_ssize_t pos = 0;
        PyObject *key;
        Py_hash_t hash;

        size = PyDict_GET_SIZE(iterable);

        PyDictKeysObject* new_keys = frozendict_new_keys_object(d, estimate_keysize(size));

        if (new_keys == NULL) {
            Py_DECREF(d);
            return NULL;
        }

        mp->ma_keys = new_keys;

        while (_d_PyDict_Next(iterable, &pos, &key, &oldvalue, &hash)) {
            if (frozendict_insert(mp, key, hash, value, 0)) {
                Py_DECREF(d);
                return NULL;
            }
        }
    }
    else if (PyAnySet_CheckExact(iterable)) {
        Py_ssize_t pos = 0;
        PyObject *key;
        Py_hash_t hash;

        size = PySet_GET_SIZE(iterable);

        PyDictKeysObject* new_keys = frozendict_new_keys_object(d, estimate_keysize(size));

        if (new_keys == NULL) {
            Py_DECREF(d);
            return NULL;
        }

        mp->ma_keys = new_keys;

        while (_PySet_NextEntry(iterable, &pos, &key, &hash)) {
            if (frozendict_insert(mp, key, hash, value, 0)) {
                Py_DECREF(d);
                return NULL;
            }
        }
    }
    else {
        it = PyObject_GetIter(iterable);
        if (it == NULL){
            Py_DECREF(d);
            return NULL;
        }

        mp->ma_keys = new_keys_object(d, PyDict_MINSIZE);

        if (mp->ma_keys == NULL) {
            Py_DECREF(it);
            Py_DECREF(d);
            return NULL;
        }

        while ((key = PyIter_Next(it)) != NULL) {
            status = frozendict_setitem(d, key, value, 0);
            Py_DECREF(key);
            if (status < 0) {
                Py_DECREF(it);
                Py_DECREF(d);
                return NULL;
            }
        }

        Py_DECREF(it);

        if (PyErr_Occurred()) {
            Py_DECREF(d);
            return NULL;
        }
    }

    ASSERT_CONSISTENT(mp);

    if (PyFrozenDict_TypeCheckExact(type)) {
        return frozendict_create_empty((PyFrozenDictObject *)d, type);
    }

    if (arg_is_dict) {
        return d;
    }

    PyObject* res = PyObject_CallFunctionObjArgs((PyObject*) type, d, NULL);
    Py_DECREF(d);

    return res;
}

/* Methods */

#define REPR_GENERIC_START "("
#define REPR_GENERIC_END ")"
#define REPR_GENERIC_START_LEN strlen(REPR_GENERIC_START)
#define REPR_GENERIC_END_LEN strlen(REPR_GENERIC_END)

#define FROZENDICT_CLASS_NAME "frozendict"
#define FROZENDICT_MODULE_NAME "frozendict"
#define FROZENDICT_FULL_NAME FROZENDICT_MODULE_NAME "." FROZENDICT_CLASS_NAME
#define FROZENDICT_EMPTY_REPR REPR_GENERIC_START "{}" REPR_GENERIC_END

static PyObject* frozendict_repr(PyFrozenDictObject* mp) {
    PyObject* o = (PyObject*) mp;
    const Py_ssize_t repr_status = Py_ReprEnter(o);
    PyTypeObject* type = Py_TYPE(mp);
    const char *name;

    if (PyFrozenDict_TypeCheckExact(type)) {
        name = FROZENDICT_FULL_NAME;
    }
    else {
        name = type->tp_name;
    }

    size_t frozendict_name_len = strlen(name);

    if (repr_status != 0) {
        return repr_status > 0 ? PyUnicode_FromFormat(
            "%s" REPR_GENERIC_START "{...}" REPR_GENERIC_END, name
        ) : NULL;
    }

    if (mp->ma_used == 0) {
        Py_ReprLeave(o);

        return PyUnicode_FromFormat("%s" FROZENDICT_EMPTY_REPR, name);
    }

    _PyUnicodeWriter writer;
    _PyUnicodeWriter* pw = &writer;
    _PyUnicodeWriter_Init(pw);
    writer.overallocate = 1;
    /* classname + "({" + "1: 2" + ", 3: 4" * (len - 1) + "})" */
    writer.min_length = frozendict_name_len + 2 + 4 + (2 + 4) * (mp->ma_used - 1) + 2;
    PyObject* name_o = PyUnicode_FromString(name);

    if (name_o == NULL) {
        goto error;
    }

    const int name_err = _PyUnicodeWriter_WriteStr(pw, name_o);
    Py_DECREF(name_o);

    if (name_err) {
        goto error;
    }

    if (_PyUnicodeWriter_WriteASCIIString(pw, REPR_GENERIC_START, REPR_GENERIC_START_LEN)) {
        goto error;
    }

    if (dict_repr((PyDictObject*) mp, pw)) {
        goto error;
    }

    if (_PyUnicodeWriter_WriteASCIIString(pw, REPR_GENERIC_END, REPR_GENERIC_END_LEN)) {
        goto error;
    }

    writer.overallocate = 0;
    Py_ReprLeave(o);

    return _PyUnicodeWriter_Finish(pw);
error:
    Py_ReprLeave(o);
    _PyUnicodeWriter_Dealloc(pw);
    return NULL;
}

static int frozendict_merge(PyObject* a, PyObject* b, const int empty) {
    /* We accept for the argument either a concrete dictionary object,
     * or an abstract "mapping" object.  For the former, we can do
     * things quite efficiently.  For the latter, we only require that
     * PyMapping_Keys() and PyObject_GetItem() be supported.
     */
    assert(a != NULL);
    assert(PyFrozenDict_Check(a));
    assert(b != NULL);

    PyDictObject* mp = (PyDictObject*) a;

    if (
        PyAnyDict_Check(b) &&
        (
            Py_TYPE(b)->tp_iter == PyDict_Type.tp_iter ||
            Py_TYPE(b)->tp_iter == (getiterfunc)frozendict_iter
        )
    ) {
        PyDictObject* other = (PyDictObject*)b;
        const Py_ssize_t numentries = other->ma_used;

        if (other == mp || numentries == 0) {
            /* a.update(a) or a.update({}); nothing to do */
            return 0;
        }

        const int is_other_combined = other->ma_values == NULL;

        PyDictKeysObject* okeys = other->ma_keys;

        if (empty && is_other_combined && numentries == okeys->dk_nentries) {
            PyDictKeysObject *keys = clone_combined_dict_keys(
                frozendict_state_of(a),
                other
            );
            if (keys == NULL) {
                return -1;
            }

            mp->ma_keys = keys;
            mp->ma_used = numentries;
            mp->ma_version_tag = DICT_NEXT_VERSION();
            ASSERT_CONSISTENT(mp);

            if (_PyObject_GC_IS_TRACKED(other) && !_PyObject_GC_IS_TRACKED(mp)) {
                PyObject_GC_Track(mp);
            }

            return 0;
        }

        PyDictKeyEntry* ep0 = DK_ENTRIES(okeys);
        const PyDictKeyEntry* entry;
        PyObject* key;
        PyObject* value;
        Py_hash_t hash;
        int err;

        if (empty) {
            PyDictKeysObject *keys = frozendict_new_keys_object(a, estimate_keysize(numentries));

            if (keys == NULL) {
                return -1;
            }

            mp->ma_keys = keys;
        }
        else {
            /* Do one big resize at the start, rather than
             * incrementally resizing as we insert new items.  Expect
             * that there will be no (or few) overlapping keys.
             */
            if (mp->ma_keys->dk_usable < numentries) {
                if (frozendict_resize(mp, estimate_keysize(mp->ma_used + numentries))) {
                   return -1;
                }
            }
        }

        for (Py_ssize_t i = 0, n = okeys->dk_nentries; i < n; i++) {
            entry = &ep0[i];
            key = entry->me_key;
            hash = entry->me_hash;

            if (is_other_combined) {
                value = entry->me_value;
            }
            else {
                value = other->ma_values[i];
            }

            if (value != NULL) {
                Py_INCREF(key);
                Py_INCREF(value);
                err = frozendict_insert(mp, key, hash, value, empty);
                Py_DECREF(value);
                Py_DECREF(key);

                if (err != 0) {
                    return -1;
                }

                if (n != other->ma_keys->dk_nentries) {
                    PyErr_SetString(PyExc_RuntimeError,
                                    "dict mutated during update");
                    return -1;
                }
            }
        }
    }
    else {
        /* Do it the generic, slower way */
        PyObject *keys = PyMapping_Keys(b);
        PyObject *iter;
        PyObject *key, *value;
        int status;

        if (mp->ma_keys == NULL) {
            mp->ma_keys = new_keys_object(a, PyDict_MINSIZE);

            if (mp->ma_keys == NULL) {
                Py_XDECREF(keys);
                return -1;
            }
        }

        if (keys == NULL)
            /* Docstring says this is equivalent to E.keys() so
             * if E doesn't have a .keys() method we want
             * AttributeError to percolate up.  Might as well
             * do the same for any other error.
             */
            return -1;

        iter = PyObject_GetIter(keys);
        Py_DECREF(keys);
        if (iter == NULL)
            return -1;

        for (key = PyIter_Next(iter); key; key = PyIter_Next(iter)) {
            value = PyObject_GetItem(b, key);
            if (value == NULL) {
                Py_DECREF(iter);
                Py_DECREF(key);
                return -1;
            }
            status = frozendict_setitem(a, key, value, 0);
            Py_DECREF(key);
            Py_DECREF(value);
            if (status < 0) {
                Py_DECREF(iter);
                return -1;
            }
        }
        Py_DECREF(iter);
        if (PyErr_Occurred())
            /* Iterator completed, via error */
            return -1;
    }
    ASSERT_CONSISTENT(a);
    return 0;
}

static int frozendict_merge_from_seq2(PyObject* d, PyObject* seq2) {
    assert(d != NULL);
    assert(PyFrozenDict_Check(d));
    assert(seq2 != NULL);

    PyObject* it = PyObject_GetIter(seq2);

    if (it == NULL) {
        return -1;
    }

    PyObject* fast;     /* item as a 2-tuple or 2-list */
    PyObject* key;
    PyObject* value;
    Py_ssize_t n;
    PyObject* item;
    int res = 0;

    PyDictObject* mp = (PyDictObject*) d;

    if (mp->ma_keys == NULL) {
        mp->ma_keys = new_keys_object(d, PyDict_MINSIZE);

        if (mp->ma_keys == NULL) {
            Py_DECREF(it);
            return -1;
        }
    }

    for (Py_ssize_t i = 0; ; ++i) {
        fast = NULL;
        item = PyIter_Next(it);

        if (item == NULL) {
            if (PyErr_Occurred()) {
                res = -1;
            }

            break;
        }

        /* Convert item to sequence, and verify length 2. */
        fast = PySequence_Fast(item, "");

        if (fast == NULL) {
            if (PyErr_ExceptionMatches(PyExc_TypeError)) {
                PyErr_Format(PyExc_TypeError,
                    "cannot convert dictionary update "
                    "sequence element #%zd to a sequence",
                    i);
            }
            Py_DECREF(item);
            res = -1;
            break;
        }

        n = PySequence_Fast_GET_SIZE(fast);

        if (n != 2) {
            PyErr_Format(PyExc_ValueError,
                         "dictionary update sequence element #%zd "
                         "has length %zd; 2 is required",
                         i, n);
            Py_DECREF(fast);
            Py_DECREF(item);
            res = -1;
            break;
        }

        /* Update/merge with this (key, value) pair. */
        key = PySequence_Fast_GET_ITEM(fast, 0);
        Py_INCREF(key);
        value = PySequence_Fast_GET_ITEM(fast, 1);
        Py_INCREF(value);

        if (frozendict_setitem(d, key, value, 0) < 0) {
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(fast);
            Py_DECREF(item);
            res = -1;
            break;
        }

        Py_DECREF(key);
        Py_DECREF(value);
        Py_DECREF(fast);
        Py_DECREF(item);
    }

    Py_DECREF(it);
    ASSERT_CONSISTENT(d);
    return res;
}

static int frozendict_update_arg(PyObject *self, 
                                 PyObject *arg,
                                 const int empty) {
    if (PyAnyDict_CheckExact(arg)) {
        return frozendict_merge(self, arg, empty);
    }
    _Py_IDENTIFIER(keys);
    PyObject *func;
    if (_PyObject_LookupAttrId(arg, &PyId_keys, &func) < 0) {
        return -1;
    }
    if (func != NULL) {
        Py_DECREF(func);
        return frozendict_merge(self, arg, empty);
    }
    return frozendict_merge_from_seq2(self, arg);
}

static int frozendict_update_common(PyObject* self, 
                                    PyObject* arg,
                                    PyObject* kwds) {
    int result = 0;
    const int no_arg = (arg == NULL);

    if (! no_arg) {
        result = frozendict_update_arg(self, arg, 1);
    }

    if (result == 0 && kwds != NULL) {
        if (PyArg_ValidateKeywordArguments(kwds)) {
            result = frozendict_merge(self, kwds, no_arg);
        }
        else {
            result = -1;
        }
    }

    return result;
}

/* Forward */
static PyObject *frozendictkeys_new(PyObject *, PyObject *);
static PyObject *frozendictitems_new(PyObject *, PyObject *);
static PyObject *frozendictvalues_new(PyObject *, PyObject *);

static Py_hash_t frozendict_hash(PyObject* self) {
    PyFrozenDictObject* frozen_self = (PyFrozenDictObject*) self;

    if (frozen_self->ma_hash != MINUSONE_HASH) {
        return frozen_self->ma_hash;
    }

    PyObject* frozen_items_tmp = frozendictitems_new(self, NULL);

    if (frozen_items_tmp == NULL) {
        return MINUSONE_HASH;
    }

    PyObject* frozen_items = PyFrozenSet_New(frozen_items_tmp);
    Py_DECREF(frozen_items_tmp);

    if (frozen_items == NULL) {
        return MINUSONE_HASH;
    }

    const Py_hash_t hash = PyFrozenSet_Type.tp_hash(frozen_items);
    Py_DECREF(frozen_items);

    frozen_self->ma_hash = hash;

    return hash;
}

static PyObject* frozendict_copy(PyObject* o, PyObject* Py_UNUSED(ignored)) {
    if (PyFrozenDict_CheckExact(o)) {
        Py_INCREF(o);
        return o;
    }

    PyTypeObject* type = Py_TYPE(o);
    PyObject* res = PyObject_CallFunctionObjArgs((PyObject *) type, o, NULL);

    return res;
}

static int frozendict_equal(PyDictObject* a, PyDictObject* b) {
    if (a == b) {
        return 1;
    }

    if (a->ma_used != b->ma_used) {
        /* can't be equal if # of entries differ */
        return 0;
    }

    PyDictKeysObject* keys = a->ma_keys;
    const PyDictKeyEntry* ep;
    PyObject* aval;
    int cmp = 1;
    PyObject* bval;
    PyObject* key;

    /* Same # of entries -- check all of 'em.  Exit early on any diff. */
    for (Py_ssize_t i = 0; i < keys->dk_nentries; i++) {
        ep = &DK_ENTRIES(keys)[i];
        aval = ep->me_value;
        Py_INCREF(aval);
        key = ep->me_key;
        Py_INCREF(key);

        /* reuse the known hash value */
        b->ma_keys->dk_lookup(b, key, ep->me_hash, &bval);

        if (bval == NULL) {
            if (PyErr_Occurred()) {
                cmp = -1;
            }
            else {
                cmp = 0;
            }
        }
        else {
            Py_INCREF(bval);
            cmp = PyObject_RichCompareBool(aval, bval, Py_EQ);
            Py_DECREF(bval);
        }

        Py_DECREF(key);
        Py_DECREF(aval);
        if (cmp <= 0) { /* error or not equal */
            break;
        }
    }

    return cmp;
}

static Py_ssize_t dict_get_index(PyDictObject *self, PyObject *key) {
    Py_hash_t hash;
    PyObject* val;

    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return DKIX_ERROR;
    }
    return (self->ma_keys->dk_lookup) (self, key, hash, &val);
}

static PyObject * frozendict_reduce(
    PyFrozenDictObject *self,
    PyObject *Py_UNUSED(ignored)
) {
    PyObject *o = PyDict_Type.tp_alloc(&PyDict_Type, 0);

    if (o == NULL) {
        return NULL;
    }

    PyDictObject *d = (PyDictObject *)o;
    PyDictKeysObject *keys = clone_combined_dict_keys(
        NULL,
        (PyDictObject*) self
    );

    if (keys == NULL) {
        Py_DECREF(d);
        return NULL;
    }

    d->ma_keys = keys;
    d->ma_values = NULL;
    d->ma_used = self->ma_used;
    d->ma_version_tag = DICT_NEXT_VERSION();
    ASSERT_CONSISTENT(d);

    PyObject *args = PyTuple_Pack(1, d);
    Py_DECREF(d);

    if (args == NULL) {
        return NULL;
    }

    PyObject *tuple = PyTuple_Pack(2, Py_TYPE(self), args);
    Py_DECREF(args);

    return tuple;
}

// the caller must track the clone if self is tracked, once it's complete
static PyObject* frozendict_clone(PyObject* self) {
    PyTypeObject* type = Py_TYPE(self);
    PyObject *new_op = frozendict_new_barebone(type);

    if (new_op == NULL){
        return NULL;
    }

    PyDictObject* mp = (PyDictObject*) self;

    PyDictKeysObject *keys = clone_combined_dict_keys(
        frozendict_state_of(self),
        mp
    );

    if (keys == NULL) {
        Py_DECREF(new_op);

        return NULL;
    }

    PyFrozenDictObject* new_mp = (PyFrozenDictObject*) new_op;
    new_mp->ma_keys = keys;

    new_mp->ma_used = mp->ma_used;
    new_mp->ma_hash = MINUSONE_HASH;
    new_mp->ma_version_tag = DICT_NEXT_VERSION();

    ASSERT_CONSISTENT(new_mp);

    return new_op;
}

static PyObject* frozendict_set(
    PyObject* self,
    PyObject* const* args,
    const Py_ssize_t nargs
) {
    if (!_PyArg_CheckPositional("set", nargs, 2, 2)) {
        return NULL;
    }

    PyObject* new_op = frozendict_clone(self);

    if (new_op == NULL) {
        return NULL;
    }

    PyObject* set_key = args[0];

    if (frozendict_setitem(new_op, set_key, args[1], 0)) {
        Py_DECREF(new_op);
        return NULL;
    }

    if (PyObject_GC_IsTracked(self) && ! PyObject_GC_IsTracked(new_op)) {
        PyObject_GC_Track(new_op);
    }

    return new_op;
}

static PyObject* frozendict_setdefault(
    PyObject* self,
    PyObject* const* args,
    const Py_ssize_t nargs
) {
    if (!_PyArg_CheckPositional("setdefault", nargs, 1, 2)) {
        return NULL;
    }

    PyObject* set_key = args[0];

    const int contains = PyDict_Contains(self, set_key);

    if (contains < 0) {
        return NULL;
    }

    if (contains) {
        Py_INCREF(self);
        return self;
    }

    PyObject* new_op = frozendict_clone(self);

    if (new_op == NULL) {
        return NULL;
    }

    PyObject* val;

    if (nargs == 2) {
        val = args[1];
    }
    else {
        val = Py_None;
    }

    if (frozendict_setitem(new_op, set_key, val, 0)) {
        Py_DECREF(new_op);

        return NULL;
    }

    if (PyObject_GC_IsTracked(self) && ! PyObject_GC_IsTracked(new_op)) {
        PyObject_GC_Track(new_op);
    }

    return new_op;
}

static PyObject* frozendict_delete(
    PyObject* self,
    PyObject *const *args,
    const Py_ssize_t nargs
) {
    if (! _PyArg_CheckPositional("delete", nargs, 1, 1)) {
        return NULL;
    }

    PyDictObject* mp = (PyDictObject*) self;
    PyObject* del_key = args[0];
    const Py_ssize_t ix = dict_get_index(mp, del_key);

    if (ix == DKIX_ERROR) {
        return NULL;
    }

    if (ix == DKIX_EMPTY) {
        _PyErr_SetKeyError(del_key);
        return NULL;
    }

    const Py_ssize_t size = mp->ma_used;
    const Py_ssize_t sizemm = size - 1;

    if (sizemm == 0) {
        return PyObject_CallNoArgs((PyObject *)Py_TYPE(self));
    }

    PyTypeObject* type = Py_TYPE(self);
    PyObject *new_op = frozendict_new_barebone(type);

    if (new_op == NULL) {
        return NULL;
    }

    PyDictKeysObject* new_keys = frozendict_new_keys_object(self, estimate_keysize(sizemm));

    if (new_keys == NULL) {
        Py_DECREF(new_op);
        return NULL;
    }

    PyDictKeysObject* old_keys = mp->ma_keys;
    new_keys->dk_lookup = old_keys->dk_lookup;

    PyFrozenDictObject* new_mp = (PyFrozenDictObject*) new_op;

    // New table must be large enough.
    assert(new_keys->dk_usable >= new_mp->ma_used);

    new_mp->ma_keys = new_keys;
    new_mp->ma_hash = MINUSONE_HASH;
    new_mp->ma_version_tag = DICT_NEXT_VERSION();

    PyObject* key;
    PyObject* value;
    Py_hash_t hash;
    Py_ssize_t hashpos;
    PyDictKeyEntry* old_entries = DK_ENTRIES(old_keys);
    PyDictKeyEntry* new_entries = DK_ENTRIES(new_keys);
    const PyDictKeyEntry* old_entry;
    PyDictKeyEntry* new_entry;
    Py_ssize_t new_i;
    int deleted = 0;

    for (Py_ssize_t i = 0; i < size; i++) {
        if (i == ix) {
            deleted = 1;
            continue;
        }

        new_i = i - deleted;

        old_entry = &old_entries[i];
        hash = old_entry->me_hash;
        key = old_entry->me_key;
        value = old_entry->me_value;
        Py_INCREF(key);
        Py_INCREF(value);
        hashpos = find_empty_slot(new_keys, hash);
        dictkeys_set_index(new_keys, hashpos, new_i);
        new_entry = &new_entries[new_i];
        new_entry->me_key = key;
        new_entry->me_hash = hash;
        new_entry->me_value = value;
    }

    new_mp->ma_used = sizemm;
    new_keys->dk_usable -= sizemm;
    new_keys->dk_nentries = sizemm;

    ASSERT_CONSISTENT(new_mp);

    if (PyObject_GC_IsTracked(self) && ! PyObject_GC_IsTracked(new_op)) {
        PyObject_GC_Track(new_op);
    }

    return new_op;
}


static PyObject* frozendict_key(
    PyObject* self,
    PyObject *const *args,
    const Py_ssize_t nargs
) {
    if (! _PyArg_CheckPositional("key", nargs, 0, 1)) {
        return NULL;
    }

    Py_ssize_t index;
    Py_ssize_t passed_index;
    const PyDictObject* d = (PyDictObject*) self;
    const Py_ssize_t size = d->ma_used;

    if (nargs > 0) {
        index = PyLong_AsSsize_t(args[0]);
        passed_index = index;

        if (index < 0) {
            if (PyErr_Occurred()) {
                return NULL;
            }

            index += size;
        }
    }
    else {
        index = 0;
        passed_index = index;
    }

    const Py_ssize_t maxindex = size - 1;

    if (index > maxindex || index < 0) {
        PyErr_Format(
            PyExc_IndexError,
            "%s index %zd out of range %zd",
            Py_TYPE(self)->tp_name,
            passed_index,
            maxindex
        );

        return NULL;
    }

    PyObject* res = DK_ENTRIES(d->ma_keys)[index].me_key;
    Py_INCREF(res);

    return res;
}

static PyObject* frozendict_value(
    PyObject* self,
    PyObject *const *args,
    const Py_ssize_t nargs
) {
    if (! _PyArg_CheckPositional("value", nargs, 0, 1)) {
        return NULL;
    }

    Py_ssize_t index;
    Py_ssize_t passed_index;
    const PyDictObject* d = (PyDictObject*) self;
    const Py_ssize_t size = d->ma_used;

    if (nargs > 0) {
        index = PyLong_AsSsize_t(args[0]);
        passed_index = index;

        if (index < 0) {
            if (PyErr_Occurred()) {
                return NULL;
            }

            index += size;
        }
    }
    else {
        index = 0;
        passed_index = index;
    }

    const Py_ssize_t maxindex = size - 1;

    if (index > maxindex || index < 0) {
        PyErr_Format(
            PyExc_IndexError,
            "%s index %zd out of range %zd",
            Py_TYPE(self)->tp_name,
            passed_index,
            maxindex
        );

        return NULL;
    }

    PyObject* res = DK_ENTRIES(d->ma_keys)[index].me_value;
    Py_INCREF(res);

    return res;
}

static PyObject* frozendict_item(
    PyObject* self,
    PyObject *const *args,
    const Py_ssize_t nargs
) {
    if (! _PyArg_CheckPositional("item", nargs, 0, 1)) {
        return NULL;
    }

    Py_ssize_t index;
    Py_ssize_t passed_index;
    const PyDictObject* d = (PyDictObject*) self;
    const Py_ssize_t size = d->ma_used;

    if (nargs > 0) {
        index = PyLong_AsSsize_t(args[0]);
        passed_index = index;

        if (index < 0) {
            if (PyErr_Occurred()) {
                return NULL;
            }

            index += size;
        }
    }
    else {
        index = 0;
        passed_index = index;
    }

    const Py_ssize_t maxindex = size - 1;

    if (index > maxindex || index < 0) {
        PyErr_Format(
            PyExc_IndexError,
            "%s index %zd out of range %zd",
            Py_TYPE(self)->tp_name,
            passed_index,
            maxindex
        );

        return NULL;
    }

    PyObject* key = DK_ENTRIES(d->ma_keys)[index].me_key;
    Py_INCREF(key);
    PyObject* val = DK_ENTRIES(d->ma_keys)[index].me_value;
    Py_INCREF(val);

    PyObject* res = PyTuple_New(2);

    if (res == NULL) {
        Py_DECREF(key);
        Py_DECREF(val);

        return NULL;
    }

    PyTuple_SET_ITEM(res, 0, key);
    PyTuple_SET_ITEM(res, 1, val);

    return res;
}

PyDoc_STRVAR(frozendict_set_doc,
"set($self, key, value, /)\n"
"--\n"
"\n"
"Returns a copy of the dictionary with the new (key, value) item.   ");

PyDoc_STRVAR(frozendict_setdefault_doc,
"set($self, key[, default], /)\n"
"--\n"
"\n"
"If key is in the dictionary, it returns the dictionary unchanged. \n"
"Otherwise, it returns a copy of the dictionary with the new (key, default) item; \n"
"default argument is optional and is None by default.   ");

PyDoc_STRVAR(frozendict_delete_doc,
"delete($self, key, /)\n"
"--\n"
"\n"
"Returns a copy of the dictionary without the item of the corresponding key.   ");

PyDoc_STRVAR(frozendict_key_doc,
"key($self[, index], /)\n"
"--\n"
"\n"
"Get the key at the specified index (insertion order). If index is not \n"
"passed, it defaults to 0. If index is negative, returns the key at \n"
"position size + index.   ");

PyDoc_STRVAR(frozendict_value_doc,
"value($self[, index], /)\n"
"--\n"
"\n"
"Get the value at the specified index (insertion order). If index is not \n"
"passed, it defaults to 0. If index is negative, returns the value at \n"
"position size + index.   ");

PyDoc_STRVAR(frozendict_item_doc,
"item($self[, index], /)\n"
"--\n"
"\n"
"Get the (key, value) item at the specified index (insertion order). If \n"
"index is not passed, it defaults to 0. If index is negative, returns the \n"
"item at position size + index.   ");

static PyMethodDef frozendict_mapp_methods[] = {
    DICT___CONTAINS___METHODDEF
    {"__getitem__", (PyCFunction)(void(*)(void))dict_subscript,        METH_O | METH_COEXIST,
     getitem__doc__},
    {"__sizeof__",      (PyCFunction)(void(*)(void))dict_sizeof,       METH_NOARGS,
     sizeof__doc__},
    DICT_GET_METHODDEF
    {"keys",            frozendictkeys_new,             METH_NOARGS,
    keys__doc__},
    {"items",           frozendictitems_new,            METH_NOARGS,
    items__doc__},
    {"values",          frozendictvalues_new,           METH_NOARGS,
    values__doc__},
    {"fromkeys",        (PyCFunction)(void(*)(void))dict_fromkeys, METH_FASTCALL|METH_CLASS,
    dict_fromkeys__doc__},
    {"copy",            (PyCFunction)frozendict_copy,   METH_NOARGS,
     copy__doc__},
    {"__copy__",        (PyCFunction)frozendict_copy,   METH_NOARGS,
     "Returns a copy of the object."},
    DICT___REVERSED___METHODDEF
    {"__class_getitem__", Py_GenericAlias, METH_O|METH_CLASS, "See PEP 585"},
    {"__reduce__", (PyCFunction)(void(*)(void))frozendict_reduce, METH_NOARGS,
     ""},
    {"set",             (PyCFunction)(void(*)(void))
                        frozendict_set,                 METH_FASTCALL,
    frozendict_set_doc},
    {"setdefault",      (PyCFunction)(void(*)(void))
                        frozendict_setdefault,          METH_FASTCALL,
    frozendict_setdefault_doc},
    {"delete",          (PyCFunction)(void(*)(void))
                        frozendict_delete,              METH_FASTCALL,
    frozendict_delete_doc},
    {"key",             (PyCFunction)(void(*)(void))
                        frozendict_key,                 METH_FASTCALL,
    frozendict_key_doc},
    {"value",           (PyCFunction)(void(*)(void))
                        frozendict_value,               METH_FASTCALL,
    frozendict_value_doc},
    {"item",            (PyCFunction)(void(*)(void))
                        frozendict_item,                METH_FASTCALL,
    frozendict_item_doc},
    {NULL,              NULL}   /* sentinel */
};

static PyObject* frozendict_vectorcall(PyObject* type, 
                                       PyObject* const* args,
                                       const size_t nargsf,
                                       PyObject* kwnames) {
    assert(PyType_Check(type));
    const Py_ssize_t nargs = PyVectorcall_NARGS(nargsf);

    if (! _PyArg_CheckPositional(FROZENDICT_CLASS_NAME, nargs, 0, 1)) {
        return NULL;
    }

    PyTypeObject* ttype = (PyTypeObject*) type;

    Py_ssize_t size;
    PyObject* arg = NULL;

    if (nargs == 1) {
        arg = args[0];

        // only argument is a frozendict
        if (
            arg != NULL &&
            PyFrozenDict_CheckExact(arg) &&
            PyFrozenDict_TypeCheckExact(ttype)
        ) {
            size = (
                kwnames == NULL
                ? 0
                : PyTuple_GET_SIZE(kwnames)
            );

            if (size == 0) {
                Py_INCREF(arg);

                return arg;
            }
        }
    }

    PyObject* self = frozendict_new_barebone(ttype);

    if (self == NULL) {
        return NULL;
    }

    PyFrozenDictObject* mp = (PyFrozenDictObject*) self;

    int empty = 1;

    if (nargs == 1) {
        if (frozendict_update_arg(self, arg, 1) < 0) {
            Py_DECREF(self);
            return NULL;
        }

        empty = mp->ma_used == 0;
        args++;
    }

    size = (
        kwnames == NULL
        ? 0
        : PyTuple_GET_SIZE(kwnames)
    );

    if (size != 0) {
        if (mp->ma_keys == NULL) {
            mp->ma_keys = frozendict_new_keys_object((PyObject *)mp, estimate_keysize(size));

            if (mp->ma_keys == NULL) {
                Py_DECREF(self);
                return NULL;
            }
        }

        if (mp->ma_keys->dk_usable < size) {
            if (frozendict_resize((PyDictObject*) self, estimate_keysize(mp->ma_used + size))) {
                Py_DECREF(self);

                return NULL;
            }
        }

        for (Py_ssize_t i = 0; i < size; i++) {
            if (frozendict_setitem(self, PyTuple_GET_ITEM(kwnames, i), args[i], empty) < 0) {
                Py_DECREF(self);
                return NULL;
            }
        }
    }

    PyObject* self_empty = frozendict_create_empty(mp, ttype);

    if (self_empty != self) {
        return self_empty;
    }

    mp->ma_version_tag = DICT_NEXT_VERSION();

    ASSERT_CONSISTENT(mp);

    return self;
}

static PyObject* frozendict_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    assert(type != NULL && type->tp_alloc != NULL);

    PyObject* arg = NULL;

    if (args != NULL && ! PyArg_UnpackTuple(args, FROZENDICT_CLASS_NAME, 0, 1, &arg)) {
        return NULL;
    }

    const int arg_is_frozendict = (arg != NULL && PyFrozenDict_CheckExact(arg));
    const int kwds_size = ((kwds != NULL)
        ? ((PyDictObject*) kwds)->ma_used
        : 0
    );

    // only argument is a frozendict
    if (arg_is_frozendict && kwds_size == 0 && PyFrozenDict_TypeCheckExact(type)) {
        Py_INCREF(arg);

        return arg;
    }

    PyObject* self = frozendict_new_barebone(type);

    if (self == NULL) {
        return NULL;
    }

    PyFrozenDictObject* mp = (PyFrozenDictObject*) self;

    if (frozendict_update_common(self, arg, kwds)) {
        Py_DECREF(self);
        return NULL;
    }

    PyObject* empty = frozendict_create_empty(mp, type);

    if (empty != self) {
        return empty;
    }

    mp->ma_version_tag = DICT_NEXT_VERSION();

    return self;
}

static PyObject* frozendict_or(PyObject *self, PyObject *other) {
    if (! (
        (PyAnyDict_Check(other) && PyFrozenDict_Check(self))
        || (PyAnyDict_Check(self) && PyFrozenDict_Check(other))
    )){
        Py_RETURN_NOTIMPLEMENTED;
    }

    if (
        ((PyDictObject *)other)->ma_used == 0
        && PyAnyDict_CheckExact(other)
        && PyFrozenDict_CheckExact(self)
    ) {
        Py_INCREF(self);
        return self;
    }

    if (
        ((PyDictObject *)self)->ma_used == 0
        && PyFrozenDict_CheckExact(other)
        && PyFrozenDict_CheckExact(self)
    ) {
        Py_INCREF(other);
        return other;
    }

    if (PyDict_Check(self)) {
        PyObject *res = PyDict_Copy(self);

        if (res == NULL) {
            return NULL;
        }

        if (PyDict_Update(res, other)) {
            Py_DECREF(res);
            return NULL;
        }

        return res;
    }


    PyObject* new_op = frozendict_clone(self);

    if (new_op == NULL) {
        return NULL;
    }

    if (frozendict_update_arg(new_op, other, 0)) {
        Py_DECREF(new_op);
        return NULL;
    }

    if (PyObject_GC_IsTracked(self) && ! PyObject_GC_IsTracked(new_op)) {
        PyObject_GC_Track(new_op);
    }

    return frozendict_create_empty((PyFrozenDictObject *)new_op, Py_TYPE(new_op));
}

PyDoc_STRVAR(frozendict_doc,
"An immutable version of dict.\n"
"\n"
FROZENDICT_FULL_NAME "() -> returns an empty immutable dictionary\n"
FROZENDICT_FULL_NAME "(mapping) -> returns an immutable dictionary initialized\n"
"    from a mapping object's (key, value) pairs\n"
FROZENDICT_FULL_NAME "(iterable) -> returns an immutable dictionary, equivalent to:\n"
"    d = {}\n"
"    "
"    for k, v in iterable:\n"
"        d[k] = v\n"
"    "
"    " FROZENDICT_FULL_NAME "(d)\n"
FROZENDICT_FULL_NAME "(**kwargs) -> returns an immutable dictionary initialized with\n"
"    the name=value pairs in the keyword argument list. For example:\n"
"    " FROZENDICT_FULL_NAME "(one=1, two=2)");


static void frozendict_dealloc(PyFrozenDictObject *mp) {
    PyTypeObject *type = Py_TYPE(mp);
    PyDictKeysObject *keys = mp->ma_keys;

    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(mp);
    Py_TRASHCAN_BEGIN(mp, frozendict_dealloc)

    assert(mp->ma_values == NULL);

    frozendict_state *state = frozendict_state_of((PyObject *)mp);

    if (keys != NULL) {
        assert(keys->dk_refcnt == 1);
        dictkeys_decref(state, keys);
    }

#if PyFrozenDict_MAXFREELIST > 0
    if (state != NULL && state->numfree < PyFrozenDict_MAXFREELIST) {
        state->free_list[state->numfree++] = mp;
    }
    else
#endif
    {
        type->tp_free((PyObject *)mp);
    }

    Py_DECREF(type);

    Py_TRASHCAN_END
}

static int frozendict_traverse(PyObject *op, const visitproc visit, void *arg) {
    Py_VISIT(Py_TYPE(op));
    return dict_traverse(op, visit, arg);
}

static PyType_Slot frozendict_type_slots[] = {
    {Py_tp_dealloc, frozendict_dealloc},
    {Py_tp_repr, frozendict_repr},
    {Py_nb_or, frozendict_or},
    {Py_sq_contains, PyDict_Contains},
    {Py_mp_length, dict_length},
    {Py_mp_subscript, dict_subscript},
    {Py_tp_hash, frozendict_hash},
    {Py_tp_getattro, PyObject_GenericGetAttr},
    {Py_tp_doc, (void *)frozendict_doc},
    {Py_tp_traverse, frozendict_traverse},
    {Py_tp_richcompare, dict_richcompare},
    {Py_tp_iter, frozendict_iter},
    {Py_tp_methods, frozendict_mapp_methods},
    {Py_tp_alloc, PyType_GenericAlloc},
    {Py_tp_new, frozendict_new},
    {Py_tp_free, PyObject_GC_Del},
    {0, NULL},
};

static PyType_Spec frozendict_spec = {
    .name = FROZENDICT_FULL_NAME,
    .basicsize = sizeof(PyFrozenDictObject),
    .itemsize = 0,
    .flags = (
        Py_TPFLAGS_DEFAULT
        | Py_TPFLAGS_HAVE_GC
        | Py_TPFLAGS_BASETYPE
        | _Py_TPFLAGS_MATCH_SELF
        | Py_TPFLAGS_MAPPING
        | Py_TPFLAGS_IMMUTABLETYPE
    ),
    .slots = frozendict_type_slots,
};

/* Dictionary iterator types */

static PyObject* frozendict_iter(PyDictObject *dict) {
    return dictiter_new(dict, &PyFrozenDictIterKey_Type);
}

static PyObject* frozendictiter_iternextkey(dictiterobject* di) {
    const Py_ssize_t pos = di->di_pos;
    assert(pos >= 0);
    PyDictObject* d = di->di_dict;

    if (d == NULL) {
        return NULL;
    }

    assert(PyFrozenDict_Check(d));

    if (pos >= d->ma_used) {
        di->di_dict = NULL;
        Py_DECREF(d);
        return NULL;
    }

    PyObject* key = DK_ENTRIES(d->ma_keys)[pos].me_key;
    assert(key != NULL);
    di->di_pos++;
    di->len--;
    Py_INCREF(key);
    return key;
}

static PyTypeObject PyFrozenDictIterKey_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".keyiterator",      /* tp_name */
    sizeof(dictiterobject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictiter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictiter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)frozendictiter_iternextkey,   /* tp_iternext */
    dictiter_methods,                           /* tp_methods */
    0,
};

static PyObject* frozendictiter_iternextvalue(dictiterobject* di) {
    const Py_ssize_t pos = di->di_pos;
    assert(pos >= 0);
    PyDictObject* d = di->di_dict;

    if (d == NULL) {
        return NULL;
    }

    assert(PyFrozenDict_Check(d));

    if (pos >= d->ma_used) {
        di->di_dict = NULL;
        Py_DECREF(d);
        return NULL;
    }

    PyObject* val = DK_ENTRIES(d->ma_keys)[pos].me_value;
    assert(val != NULL);
    di->di_pos++;
    di->len--;
    Py_INCREF(val);
    return val;
}

static PyTypeObject PyFrozenDictIterValue_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".valueiterator",    /* tp_name */
    sizeof(dictiterobject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictiter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictiter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)frozendictiter_iternextvalue, /* tp_iternext */
    dictiter_methods,                           /* tp_methods */
    0,
};

static PyObject* frozendictiter_iternextitem(dictiterobject* di) {
    const Py_ssize_t pos = di->di_pos;
    assert(pos >= 0);
    PyDictObject* d = di->di_dict;

    if (d == NULL) {
        return NULL;
    }

    assert(PyFrozenDict_Check(d));

    if (pos >= d->ma_used) {
        di->di_dict = NULL;
        Py_DECREF(d);
        return NULL;
    }

    const PyDictKeyEntry* entry_ptr = &DK_ENTRIES(d->ma_keys)[pos];
    PyObject* key = entry_ptr->me_key;
    PyObject* val = entry_ptr->me_value;
    assert(key != NULL);
    assert(val != NULL);
    di->di_pos++;
    di->len--;
    Py_INCREF(key);
    Py_INCREF(val);

    PyObject* result;
    if (Py_REFCNT(di->di_result) == 1) {
        result = di->di_result;
        PyObject *oldkey = PyTuple_GET_ITEM(result, 0);
        PyObject *oldvalue = PyTuple_GET_ITEM(result, 1);
        Py_INCREF(result);
        Py_DECREF(oldkey);
        Py_DECREF(oldvalue);

        if (!_PyObject_GC_IS_TRACKED(result)) {
            PyObject_GC_Track(result);
        }
    }
    else {
        result = PyTuple_New(2);

        if (result == NULL) {
            // key and val are already owned here
            Py_DECREF(key);
            Py_DECREF(val);

            return NULL;
        }
    }

    PyTuple_SET_ITEM(result, 0, key);  /* steals reference */
    PyTuple_SET_ITEM(result, 1, val);  /* steals reference */
    return result;
}

static PyTypeObject PyFrozenDictIterItem_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".itemiterator",     /* tp_name */
    sizeof(dictiterobject),                     /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictiter_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,/* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictiter_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)frozendictiter_iternextitem,  /* tp_iternext */
    dictiter_methods,                           /* tp_methods */
    0,
};

/*** dict_keys ***/

static PyObject *
frozendictkeys_iter(const _PyDictViewObject *dv)
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyFrozenDictIterKey_Type);
}

static PyTypeObject PyFrozenDictKeys_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".keys",             /* tp_name */
    sizeof(_PyDictViewObject),                  /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictview_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)dictview_repr,                    /* tp_repr */
    &dictviews_as_number,                       /* tp_as_number */
    &dictkeys_as_sequence,                      /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,/* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictview_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    dictview_richcompare,                       /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    (getiterfunc)frozendictkeys_iter,           /* tp_iter */
    0,                                          /* tp_iternext */
    dictkeys_methods,                           /* tp_methods */
    .tp_getset = dictview_getset,
};

static PyObject *
frozendictkeys_new(PyObject *dict, PyObject *Py_UNUSED(ignored))
{
    return _d_PyDictView_New(dict, &PyFrozenDictKeys_Type);
}

/*** dict_items ***/

static PyObject *
frozendictitems_iter(const _PyDictViewObject *dv)
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyFrozenDictIterItem_Type);
}

static PyTypeObject PyFrozenDictItems_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".items",            /* tp_name */
    sizeof(_PyDictViewObject),                  /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictview_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)dictview_repr,                    /* tp_repr */
    &dictviews_as_number,                       /* tp_as_number */
    &dictitems_as_sequence,                     /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,/* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictview_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    dictview_richcompare,                       /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    (getiterfunc)frozendictitems_iter,          /* tp_iter */
    0,                                          /* tp_iternext */
    dictitems_methods,                          /* tp_methods */
    .tp_getset = dictview_getset,
};

static PyObject *
frozendictitems_new(PyObject *dict, PyObject *Py_UNUSED(ignored))
{
    return _d_PyDictView_New(dict, &PyFrozenDictItems_Type);
}

/*** dict_values ***/

static PyObject *
frozendictvalues_iter(const _PyDictViewObject *dv)
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyFrozenDictIterValue_Type);
}

static PyTypeObject PyFrozenDictValues_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    FROZENDICT_MODULE_NAME ".values",           /* tp_name */
    sizeof(_PyDictViewObject),                  /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)dictview_dealloc,               /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)dictview_repr,                    /* tp_repr */
    0,                                          /* tp_as_number */
    &dictvalues_as_sequence,                    /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,/* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)dictview_traverse,            /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    (getiterfunc)frozendictvalues_iter,         /* tp_iter */
    0,                                          /* tp_iternext */
    dictvalues_methods,                         /* tp_methods */
    .tp_getset = dictview_getset,
};

static PyObject *
frozendictvalues_new(PyObject *dict, PyObject *Py_UNUSED(ignored))
{
    return _d_PyDictView_New(dict, &PyFrozenDictValues_Type);
}

static int
frozendict_exec(PyObject *m)
{
    /* Finalize the type object including setting type of the new type
     * object; doing it here is required for portability, too. */
    if (PyType_Ready(&PyFrozenDictIterKey_Type) < 0) {
        goto fail;
    }

    if (PyType_Ready(&PyFrozenDictIterValue_Type) < 0) {
        goto fail;
    }

    if (PyType_Ready(&PyFrozenDictIterItem_Type) < 0) {
        goto fail;
    }

    if (PyType_Ready(&PyFrozenDictKeys_Type) < 0) {
        goto fail;
    }

    if (PyType_Ready(&PyFrozenDictItems_Type) < 0) {
        goto fail;
    }

    if (PyType_Ready(&PyFrozenDictValues_Type) < 0) {
        goto fail;
    }

    PyObject *type = PyType_FromModuleAndSpec(m, &frozendict_spec, NULL);

    if (type == NULL) {
        goto fail;
    }

    // PyType_Spec has no slot for tp_vectorcall before 3.14
    ((PyTypeObject *)type)->tp_vectorcall = frozendict_vectorcall;

    const int added = PyModule_AddObjectRef(m, FROZENDICT_CLASS_NAME, type);
    Py_DECREF(type);

    if (added < 0) {
        goto fail;
    }

    return 0;
 fail:
    return -1;
}

static struct PyModuleDef_Slot frozendict_slots[] = {
    {Py_mod_exec, frozendict_exec},
    {0, NULL},
};

static int frozendict_module_traverse(PyObject *m, const visitproc visit, void *arg) {
    const frozendict_state *state = PyModule_GetState(m);
    Py_VISIT(state->empty);
    return 0;
}

static int frozendict_module_clear(PyObject *m) {
    frozendict_state *state = PyModule_GetState(m);
    Py_CLEAR(state->empty);
    return 0;
}

static void frozendict_module_free(void *m) {
    frozendict_module_clear((PyObject *)m);

#if PyFrozenDict_MAXFREELIST > 0
    frozendict_state *state = PyModule_GetState((PyObject *)m);

    while (state->numfree > 0) {
        PyObject_GC_Del(state->free_list[--state->numfree]);
    }

    while (state->keys_numfree > 0) {
        PyObject_Free(state->keys_free_list[--state->keys_numfree]);
    }
#endif
}

static struct PyModuleDef frozendictmodule = {
    PyModuleDef_HEAD_INIT,
    FROZENDICT_MODULE_NAME,   /* name of module */
    NULL, /* module documentation, may be NULL */
    sizeof(frozendict_state),   /* size of per-interpreter state */
    NULL,
    frozendict_slots,
    frozendict_module_traverse,
    frozendict_module_clear,
    frozendict_module_free
};

PyMODINIT_FUNC
PyInit__frozendict(void)
{
    return PyModuleDef_Init(&frozendictmodule);
}
