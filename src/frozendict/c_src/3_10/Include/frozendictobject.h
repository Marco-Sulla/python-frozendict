#ifndef Py_FROZENDICTOBJECT_H
#define Py_FROZENDICTOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

// PyAPI_DATA(PyTypeObject) PyFrozenDict_Type;
/*
frozendict is a heap type, so there is no static object whose address could identify it.
On the contrary, frozendict_dealloc is static. For subclasses we have to walk on the MRO.
*/
#define PyFrozenDict_TypeCheckExact(tp) \
    ((tp)->tp_dealloc == (destructor)frozendict_dealloc)

#define PyFrozenDict_CheckExact(op) PyFrozenDict_TypeCheckExact(Py_TYPE(op))

#define PyFrozenDict_Check(op) PyFrozenDict_TypeCheck(Py_TYPE(op))

#define PyAnyDict_Check(ob) (PyDict_Check(ob) || PyFrozenDict_Check(ob))

#define PyAnyDict_CheckExact(op) \
    (PyDict_CheckExact(op) || PyFrozenDict_CheckExact(op))

// PyAPI_DATA(PyTypeObject) PyFrozenDictIterKey_Type;
static PyTypeObject PyFrozenDictIterKey_Type;
// PyAPI_DATA(PyTypeObject) PyFrozenDictIterValues_Type;
static PyTypeObject PyFrozenDictIterValue_Type;
// PyAPI_DATA(PyTypeObject) PyFrozenDictIterItem_Type;
static PyTypeObject PyFrozenDictIterItem_Type;

// PyAPI_DATA(PyTypeObject) PyFrozenDictKeys_Type;
static PyTypeObject PyFrozenDictKeys_Type;
// PyAPI_DATA(PyTypeObject) PyFrozenDictValues_Type;
static PyTypeObject PyFrozenDictValues_Type;
// PyAPI_DATA(PyTypeObject) PyFrozenDictItems_Type;
static PyTypeObject PyFrozenDictItems_Type;

#define PyAnyDictKeys_Check(op) (PyDictKeys_Check(op) || PyObject_TypeCheck(op, &PyFrozenDictKeys_Type))
#define PyAnyDictValues_Check(op) (PyDictValues_Check(op) || PyObject_TypeCheck(op, &PyFrozenDictValues_Type))
#define PyAnyDictItems_Check(op) (PyDictItems_Check(op) || PyObject_TypeCheck(op, &PyFrozenDictItems_Type))
/* This excludes Values, since they are not sets. */
# define PyAnyDictViewSet_Check(op) \
    (PyAnyDictKeys_Check(op) || PyAnyDictItems_Check(op))

#ifndef Py_LIMITED_API
#  define Py_CPYTHON_FROZENDICTOBJECT_H
#  include  "cpython/frozendictobject.h"
#  undef Py_CPYTHON_FROZENDICTOBJECT_H
#endif

static void frozendict_dealloc(PyFrozenDictObject *mp);

/* PyType_IsSubtype, with the tp_dealloc identity in place of the address
   of a static type */
static inline int PyFrozenDict_TypeCheck(PyTypeObject *tp) {
    if (PyFrozenDict_TypeCheckExact(tp)) {
        return 1;
    }

    /* no static type can inherit from a heap type */
    if (! PyType_HasFeature(tp, Py_TPFLAGS_HEAPTYPE)) {
        return 0;
    }

    PyObject *mro = tp->tp_mro;

    if (mro != NULL) {
        const Py_ssize_t n = PyTuple_GET_SIZE(mro);

        for (Py_ssize_t i = 1; i < n; i++) {
            if (PyFrozenDict_TypeCheckExact(
                (PyTypeObject *)PyTuple_GET_ITEM(mro, i)
            )) {
                return 1;
            }
        }

        return 0;
    }

    /* a type that is not ready yet has no MRO: follow tp_base */
    for (tp = tp->tp_base; tp != NULL; tp = tp->tp_base) {
        if (PyFrozenDict_TypeCheckExact(tp)) {
            return 1;
        }
    }

    return 0;
}

#ifdef __cplusplus
}
#endif
#endif
