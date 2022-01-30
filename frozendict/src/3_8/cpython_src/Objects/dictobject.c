/* Dictionary object implementation using a hash table */

/* The distribution includes a separate file, Objects/dictnotes.txt,
   describing explorations into dictionary design and optimization.
   It covers typical dictionary use patterns, the parameters for
   tuning dictionaries, and several ideas for possible optimizations.
*/

/* PyDictKeysObject

This implements the dictionary's hashtable.

As of Python 3.6, this is compact and ordered. Basic idea is described here:
* https://mail.python.org/pipermail/python-dev/2012-December/123028.html
* https://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html

layout:

+---------------+
| dk_refcnt     |
| dk_size       |
| dk_lookup     |
| dk_usable     |
| dk_nentries   |
+---------------+
| dk_indices    |
|               |
+---------------+
| dk_entries    |
|               |
+---------------+

dk_indices is actual hashtable.  It holds index in entries, or DKIX_EMPTY(-1)
or DKIX_DUMMY(-2).
Size of indices is dk_size.  Type of each index in indices is vary on dk_size:

* int8  for          dk_size <= 128
* int16 for 256   <= dk_size <= 2**15
* int32 for 2**16 <= dk_size <= 2**31
* int64 for 2**32 <= dk_size

dk_entries is array of PyDictKeyEntry.  Its size is USABLE_FRACTION(dk_size).
DK_ENTRIES(dk) can be used to get pointer to entries.

NOTE: Since negative value is used for DKIX_EMPTY and DKIX_DUMMY, type of
dk_indices entry is signed integer and int16 is used for table which
dk_size == 256.
*/


/*
The DictObject can be in one of two forms.

Either:
  A combined table:
    ma_values == NULL, dk_refcnt == 1.
    Values are stored in the me_value field of the PyDictKeysObject.
Or:
  A split table:
    ma_values != NULL, dk_refcnt >= 1
    Values are stored in the ma_values array.
    Only string (unicode) keys are allowed.
    All dicts sharing same key must have same insertion order.

There are four kinds of slots in the table (slot is index, and
DK_ENTRIES(keys)[index] if index >= 0):

1. Unused.  index == DKIX_EMPTY
   Does not hold an active (key, value) pair now and never did.  Unused can
   transition to Active upon key insertion.  This is each slot's initial state.

2. Active.  index >= 0, me_key != NULL and me_value != NULL
   Holds an active (key, value) pair.  Active can transition to Dummy or
   Pending upon key deletion (for combined and split tables respectively).
   This is the only case in which me_value != NULL.

3. Dummy.  index == DKIX_DUMMY  (combined only)
   Previously held an active (key, value) pair, but that was deleted and an
   active pair has not yet overwritten the slot.  Dummy can transition to
   Active upon key insertion.  Dummy slots cannot be made Unused again
   else the probe sequence in case of collision would have no way to know
   they were once active.

4. Pending. index >= 0, key != NULL, and value == NULL  (split only)
   Not yet inserted in split-table.
*/

/*
Preserving insertion order

It's simple for combined table.  Since dk_entries is mostly append only, we can
get insertion order by just iterating dk_entries.

One exception is .popitem().  It removes last item in dk_entries and decrement
dk_nentries to achieve amortized O(1).  Since there are DKIX_DUMMY remains in
dk_indices, we can't increment dk_usable even though dk_nentries is
decremented.

In split table, inserting into pending entry is allowed only for dk_entries[ix]
where ix == mp->ma_used. Inserting into other index and deleting item cause
converting the dict to the combined table.
*/

/* PyDict_MINSIZE is the starting size for any new dict.
 * 8 allows dicts with no more than 5 active entries; experiments suggested
 * this suffices for the majority of dicts (consisting mostly of usually-small
 * dicts created to pass keyword arguments).
 * Making this 8, rather than 4 reduces the number of resizes for most
 * dictionaries, without any significant extra memory use.
 */
#define PyDict_MINSIZE 8

#include "Python.h"
#include "dict-common.h"
#include "stringlib/eq.h"    // unicode_eq()

/*[clinic input]
class dict "PyDictObject *" "&PyDict_Type"
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=f157a5a0ce9589d6]*/


/*
To ensure the lookup algorithm terminates, there must be at least one Unused
slot (NULL key) in the table.
To avoid slowing down lookups on a near-full table, we resize the table when
it's USABLE_FRACTION (currently two-thirds) full.
*/

#define PERTURB_SHIFT 5

/*
Major subtleties ahead:  Most hash schemes depend on having a "good" hash
function, in the sense of simulating randomness.  Python doesn't:  its most
important hash functions (for ints) are very regular in common
cases:

  >>>[hash(i) for i in range(4)]
  [0, 1, 2, 3]

This isn't necessarily bad!  To the contrary, in a table of size 2**i, taking
the low-order i bits as the initial table index is extremely fast, and there
are no collisions at all for dicts indexed by a contiguous range of ints. So
this gives better-than-random behavior in common cases, and that's very
desirable.

OTOH, when collisions occur, the tendency to fill contiguous slices of the
hash table makes a good collision resolution strategy crucial.  Taking only
the last i bits of the hash code is also vulnerable:  for example, consider
the list [i << 16 for i in range(20000)] as a set of keys.  Since ints are
their own hash codes, and this fits in a dict of size 2**15, the last 15 bits
 of every hash code are all 0:  they *all* map to the same table index.

But catering to unusual cases should not slow the usual ones, so we just take
the last i bits anyway.  It's up to collision resolution to do the rest.  If
we *usually* find the key we're looking for on the first try (and, it turns
out, we usually do -- the table load factor is kept under 2/3, so the odds
are solidly in our favor), then it makes best sense to keep the initial index
computation dirt cheap.

The first half of collision resolution is to visit table indices via this
recurrence:

    j = ((5*j) + 1) mod 2**i

For any initial j in range(2**i), repeating that 2**i times generates each
int in range(2**i) exactly once (see any text on random-number generation for
proof).  By itself, this doesn't help much:  like linear probing (setting
j += 1, or j -= 1, on each loop trip), it scans the table entries in a fixed
order.  This would be bad, except that's not the only thing we do, and it's
actually *good* in the common cases where hash keys are consecutive.  In an
example that's really too small to make this entirely clear, for a table of
size 2**3 the order of indices is:

    0 -> 1 -> 6 -> 7 -> 4 -> 5 -> 2 -> 3 -> 0 [and here it's repeating]

If two things come in at index 5, the first place we look after is index 2,
not 6, so if another comes in at index 6 the collision at 5 didn't hurt it.
Linear probing is deadly in this case because there the fixed probe order
is the *same* as the order consecutive keys are likely to arrive.  But it's
extremely unlikely hash codes will follow a 5*j+1 recurrence by accident,
and certain that consecutive hash codes do not.

The other half of the strategy is to get the other bits of the hash code
into play.  This is done by initializing a (unsigned) vrbl "perturb" to the
full hash code, and changing the recurrence to:

    perturb >>= PERTURB_SHIFT;
    j = (5*j) + 1 + perturb;
    use j % 2**i as the next table index;

Now the probe sequence depends (eventually) on every bit in the hash code,
and the pseudo-scrambling property of recurring on 5*j+1 is more valuable,
because it quickly magnifies small differences in the bits that didn't affect
the initial index.  Note that because perturb is unsigned, if the recurrence
is executed often enough perturb eventually becomes and remains 0.  At that
point (very rarely reached) the recurrence is on (just) 5*j+1 again, and
that's certain to find an empty slot eventually (since it generates every int
in range(2**i), and we make sure there's always at least one empty slot).

Selecting a good value for PERTURB_SHIFT is a balancing act.  You want it
small so that the high bits of the hash code continue to affect the probe
sequence across iterations; but you want it large so that in really bad cases
the high-order hash bits have an effect on early iterations.  5 was "the
best" in minimizing total collisions across experiments Tim Peters ran (on
both normal and pathological cases), but 4 and 6 weren't significantly worse.

Historical: Reimer Behrends contributed the idea of using a polynomial-based
approach, using repeated multiplication by x in GF(2**n) where an irreducible
polynomial for each table size was chosen such that x was a primitive root.
Christian Tismer later extended that to use division by x instead, as an
efficient way to get the high bits of the hash code into play.  This scheme
also gave excellent collision statistics, but was more expensive:  two
if-tests were required inside the loop; computing "the next" index took about
the same number of operations but without as much potential parallelism
(e.g., computing 5*j can go on at the same time as computing 1+perturb in the
above, and then shifting perturb can be done while the table index is being
masked); and the PyDictObject struct required a member to hold the table's
polynomial.  In Tim's experiments the current scheme ran faster, produced
equally good collision statistics, needed less code & used less memory.

*/

/* forward declarations */
static Py_ssize_t lookdict(PyDictObject *mp, PyObject *key,
                           Py_hash_t hash, PyObject **value_addr);
static Py_ssize_t
lookdict_unicode_nodummy(PyDictObject *mp, PyObject *key,
                                 Py_hash_t hash, PyObject **value_addr);

/*Global counter used to set ma_version_tag field of dictionary.
 * It is incremented each time that a dictionary is created and each
 * time that a dictionary is modified. */
static uint64_t pydict_global_version = 0;

#define DICT_NEXT_VERSION() (++pydict_global_version)

/* Dictionary reuse scheme to save calls to malloc and free */
#ifndef PyDict_MAXFREELIST
#define PyDict_MAXFREELIST 80
#endif

#if PyDict_MAXFREELIST > 0
static PyDictObject *free_list[PyDict_MAXFREELIST];
static int numfree = 0;
static PyDictKeysObject *keys_free_list[PyDict_MAXFREELIST];
static int numfreekeys = 0;
#endif

#include "clinic/dictobject.c.h"

#define DK_SIZE(dk) ((dk)->dk_size)
#if SIZEOF_VOID_P > 4
#define DK_IXSIZE(dk)                          \
    (DK_SIZE(dk) <= 0xff ?                     \
        1 : DK_SIZE(dk) <= 0xffff ?            \
            2 : DK_SIZE(dk) <= 0xffffffff ?    \
                4 : sizeof(int64_t))
#else
#define DK_IXSIZE(dk)                          \
    (DK_SIZE(dk) <= 0xff ?                     \
        1 : DK_SIZE(dk) <= 0xffff ?            \
            2 : sizeof(int32_t))
#endif
#define DK_ENTRIES(dk) \
    ((PyDictKeyEntry*)(&((int8_t*)((dk)->dk_indices))[DK_SIZE(dk) * DK_IXSIZE(dk)]))

#define DK_MASK(dk) (((dk)->dk_size)-1)
#define IS_POWER_OF_2(x) (((x) & (x-1)) == 0)

static void free_keys_object(PyDictKeysObject *keys);

static inline void
dictkeys_incref(PyDictKeysObject *dk)
{
    _Py_INC_REFTOTAL;
    dk->dk_refcnt++;
}

static inline void
dictkeys_decref(PyDictKeysObject *dk)
{
    assert(dk->dk_refcnt > 0);
    _Py_DEC_REFTOTAL;
    if (--dk->dk_refcnt == 0) {
        free_keys_object(dk);
    }
}

/* lookup indices.  returns DKIX_EMPTY, DKIX_DUMMY, or ix >=0 */
static inline Py_ssize_t
dictkeys_get_index(const PyDictKeysObject *keys, Py_ssize_t i)
{
    Py_ssize_t s = DK_SIZE(keys);
    Py_ssize_t ix;

    if (s <= 0xff) {
        const int8_t *indices = (const int8_t*)(keys->dk_indices);
        ix = indices[i];
    }
    else if (s <= 0xffff) {
        const int16_t *indices = (const int16_t*)(keys->dk_indices);
        ix = indices[i];
    }
#if SIZEOF_VOID_P > 4
    else if (s > 0xffffffff) {
        const int64_t *indices = (const int64_t*)(keys->dk_indices);
        ix = indices[i];
    }
#endif
    else {
        const int32_t *indices = (const int32_t*)(keys->dk_indices);
        ix = indices[i];
    }
    assert(ix >= DKIX_DUMMY);
    return ix;
}

/* write to indices. */
static inline void
dictkeys_set_index(PyDictKeysObject *keys, Py_ssize_t i, Py_ssize_t ix)
{
    Py_ssize_t s = DK_SIZE(keys);

    assert(ix >= DKIX_DUMMY);

    if (s <= 0xff) {
        int8_t *indices = (int8_t*)(keys->dk_indices);
        assert(ix <= 0x7f);
        indices[i] = (char)ix;
    }
    else if (s <= 0xffff) {
        int16_t *indices = (int16_t*)(keys->dk_indices);
        assert(ix <= 0x7fff);
        indices[i] = (int16_t)ix;
    }
#if SIZEOF_VOID_P > 4
    else if (s > 0xffffffff) {
        int64_t *indices = (int64_t*)(keys->dk_indices);
        indices[i] = ix;
    }
#endif
    else {
        int32_t *indices = (int32_t*)(keys->dk_indices);
        assert(ix <= 0x7fffffff);
        indices[i] = (int32_t)ix;
    }
}


/* USABLE_FRACTION is the maximum dictionary load.
 * Increasing this ratio makes dictionaries more dense resulting in more
 * collisions.  Decreasing it improves sparseness at the expense of spreading
 * indices over more cache lines and at the cost of total memory consumed.
 *
 * USABLE_FRACTION must obey the following:
 *     (0 < USABLE_FRACTION(n) < n) for all n >= 2
 *
 * USABLE_FRACTION should be quick to calculate.
 * Fractions around 1/2 to 2/3 seem to work well in practice.
 */
#define USABLE_FRACTION(n) (((n) << 1)/3)

/* Find the smallest dk_size >= minsize. */
static inline Py_ssize_t
calculate_keysize(Py_ssize_t minsize)
{
#if SIZEOF_LONG == SIZEOF_SIZE_T
    minsize = (minsize | PyDict_MINSIZE) - 1;
    return 1LL << _Py_bit_length(minsize | (PyDict_MINSIZE-1));
#elif defined(_MSC_VER)
    // On 64bit Windows, sizeof(long) == 4.
    minsize = (minsize | PyDict_MINSIZE) - 1;
    unsigned long msb;
    _BitScanReverse64(&msb, (uint64_t)minsize);
    return 1LL << (msb + 1);
#else
    Py_ssize_t size;
    for (size = PyDict_MINSIZE;
            size < minsize && size > 0;
            size <<= 1)
        ;
    return size;
#endif
}

/* estimate_keysize is reverse function of USABLE_FRACTION.
 *
 * This can be used to reserve enough size to insert n entries without
 * resizing.
 */
static inline Py_ssize_t
estimate_keysize(Py_ssize_t n)
{
    return calculate_keysize((n*3 + 1) / 2);
}


/* GROWTH_RATE. Growth rate upon hitting maximum load.
 * Currently set to used*3.
 * This means that dicts double in size when growing without deletions,
 * but have more head room when the number of deletions is on a par with the
 * number of insertions.  See also bpo-17563 and bpo-33205.
 *
 * GROWTH_RATE was set to used*4 up to version 3.2.
 * GROWTH_RATE was set to used*2 in version 3.3.0
 * GROWTH_RATE was set to used*2 + capacity/2 in 3.4.0-3.6.0.
 */
#define GROWTH_RATE(d) ((d)->ma_used*3)

/* This immutable, empty PyDictKeysObject is used for PyDict_Clear()
 * (which cannot fail and thus can do no allocation).
 */
static PyDictKeysObject empty_keys_struct = {
        1, /* dk_refcnt */
        1, /* dk_size */
        lookdict_unicode_nodummy, /* dk_lookup */
        0, /* dk_usable (immutable) */
        0, /* dk_nentries */
        {DKIX_EMPTY, DKIX_EMPTY, DKIX_EMPTY, DKIX_EMPTY,
         DKIX_EMPTY, DKIX_EMPTY, DKIX_EMPTY, DKIX_EMPTY}, /* dk_indices */
};

static PyObject *empty_values[1] = { NULL };

#define Py_EMPTY_KEYS &empty_keys_struct

/* Uncomment to check the dict content in _PyDict_CheckConsistency() */
/* #define DEBUG_PYDICT */

#ifdef DEBUG_PYDICT
#  define ASSERT_CONSISTENT(op) assert(_PyDict_CheckConsistency((PyObject *)(op), 1))
#else
#  define ASSERT_CONSISTENT(op) assert(_PyDict_CheckConsistency((PyObject *)(op), 0))
#endif


static int
_PyDict_CheckConsistency(PyObject *op, int check_content)
{
#define CHECK(expr) \
    do { if (!(expr)) { _PyObject_ASSERT_FAILED_MSG(op, Py_STRINGIFY(expr)); } } while (0)

    assert(op != NULL);
    CHECK(PyAnyDict_Check(op));
    PyDictObject *mp = (PyDictObject *)op;

    PyDictKeysObject *keys = mp->ma_keys;
    int splitted = _PyDict_HasSplitTable(mp);
    Py_ssize_t usable = USABLE_FRACTION(keys->dk_size);

    CHECK(0 <= mp->ma_used && mp->ma_used <= usable);
    CHECK(IS_POWER_OF_2(keys->dk_size));
    CHECK(0 <= keys->dk_usable && keys->dk_usable <= usable);
    CHECK(0 <= keys->dk_nentries && keys->dk_nentries <= usable);
    CHECK(keys->dk_usable + keys->dk_nentries <= usable);

    if (!splitted) {
        /* combined table */
        CHECK(keys->dk_refcnt == 1);
    }

    if (check_content) {
        PyDictKeyEntry *entries = DK_ENTRIES(keys);
        Py_ssize_t i;

        for (i=0; i < keys->dk_size; i++) {
            Py_ssize_t ix = dictkeys_get_index(keys, i);
            CHECK(DKIX_DUMMY <= ix && ix <= usable);
        }

        for (i=0; i < usable; i++) {
            PyDictKeyEntry *entry = &entries[i];
            PyObject *key = entry->me_key;

            if (key != NULL) {
                if (PyUnicode_CheckExact(key)) {
                    Py_hash_t hash = ((PyASCIIObject *)key)->hash;
                    CHECK(hash != -1);
                    CHECK(entry->me_hash == hash);
                }
                else {
                    /* test_dict fails if PyObject_Hash() is called again */
                    CHECK(entry->me_hash != -1);
                }
                if (!splitted) {
                    CHECK(entry->me_value != NULL);
                }
            }

            if (splitted) {
                CHECK(entry->me_value == NULL);
            }
        }

        if (splitted) {
            /* splitted table */
            for (i=0; i < mp->ma_used; i++) {
                CHECK(mp->ma_values[i] != NULL);
            }
        }
    }
    return 1;

#undef CHECK
}


static PyDictKeysObject*
new_keys_object(Py_ssize_t size)
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

#if PyDict_MAXFREELIST > 0
    if (size == PyDict_MINSIZE && numfreekeys > 0) {
        dk = keys_free_list[--numfreekeys];
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
    _Py_INC_REFTOTAL;
    dk->dk_refcnt = 1;
    dk->dk_size = size;
    dk->dk_usable = usable;
    dk->dk_lookup = lookdict_unicode_nodummy;
    dk->dk_nentries = 0;
    memset(&dk->dk_indices[0], 0xff, es * size);
    memset(DK_ENTRIES(dk), 0, sizeof(PyDictKeyEntry) * usable);
    return dk;
}

static void
free_keys_object(PyDictKeysObject *keys)
{
    PyDictKeyEntry *entries = DK_ENTRIES(keys);
    Py_ssize_t i, n;
    for (i = 0, n = keys->dk_nentries; i < n; i++) {
        Py_XDECREF(entries[i].me_key);
        Py_XDECREF(entries[i].me_value);
    }
#if PyDict_MAXFREELIST > 0
    if (keys->dk_size == PyDict_MINSIZE && numfreekeys < PyDict_MAXFREELIST) {
        keys_free_list[numfreekeys++] = keys;
        return;
    }
#endif
    PyObject_Free(keys);
}

#define new_values(size) PyMem_NEW(PyObject *, size)
#define free_values(values) PyMem_Free(values)

static Py_ssize_t
_d_PyDict_KeysSize(PyDictKeysObject *keys)
{
    return (sizeof(PyDictKeysObject)
            + DK_IXSIZE(keys) * DK_SIZE(keys)
            + USABLE_FRACTION(DK_SIZE(keys)) * sizeof(PyDictKeyEntry));
}

static PyDictKeysObject *
clone_combined_dict_keys(PyDictObject *orig)
{
    assert(PyAnyDict_Check(orig));

    assert(
        Py_TYPE(orig)->tp_iter == PyDict_Type.tp_iter ||
        Py_TYPE(orig)->tp_iter == (getiterfunc)frozendict_iter
    );

    assert(orig->ma_values == NULL);
    assert(orig->ma_keys->dk_refcnt == 1);

    Py_ssize_t keys_size = _d_PyDict_KeysSize(orig->ma_keys);
    PyDictKeysObject *keys = PyObject_Malloc(keys_size);
    if (keys == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    memcpy(keys, orig->ma_keys, keys_size);

    /* After copying key/value pairs, we need to incref all
       keys and values and they are about to be co-owned by a
       new dict object. */
    PyDictKeyEntry *ep0 = DK_ENTRIES(keys);
    Py_ssize_t n = keys->dk_nentries;
    for (Py_ssize_t i = 0; i < n; i++) {
        PyDictKeyEntry *entry = &ep0[i];
        PyObject *value = entry->me_value;
        Py_INCREF(value);
        Py_INCREF(entry->me_key);
    }

    /* Since we copied the keys table we now have an extra reference
       in the system.  Manually call _Py_INC_REFTOTAL to signal that
       we have it now; calling dictkeys_incref would be an error as
       keys->dk_refcnt is already set to 1 (after memcpy). */
    _Py_INC_REFTOTAL;

    return keys;
}

/*
The basic lookup function used by all operations.
This is based on Algorithm D from Knuth Vol. 3, Sec. 6.4.
Open addressing is preferred over chaining since the link overhead for
chaining would be substantial (100% with typical malloc overhead).

The initial probe index is computed as hash mod the table size. Subsequent
probe indices are computed as explained earlier.

All arithmetic on hash should ignore overflow.

The details in this version are due to Tim Peters, building on many past
contributions by Reimer Behrends, Jyrki Alakuijala, Vladimir Marangozov and
Christian Tismer.

lookdict() is general-purpose, and may return DKIX_ERROR if (and only if) a
comparison raises an exception.
lookdict_unicode() below is specialized to string keys, comparison of which can
never raise an exception; that function can never return DKIX_ERROR when key
is string.  Otherwise, it falls back to lookdict().
lookdict_unicode_nodummy is further specialized for string keys that cannot be
the <dummy> value.
For both, when the key isn't found a DKIX_EMPTY is returned.
*/
static Py_ssize_t _Py_HOT_FUNCTION
lookdict(PyDictObject *mp, PyObject *key,
         Py_hash_t hash, PyObject **value_addr)
{
    size_t i, mask, perturb;
    PyDictKeysObject *dk;
    PyDictKeyEntry *ep0;

top:
    dk = mp->ma_keys;
    ep0 = DK_ENTRIES(dk);
    mask = DK_MASK(dk);
    perturb = hash;
    i = (size_t)hash & mask;

    for (;;) {
        Py_ssize_t ix = dictkeys_get_index(dk, i);
        if (ix == DKIX_EMPTY) {
            *value_addr = NULL;
            return ix;
        }
        if (ix >= 0) {
            PyDictKeyEntry *ep = &ep0[ix];
            assert(ep->me_key != NULL);
            if (ep->me_key == key) {
                *value_addr = ep->me_value;
                return ix;
            }
            if (ep->me_hash == hash) {
                PyObject *startkey = ep->me_key;
                Py_INCREF(startkey);
                int cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                Py_DECREF(startkey);
                if (cmp < 0) {
                    *value_addr = NULL;
                    return DKIX_ERROR;
                }
                if (dk == mp->ma_keys && ep->me_key == startkey) {
                    if (cmp > 0) {
                        *value_addr = ep->me_value;
                        return ix;
                    }
                }
                else {
                    /* The dict was mutated, restart */
                    goto top;
                }
            }
        }
        perturb >>= PERTURB_SHIFT;
        i = (i*5 + perturb + 1) & mask;
    }
    Py_UNREACHABLE();
}

/* Faster version of lookdict_unicode when it is known that no <dummy> keys
 * will be present. */
static Py_ssize_t _Py_HOT_FUNCTION
lookdict_unicode_nodummy(PyDictObject *mp, PyObject *key,
                         Py_hash_t hash, PyObject **value_addr)
{
    assert(mp->ma_values == NULL);
    /* Make sure this function doesn't have to handle non-unicode keys,
       including subclasses of str; e.g., one reason to subclass
       unicodes is to override __eq__, and for speed we don't cater to
       that here. */
    if (!PyUnicode_CheckExact(key)) {
        return lookdict(mp, key, hash, value_addr);
    }

    PyDictKeyEntry *ep0 = DK_ENTRIES(mp->ma_keys);
    size_t mask = DK_MASK(mp->ma_keys);
    size_t perturb = (size_t)hash;
    size_t i = (size_t)hash & mask;

    for (;;) {
        Py_ssize_t ix = dictkeys_get_index(mp->ma_keys, i);
        assert (ix != DKIX_DUMMY);
        if (ix == DKIX_EMPTY) {
            *value_addr = NULL;
            return DKIX_EMPTY;
        }
        PyDictKeyEntry *ep = &ep0[ix];
        assert(ep->me_key != NULL);
        assert(PyUnicode_CheckExact(ep->me_key));
        if (ep->me_key == key ||
            (ep->me_hash == hash && unicode_eq(ep->me_key, key))) {
            *value_addr = ep->me_value;
            return ix;
        }
        perturb >>= PERTURB_SHIFT;
        i = mask & (i*5 + perturb + 1);
    }
    Py_UNREACHABLE();
}

#define MAINTAIN_TRACKING(mp, key, value) \
    do { \
        if (!_PyObject_GC_IS_TRACKED(mp)) { \
            if (_PyObject_GC_MAY_BE_TRACKED(key) || \
                _PyObject_GC_MAY_BE_TRACKED(value)) { \
                PyObject_GC_Track(mp); \
            } \
        } \
    } while(0)

/* Internal function to find slot for an item from its hash
   when it is known that the key is not present in the dict.

   The dict must be combined. */
static Py_ssize_t
find_empty_slot(PyDictKeysObject *keys, Py_hash_t hash)
{
    assert(keys != NULL);

    const size_t mask = DK_MASK(keys);
    size_t i = hash & mask;
    Py_ssize_t ix = dictkeys_get_index(keys, i);
    for (size_t perturb = hash; ix >= 0;) {
        perturb >>= PERTURB_SHIFT;
        i = (i*5 + perturb + 1) & mask;
        ix = dictkeys_get_index(keys, i);
    }
    return i;
}

/*
Internal routine used by dictresize() to build a hashtable of entries.
*/
static void
build_indices(PyDictKeysObject *keys, PyDictKeyEntry *ep, Py_ssize_t n)
{
    size_t mask = (size_t)DK_SIZE(keys) - 1;
    for (Py_ssize_t ix = 0; ix != n; ix++, ep++) {
        Py_hash_t hash = ep->me_hash;
        size_t i = hash & mask;
        for (size_t perturb = hash; dictkeys_get_index(keys, i) != DKIX_EMPTY;) {
            perturb >>= PERTURB_SHIFT;
            i = mask & (i*5 + perturb + 1);
        }
        dictkeys_set_index(keys, i, ix);
    }
}

static int
_d_PyDict_Next(PyObject *op, Py_ssize_t *ppos, PyObject **pkey,
             PyObject **pvalue, Py_hash_t *phash)
{
    Py_ssize_t i;
    PyDictObject *mp;
    PyDictKeyEntry *entry_ptr;
    PyObject *value;

    if (!PyAnyDict_Check(op))
        return 0;
    mp = (PyDictObject *)op;
    i = *ppos;
    if (mp->ma_values) {
        if (i < 0 || i >= mp->ma_used)
            return 0;
        /* values of split table is always dense */
        entry_ptr = &DK_ENTRIES(mp->ma_keys)[i];
        value = mp->ma_values[i];
        assert(value != NULL);
    }
    else {
        Py_ssize_t n = mp->ma_keys->dk_nentries;
        if (i < 0 || i >= n)
            return 0;
        entry_ptr = &DK_ENTRIES(mp->ma_keys)[i];
        while (i < n && entry_ptr->me_value == NULL) {
            entry_ptr++;
            i++;
        }
        if (i >= n)
            return 0;
        value = entry_ptr->me_value;
    }
    *ppos = i+1;
    if (pkey)
        *pkey = entry_ptr->me_key;
    if (phash)
        *phash = entry_ptr->me_hash;
    if (pvalue)
        *pvalue = value;
    return 1;
}

/* Methods */

static void
dict_dealloc(PyDictObject *mp)
{
    PyObject **values = mp->ma_values;
    PyDictKeysObject *keys = mp->ma_keys;
    Py_ssize_t i, n;

    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(mp);
    Py_TRASHCAN_BEGIN(mp, dict_dealloc)
    if (values != NULL) {
        if (values != empty_values) {
            for (i = 0, n = mp->ma_keys->dk_nentries; i < n; i++) {
                Py_XDECREF(values[i]);
            }
            free_values(values);
        }
        dictkeys_decref(keys);
    }
    else if (keys != NULL) {
        assert(keys->dk_refcnt == 1 || keys == Py_EMPTY_KEYS);
        dictkeys_decref(keys);
    }
#if PyDict_MAXFREELIST > 0
    if (numfree < PyDict_MAXFREELIST && Py_IS_TYPE(mp, &PyDict_Type)) {
        free_list[numfree++] = mp;
    }
    else
#endif
    {
        Py_TYPE(mp)->tp_free((PyObject *)mp);
    }
    Py_TRASHCAN_END
}

static PyObject *
dict_repr(PyDictObject *mp)
{
    Py_ssize_t i;
    PyObject *key = NULL, *value = NULL;
    _PyUnicodeWriter writer;
    int first;

    i = Py_ReprEnter((PyObject *)mp);
    if (i != 0) {
        return i > 0 ? PyUnicode_FromString("{...}") : NULL;
    }

    if (mp->ma_used == 0) {
        Py_ReprLeave((PyObject *)mp);
        return PyUnicode_FromString("{}");
    }

    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    /* "{" + "1: 2" + ", 3: 4" * (len - 1) + "}" */
    writer.min_length = 1 + 4 + (2 + 4) * (mp->ma_used - 1) + 1;

    if (_PyUnicodeWriter_WriteChar(&writer, '{') < 0)
        goto error;

    /* Do repr() on each key+value pair, and insert ": " between them.
       Note that repr may mutate the dict. */
    i = 0;
    first = 1;
    while (_d_PyDict_Next((PyObject *)mp, &i, &key, &value, NULL)) {
        PyObject *s;
        int res;

        /* Prevent repr from deleting key or value during key format. */
        Py_INCREF(key);
        Py_INCREF(value);

        if (!first) {
            if (_PyUnicodeWriter_WriteASCIIString(&writer, ", ", 2) < 0)
                goto error;
        }
        first = 0;

        s = PyObject_Repr(key);
        if (s == NULL)
            goto error;
        res = _PyUnicodeWriter_WriteStr(&writer, s);
        Py_DECREF(s);
        if (res < 0)
            goto error;

        if (_PyUnicodeWriter_WriteASCIIString(&writer, ": ", 2) < 0)
            goto error;

        s = PyObject_Repr(value);
        if (s == NULL)
            goto error;
        res = _PyUnicodeWriter_WriteStr(&writer, s);
        Py_DECREF(s);
        if (res < 0)
            goto error;

        Py_CLEAR(key);
        Py_CLEAR(value);
    }

    writer.overallocate = 0;
    if (_PyUnicodeWriter_WriteChar(&writer, '}') < 0)
        goto error;

    Py_ReprLeave((PyObject *)mp);

    return _PyUnicodeWriter_Finish(&writer);

error:
    Py_ReprLeave((PyObject *)mp);
    _PyUnicodeWriter_Dealloc(&writer);
    Py_XDECREF(key);
    Py_XDECREF(value);
    return NULL;
}

static Py_ssize_t
dict_length(PyDictObject *mp)
{
    return mp->ma_used;
}

static PyObject *
dict_subscript(PyDictObject *mp, PyObject *key)
{
    Py_ssize_t ix;
    Py_hash_t hash;
    PyObject *value;

    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return NULL;
    }
    ix = (mp->ma_keys->dk_lookup)(mp, key, hash, &value);
    if (ix == DKIX_ERROR)
        return NULL;
    if (ix == DKIX_EMPTY || value == NULL) {
        if (!PyAnyDict_CheckExact(mp)) {
            /* Look up __missing__ method if we're a subclass. */
            PyObject *missing, *res;
            _Py_IDENTIFIER(__missing__);
            missing = _PyObject_LookupSpecial((PyObject *)mp, &PyId___missing__);
            if (missing != NULL) {
                res = PyObject_CallFunctionObjArgs(missing,
                                                   key, NULL);
                Py_DECREF(missing);
                return res;
            }
            else if (PyErr_Occurred())
                return NULL;
        }
        _PyErr_SetKeyError(key);
        return NULL;
    }
    Py_INCREF(value);
    return value;
}

static PyObject *
dict_richcompare(PyObject *v, PyObject *w, int op)
{
    int cmp;
    PyObject *res;

    if (!PyAnyDict_Check(v) || !PyAnyDict_Check(w)) {
        res = Py_NotImplemented;
    }
    else if (op == Py_EQ || op == Py_NE) {
        cmp = frozendict_equal((PyDictObject *)v, (PyDictObject *)w);
        if (cmp < 0)
            return NULL;
        res = (cmp == (op == Py_EQ)) ? Py_True : Py_False;
    }
    else
        res = Py_NotImplemented;
    Py_INCREF(res);
    return res;
}

/*[clinic input]

@coexist
dict.__contains__

  key: object
  /

True if the dictionary has the specified key, else False.
[clinic start generated code]*/

static PyObject *
dict___contains__(PyDictObject *self, PyObject *key)
/*[clinic end generated code: output=a3d03db709ed6e6b input=fe1cb42ad831e820]*/
{
    register PyDictObject *mp = self;
    Py_hash_t hash;
    Py_ssize_t ix;
    PyObject *value;

    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return NULL;
    }
    ix = (mp->ma_keys->dk_lookup)(mp, key, hash, &value);
    if (ix == DKIX_ERROR)
        return NULL;
    if (ix == DKIX_EMPTY || value == NULL)
        Py_RETURN_FALSE;
    Py_RETURN_TRUE;
}

/*[clinic input]
dict.get

    key: object
    default: object = None
    /

Return the value for key if key is in the dictionary, else default.
[clinic start generated code]*/

static PyObject *
dict_get_impl(PyDictObject *self, PyObject *key, PyObject *default_value)
/*[clinic end generated code: output=bba707729dee05bf input=279ddb5790b6b107]*/
{
    PyObject *val = NULL;
    Py_hash_t hash;
    Py_ssize_t ix;

    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return NULL;
    }
    ix = (self->ma_keys->dk_lookup) (self, key, hash, &val);
    if (ix == DKIX_ERROR)
        return NULL;
    if (ix == DKIX_EMPTY || val == NULL) {
        val = default_value;
    }
    Py_INCREF(val);
    return val;
}

static int
dict_traverse(PyObject *op, visitproc visit, void *arg)
{
    PyDictObject *mp = (PyDictObject *)op;
    PyDictKeysObject *keys = mp->ma_keys;
    PyDictKeyEntry *entries = DK_ENTRIES(keys);
    Py_ssize_t i, n = keys->dk_nentries;

    if (keys->dk_lookup == lookdict) {
        for (i = 0; i < n; i++) {
            if (entries[i].me_value != NULL) {
                Py_VISIT(entries[i].me_value);
                Py_VISIT(entries[i].me_key);
            }
        }
    }
    else {
        if (mp->ma_values != NULL) {
            for (i = 0; i < n; i++) {
                Py_VISIT(mp->ma_values[i]);
            }
        }
        else {
            for (i = 0; i < n; i++) {
                Py_VISIT(entries[i].me_value);
            }
        }
    }
    return 0;
}

static PyObject *dictiter_new(PyDictObject *, PyTypeObject *);

static PyObject *
dict_sizeof(PyDictObject *mp, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromSsize_t(_PyDict_SizeOf(mp));
}

PyDoc_STRVAR(getitem__doc__, "x.__getitem__(y) <==> x[y]");

PyDoc_STRVAR(sizeof__doc__,
"D.__sizeof__() -> size of D in memory, in bytes");

PyDoc_STRVAR(copy__doc__,
"D.copy() -> a shallow copy of D");

PyDoc_STRVAR(keys__doc__,
             "D.keys() -> a set-like object providing a view on D's keys");
PyDoc_STRVAR(items__doc__,
             "D.items() -> a set-like object providing a view on D's items");
PyDoc_STRVAR(values__doc__,
             "D.values() -> an object providing a view on D's values");

/* Hack to implement "key in dict" */
static PySequenceMethods dict_as_sequence = {
    0,                          /* sq_length */
    0,                          /* sq_concat */
    0,                          /* sq_repeat */
    0,                          /* sq_item */
    0,                          /* sq_slice */
    0,                          /* sq_ass_item */
    0,                          /* sq_ass_slice */
    PyDict_Contains,            /* sq_contains */
    0,                          /* sq_inplace_concat */
    0,                          /* sq_inplace_repeat */
};

/* Dictionary iterator types */

typedef struct {
    PyObject_HEAD
    PyDictObject *di_dict; /* Set to NULL when iterator is exhausted */
    Py_ssize_t di_used;
    Py_ssize_t di_pos;
    PyObject* di_result; /* reusable result tuple for iteritems */
    Py_ssize_t len;
} dictiterobject;

static PyObject *
dictiter_new(PyDictObject *dict, PyTypeObject *itertype)
{
    dictiterobject *di;
    di = PyObject_GC_New(dictiterobject, itertype);
    if (di == NULL) {
        return NULL;
    }
    Py_INCREF(dict);
    di->di_dict = dict;
    di->di_used = dict->ma_used;
    di->len = dict->ma_used;
    if (itertype == &PyDictRevIterKey_Type ||
         itertype == &PyDictRevIterItem_Type ||
         itertype == &PyDictRevIterValue_Type) {
        if (dict->ma_values) {
            di->di_pos = dict->ma_used - 1;
        }
        else {
            di->di_pos = dict->ma_keys->dk_nentries - 1;
        }
    }
    else {
        di->di_pos = 0;
    }
    if (
        itertype == &PyFrozenDictIterItem_Type ||
        itertype == &PyDictRevIterItem_Type
    ) {
        di->di_result = PyTuple_Pack(2, Py_None, Py_None);
        if (di->di_result == NULL) {
            Py_DECREF(di);
            return NULL;
        }
    }
    else {
        di->di_result = NULL;
    }
    PyObject_GC_Track(di);
    return (PyObject *)di;
}

static void
dictiter_dealloc(dictiterobject *di)
{
    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(di);
    Py_XDECREF(di->di_dict);
    Py_XDECREF(di->di_result);
    PyObject_GC_Del(di);
}

static int
dictiter_traverse(dictiterobject *di, visitproc visit, void *arg)
{
    Py_VISIT(di->di_dict);
    Py_VISIT(di->di_result);
    return 0;
}

static PyObject *
dictiter_len(dictiterobject *di, PyObject *Py_UNUSED(ignored))
{
    Py_ssize_t len = 0;
    if (di->di_dict != NULL && di->di_used == di->di_dict->ma_used)
        len = di->len;
    return PyLong_FromSize_t(len);
}

PyDoc_STRVAR(length_hint_doc,
             "Private method returning an estimate of len(list(it)).");

static PyObject *
dictiter_reduce(dictiterobject *di, PyObject *Py_UNUSED(ignored));

PyDoc_STRVAR(reduce_doc, "Return state information for pickling.");

static PyMethodDef dictiter_methods[] = {
    {"__length_hint__", (PyCFunction)(void(*)(void))dictiter_len, METH_NOARGS,
     length_hint_doc},
     {"__reduce__", (PyCFunction)(void(*)(void))dictiter_reduce, METH_NOARGS,
     reduce_doc},
    {NULL,              NULL}           /* sentinel */
};

/* dictreviter */

/*[clinic input]
dict.__reversed__

Return a reverse iterator over the dict keys.
[clinic start generated code]*/

static PyObject *
dict___reversed___impl(PyDictObject *self)
/*[clinic end generated code: output=e674483336d1ed51 input=23210ef3477d8c4d]*/
{
    assert (PyAnyDict_Check(self));
    return dictiter_new(self, &PyDictRevIterKey_Type);
}

static PyObject *
dictiter_reduce(dictiterobject *di, PyObject *Py_UNUSED(ignored))
{
    _Py_IDENTIFIER(iter);
    /* copy the iterator state */
    dictiterobject tmp = *di;
    Py_XINCREF(tmp.di_dict);

    PyObject *list = PySequence_List((PyObject*)&tmp);
    Py_XDECREF(tmp.di_dict);
    if (list == NULL) {
        return NULL;
    }
    return Py_BuildValue("N(N)", _PyEval_GetBuiltinId(&PyId_iter), list);
}

/***********************************************/
/* View objects for keys(), items(), values(). */
/***********************************************/

/* The instance lay-out is the same for all three; but the type differs. */

static void
dictview_dealloc(_PyDictViewObject *dv)
{
    /* bpo-31095: UnTrack is needed before calling any callbacks */
    PyObject_GC_UnTrack(dv);
    Py_XDECREF(dv->dv_dict);
    PyObject_GC_Del(dv);
}

static int
dictview_traverse(_PyDictViewObject *dv, visitproc visit, void *arg)
{
    Py_VISIT(dv->dv_dict);
    return 0;
}

static Py_ssize_t
dictview_len(_PyDictViewObject *dv)
{
    Py_ssize_t len = 0;
    if (dv->dv_dict != NULL)
        len = dv->dv_dict->ma_used;
    return len;
}

static PyObject *
_d_PyDictView_New(PyObject *dict, PyTypeObject *type)
{
    _PyDictViewObject *dv;
    if (dict == NULL) {
        PyErr_BadInternalCall();
        return NULL;
    }
    if (!PyAnyDict_Check(dict)) {
        /* XXX Get rid of this restriction later */
        PyErr_Format(PyExc_TypeError,
                     "%s() requires a dict argument, not '%s'",
                     type->tp_name, Py_TYPE(dict)->tp_name);
        return NULL;
    }
    dv = PyObject_GC_New(_PyDictViewObject, type);
    if (dv == NULL)
        return NULL;
    Py_INCREF(dict);
    dv->dv_dict = (PyDictObject *)dict;
    PyObject_GC_Track(dv);
    return (PyObject *)dv;
}

static PyObject *
dictview_mapping(PyObject *view, void *Py_UNUSED(ignored)) {
    assert(view != NULL);
    assert(PyAnyDictKeys_Check(view)
           || PyAnyDictValues_Check(view)
           || PyAnyDictItems_Check(view));
    PyObject *mapping = (PyObject *)((_PyDictViewObject *)view)->dv_dict;
    return PyDictProxy_New(mapping);
}

static PyGetSetDef dictview_getset[] = {
    {"mapping", dictview_mapping, (setter)NULL,
     "dictionary that this view refers to", NULL},
    {0}
};

/* TODO(guido): The views objects are not complete:

 * support more set operations
 * support arbitrary mappings?
   - either these should be static or exported in dictobject.h
   - if public then they should probably be in builtins
*/

/* Return 1 if self is a subset of other, iterating over self;
   0 if not; -1 if an error occurred. */
static int
all_contained_in(PyObject *self, PyObject *other)
{
    PyObject *iter = PyObject_GetIter(self);
    int ok = 1;

    if (iter == NULL)
        return -1;
    for (;;) {
        PyObject *next = PyIter_Next(iter);
        if (next == NULL) {
            if (PyErr_Occurred())
                ok = -1;
            break;
        }
        ok = PySequence_Contains(other, next);
        Py_DECREF(next);
        if (ok <= 0)
            break;
    }
    Py_DECREF(iter);
    return ok;
}

static PyObject *
dictview_richcompare(PyObject *self, PyObject *other, int op)
{
    Py_ssize_t len_self, len_other;
    int ok;
    PyObject *result;

    assert(self != NULL);
    assert(PyAnyDictViewSet_Check(self));
    assert(other != NULL);

    if (!PyAnySet_Check(other) && !PyAnyDictViewSet_Check(other))
        Py_RETURN_NOTIMPLEMENTED;

    len_self = PyObject_Size(self);
    if (len_self < 0)
        return NULL;
    len_other = PyObject_Size(other);
    if (len_other < 0)
        return NULL;

    ok = 0;
    switch(op) {

    case Py_NE:
    case Py_EQ:
        if (len_self == len_other)
            ok = all_contained_in(self, other);
        if (op == Py_NE && ok >= 0)
            ok = !ok;
        break;

    case Py_LT:
        if (len_self < len_other)
            ok = all_contained_in(self, other);
        break;

      case Py_LE:
          if (len_self <= len_other)
              ok = all_contained_in(self, other);
          break;

    case Py_GT:
        if (len_self > len_other)
            ok = all_contained_in(other, self);
        break;

    case Py_GE:
        if (len_self >= len_other)
            ok = all_contained_in(other, self);
        break;

    }
    if (ok < 0)
        return NULL;
    result = ok ? Py_True : Py_False;
    Py_INCREF(result);
    return result;
}

static PyObject *
dictview_repr(_PyDictViewObject *dv)
{
    PyObject *seq;
    PyObject *result = NULL;
    Py_ssize_t rc;

    rc = Py_ReprEnter((PyObject *)dv);
    if (rc != 0) {
        return rc > 0 ? PyUnicode_FromString("...") : NULL;
    }
    seq = PySequence_List((PyObject *)dv);
    if (seq == NULL) {
        goto Done;
    }
    result = PyUnicode_FromFormat("%s(%R)", Py_TYPE(dv)->tp_name, seq);
    Py_DECREF(seq);

Done:
    Py_ReprLeave((PyObject *)dv);
    return result;
}

/*** dict_keys ***/

static int
dictkeys_contains(_PyDictViewObject *dv, PyObject *obj)
{
    if (dv->dv_dict == NULL)
        return 0;
    return PyDict_Contains((PyObject *)dv->dv_dict, obj);
}

static PySequenceMethods dictkeys_as_sequence = {
    (lenfunc)dictview_len,              /* sq_length */
    0,                                  /* sq_concat */
    0,                                  /* sq_repeat */
    0,                                  /* sq_item */
    0,                                  /* sq_slice */
    0,                                  /* sq_ass_item */
    0,                                  /* sq_ass_slice */
    (objobjproc)dictkeys_contains,      /* sq_contains */
};

// Create an set object from dictviews object.
// Returns a new reference.
// This utility function is used by set operations.
static PyObject*
dictviews_to_set(PyObject *self)
{
    PyObject *left = self;
    if (PyAnyDictKeys_Check(self)) {
        // PySet_New() has fast path for the dict object.
        PyObject *dict = (PyObject *)((_PyDictViewObject *)self)->dv_dict;
        if (PyAnyDict_CheckExact(dict)) {
            left = dict;
        }
    }
    return PySet_New(left);
}

static PyObject*
dictviews_sub(PyObject* self, PyObject *other)
{
    PyObject *result = dictviews_to_set(self);
    if (result == NULL) {
        return NULL;
    }

    _Py_IDENTIFIER(difference_update);
    PyObject *tmp = _PyObject_CallMethodIdObjArgs(result, &PyId_difference_update, other, NULL);
    if (tmp == NULL) {
        Py_DECREF(result);
        return NULL;
    }

    Py_DECREF(tmp);
    return result;
}

static int
dictitems_contains(_PyDictViewObject *dv, PyObject *obj);

static PyObject*
_d_PyDictView_Intersect(PyObject* self, PyObject *other)
{
    PyObject *result;
    PyObject *it;
    PyObject *key;
    Py_ssize_t len_self;
    int rv;
    int (*dict_contains)(_PyDictViewObject *, PyObject *);

    /* Python interpreter swaps parameters when dict view
       is on right side of & */
    if (!PyAnyDictViewSet_Check(self)) {
        PyObject *tmp = other;
        other = self;
        self = tmp;
    }

    len_self = dictview_len((_PyDictViewObject *)self);

    /* if other is a set and self is smaller than other,
       reuse set intersection logic */
    if (PySet_CheckExact(other) && len_self <= PyObject_Size(other)) {
        _Py_IDENTIFIER(intersection);
        return _PyObject_CallMethodIdObjArgs(other, &PyId_intersection, self, NULL);
    }

    /* if other is another dict view, and it is bigger than self,
       swap them */
    if (PyAnyDictViewSet_Check(other)) {
        Py_ssize_t len_other = dictview_len((_PyDictViewObject *)other);
        if (len_other > len_self) {
            PyObject *tmp = other;
            other = self;
            self = tmp;
        }
    }

    /* at this point, two things should be true
       1. self is a dictview
       2. if other is a dictview then it is smaller than self */
    result = PySet_New(NULL);
    if (result == NULL)
        return NULL;

    it = PyObject_GetIter(other);
    if (it == NULL) {
        Py_DECREF(result);
        return NULL;
    }

    if (PyAnyDictKeys_Check(self)) {
        dict_contains = dictkeys_contains;
    }
    /* else PyDictItems_Check(self) */
    else {
        dict_contains = dictitems_contains;
    }

    while ((key = PyIter_Next(it)) != NULL) {
        rv = dict_contains((_PyDictViewObject *)self, key);
        if (rv < 0) {
            goto error;
        }
        if (rv) {
            if (PySet_Add(result, key)) {
                goto error;
            }
        }
        Py_DECREF(key);
    }
    Py_DECREF(it);
    if (PyErr_Occurred()) {
        Py_DECREF(result);
        return NULL;
    }
    return result;

error:
    Py_DECREF(it);
    Py_DECREF(result);
    Py_DECREF(key);
    return NULL;
}

static PyObject*
dictviews_or(PyObject* self, PyObject *other)
{
    PyObject *result = dictviews_to_set(self);
    if (result == NULL) {
        return NULL;
    }

    if (_PySet_Update(result, other) < 0) {
        Py_DECREF(result);
        return NULL;
    }
    return result;
}

static PyObject *
dictitems_xor(PyObject *self, PyObject *other)
{
    assert(PyAnyDictItems_Check(self));
    assert(PyAnyDictItems_Check(other));
    PyObject *d1 = (PyObject *)((_PyDictViewObject *)self)->dv_dict;
    PyObject *d2 = (PyObject *)((_PyDictViewObject *)other)->dv_dict;

    PyObject *temp_dict;

    if (PyDict_CheckExact(d1)) {
        temp_dict = PyDict_Copy(d1);
    }
    else {
        PyObject* args = PyTuple_New(1);

        if (args == NULL) {
            return NULL;
        }

        Py_INCREF(d1);
        PyTuple_SET_ITEM(args, 0, d1);

        temp_dict = PyObject_Call((PyObject *) &PyDict_Type, args, NULL);
    }
    if (temp_dict == NULL) {
        return NULL;
    }
    PyObject *result_set = PySet_New(NULL);
    if (result_set == NULL) {
        Py_CLEAR(temp_dict);
        return NULL;
    }

    PyObject *key = NULL, *val1 = NULL, *val2 = NULL;
    Py_ssize_t pos = 0;
    Py_hash_t hash;

    while (_d_PyDict_Next(d2, &pos, &key, &val2, &hash)) {
        Py_INCREF(key);
        Py_INCREF(val2);
        val1 = _PyDict_GetItem_KnownHash(temp_dict, key, hash);

        int to_delete;
        if (val1 == NULL) {
            if (PyErr_Occurred()) {
                goto error;
            }
            to_delete = 0;
        }
        else {
            Py_INCREF(val1);
            to_delete = PyObject_RichCompareBool(val1, val2, Py_EQ);
            if (to_delete < 0) {
                goto error;
            }
        }

        if (to_delete) {
            if (_PyDict_DelItem_KnownHash(temp_dict, key, hash) < 0) {
                goto error;
            }
        }
        else {
            PyObject *pair = PyTuple_Pack(2, key, val2);
            if (pair == NULL) {
                goto error;
            }
            if (PySet_Add(result_set, pair) < 0) {
                Py_DECREF(pair);
                goto error;
            }
            Py_DECREF(pair);
        }
        Py_DECREF(key);
        Py_XDECREF(val1);
        Py_DECREF(val2);
    }
    key = val1 = val2 = NULL;

    _Py_IDENTIFIER(items);
    PyObject *remaining_pairs = _PyObject_CallMethodIdObjArgs(temp_dict,
                                                             &PyId_items, NULL);
    if (remaining_pairs == NULL) {
        goto error;
    }
    if (_PySet_Update(result_set, remaining_pairs) < 0) {
        Py_DECREF(remaining_pairs);
        goto error;
    }
    Py_DECREF(temp_dict);
    Py_DECREF(remaining_pairs);
    return result_set;

error:
    Py_XDECREF(temp_dict);
    Py_XDECREF(result_set);
    Py_XDECREF(key);
    Py_XDECREF(val1);
    Py_XDECREF(val2);
    return NULL;
}

static PyObject*
dictviews_xor(PyObject* self, PyObject *other)
{
    if (PyAnyDictItems_Check(self) && PyAnyDictItems_Check(other)) {
        return dictitems_xor(self, other);
    }
    PyObject *result = dictviews_to_set(self);
    if (result == NULL) {
        return NULL;
    }

    _Py_IDENTIFIER(symmetric_difference_update);
    PyObject *tmp = _PyObject_CallMethodIdObjArgs(result, &PyId_symmetric_difference_update, other, NULL);
    if (tmp == NULL) {
        Py_DECREF(result);
        return NULL;
    }

    Py_DECREF(tmp);
    return result;
}

static PyNumberMethods dictviews_as_number = {
    0,                                  /*nb_add*/
    (binaryfunc)dictviews_sub,          /*nb_subtract*/
    0,                                  /*nb_multiply*/
    0,                                  /*nb_remainder*/
    0,                                  /*nb_divmod*/
    0,                                  /*nb_power*/
    0,                                  /*nb_negative*/
    0,                                  /*nb_positive*/
    0,                                  /*nb_absolute*/
    0,                                  /*nb_bool*/
    0,                                  /*nb_invert*/
    0,                                  /*nb_lshift*/
    0,                                  /*nb_rshift*/
    (binaryfunc)_d_PyDictView_Intersect,/*nb_and*/
    (binaryfunc)dictviews_xor,          /*nb_xor*/
    (binaryfunc)dictviews_or,           /*nb_or*/
};

static PyObject*
dictviews_isdisjoint(PyObject *self, PyObject *other)
{
    PyObject *it;
    PyObject *item = NULL;

    if (self == other) {
        if (dictview_len((_PyDictViewObject *)self) == 0)
            Py_RETURN_TRUE;
        else
            Py_RETURN_FALSE;
    }

    /* Iterate over the shorter object (only if other is a set,
     * because PySequence_Contains may be expensive otherwise): */
    if (PyAnySet_Check(other) || PyAnyDictViewSet_Check(other)) {
        Py_ssize_t len_self = dictview_len((_PyDictViewObject *)self);
        Py_ssize_t len_other = PyObject_Size(other);
        if (len_other == -1)
            return NULL;

        if ((len_other > len_self)) {
            PyObject *tmp = other;
            other = self;
            self = tmp;
        }
    }

    it = PyObject_GetIter(other);
    if (it == NULL)
        return NULL;

    while ((item = PyIter_Next(it)) != NULL) {
        int contains = PySequence_Contains(self, item);
        Py_DECREF(item);
        if (contains == -1) {
            Py_DECREF(it);
            return NULL;
        }

        if (contains) {
            Py_DECREF(it);
            Py_RETURN_FALSE;
        }
    }
    Py_DECREF(it);
    if (PyErr_Occurred())
        return NULL; /* PyIter_Next raised an exception. */
    Py_RETURN_TRUE;
}

PyDoc_STRVAR(isdisjoint_doc,
"Return True if the view and the given iterable have a null intersection.");

static PyObject* dictkeys_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored));

PyDoc_STRVAR(reversed_keys_doc,
"Return a reverse iterator over the dict keys.");

static PyMethodDef dictkeys_methods[] = {
    {"isdisjoint",      (PyCFunction)dictviews_isdisjoint,  METH_O,
     isdisjoint_doc},
    {"__reversed__",    (PyCFunction)(void(*)(void))dictkeys_reversed,    METH_NOARGS,
     reversed_keys_doc},
    {NULL,              NULL}           /* sentinel */
};

static PyObject *
dictkeys_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored))
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyDictRevIterKey_Type);
}

/*** dict_items ***/

/* Variant of PyDict_GetItem() that doesn't suppress exceptions.
   This returns NULL *with* an exception set if an exception occurred.
   It returns NULL *without* an exception set if the key wasn't present.
*/
static PyObject *
d_PyDict_GetItemWithError(PyObject *op, PyObject *key)
{
    Py_ssize_t ix;
    Py_hash_t hash;
    PyDictObject*mp = (PyDictObject *)op;
    PyObject *value;

    if (!PyAnyDict_Check(op)) {
        PyErr_BadInternalCall();
        return NULL;
    }
    if (!PyUnicode_CheckExact(key) ||
        (hash = ((PyASCIIObject *) key)->hash) == -1)
    {
        hash = PyObject_Hash(key);
        if (hash == -1) {
            return NULL;
        }
    }

    ix = (mp->ma_keys->dk_lookup)(mp, key, hash, &value);
    if (ix < 0)
        return NULL;
    return value;
}

static int
dictitems_contains(_PyDictViewObject *dv, PyObject *obj)
{
    int result;
    PyObject *key, *value, *found;
    if (dv->dv_dict == NULL)
        return 0;
    if (!PyTuple_Check(obj) || PyTuple_GET_SIZE(obj) != 2)
        return 0;
    key = PyTuple_GET_ITEM(obj, 0);
    value = PyTuple_GET_ITEM(obj, 1);
    found = d_PyDict_GetItemWithError((PyObject *)dv->dv_dict, key);
    if (found == NULL) {
        if (PyErr_Occurred())
            return -1;
        return 0;
    }
    Py_INCREF(found);
    result = PyObject_RichCompareBool(found, value, Py_EQ);
    Py_DECREF(found);
    return result;
}

static PySequenceMethods dictitems_as_sequence = {
    (lenfunc)dictview_len,              /* sq_length */
    0,                                  /* sq_concat */
    0,                                  /* sq_repeat */
    0,                                  /* sq_item */
    0,                                  /* sq_slice */
    0,                                  /* sq_ass_item */
    0,                                  /* sq_ass_slice */
    (objobjproc)dictitems_contains,     /* sq_contains */
};

static PyObject* dictitems_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored));

PyDoc_STRVAR(reversed_items_doc,
"Return a reverse iterator over the dict items.");

static PyMethodDef dictitems_methods[] = {
    {"isdisjoint",      (PyCFunction)dictviews_isdisjoint,  METH_O,
     isdisjoint_doc},
    {"__reversed__",    (PyCFunction)dictitems_reversed,    METH_NOARGS,
     reversed_items_doc},
    {NULL,              NULL}           /* sentinel */
};

static PyObject *
dictitems_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored))
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyDictRevIterItem_Type);
}

/*** dict_values ***/

static PySequenceMethods dictvalues_as_sequence = {
    (lenfunc)dictview_len,              /* sq_length */
    0,                                  /* sq_concat */
    0,                                  /* sq_repeat */
    0,                                  /* sq_item */
    0,                                  /* sq_slice */
    0,                                  /* sq_ass_item */
    0,                                  /* sq_ass_slice */
    (objobjproc)0,                      /* sq_contains */
};

static PyObject* dictvalues_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored));

PyDoc_STRVAR(reversed_values_doc,
"Return a reverse iterator over the dict values.");

static PyMethodDef dictvalues_methods[] = {
    {"__reversed__",    (PyCFunction)dictvalues_reversed,    METH_NOARGS,
     reversed_values_doc},
    {NULL,              NULL}           /* sentinel */
};

static PyObject *
dictvalues_reversed(_PyDictViewObject *dv, PyObject *Py_UNUSED(ignored))
{
    if (dv->dv_dict == NULL) {
        Py_RETURN_NONE;
    }
    return dictiter_new(dv->dv_dict, &PyDictRevIterValue_Type);
}
