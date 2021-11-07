#ifndef Py_FROZENDICTOBJECT_H
#define Py_FROZENDICTOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

PyAPI_DATA(PyTypeObject) PyFrozenDict_Type;
PyAPI_DATA(PyTypeObject) PyCoold_Type;
#define PyFrozenDict_Check(op) \
    ( \
        Py_IS_TYPE(op, &PyFrozenDict_Type) \
        || PyType_IsSubtype(Py_TYPE(op), &PyFrozenDict_Type) \
    )

#define PyFrozenDict_CheckExact(op) Py_IS_TYPE(op, &PyFrozenDict_Type)

#define PyAnyFrozenDict_Check(op) \
    ( \
        Py_IS_TYPE(op, &PyFrozenDict_Type) \
        || Py_IS_TYPE(op, &PyCoold_Type) \
        || PyType_IsSubtype(Py_TYPE(op), &PyFrozenDict_Type) \
        || PyType_IsSubtype(Py_TYPE(op), &PyCoold_Type) \
    )

#define PyAnyFrozenDict_CheckExact(op) \
    ( \
        Py_IS_TYPE(op, &PyFrozenDict_Type) \
        || Py_IS_TYPE(op, &PyCoold_Type) \
    )

#define PyAnyDict_Check(ob) \
    ( \
        PyDict_Check(ob) \
        || Py_IS_TYPE(ob, &PyFrozenDict_Type) \
        || Py_IS_TYPE(ob, &PyCoold_Type) \
        || PyType_IsSubtype(Py_TYPE(ob), &PyFrozenDict_Type) \
        || PyType_IsSubtype(Py_TYPE(ob), &PyCoold_Type) \
    )

#define PyAnyDict_CheckExact(op) ( \
    (Py_IS_TYPE(op, &PyDict_Type)) \
    || (Py_IS_TYPE(op, &PyFrozenDict_Type)) \
    || (Py_IS_TYPE(op, &PyCoold_Type)) \
)

PyAPI_DATA(PyTypeObject) PyFrozenDictItems_Type;
PyAPI_DATA(PyTypeObject) PyFrozenDictIterKey_Type;
PyAPI_DATA(PyTypeObject) PyFrozenDictIterItem_Type;

#ifndef Py_LIMITED_API
#  define Py_CPYTHON_FROZENDICTOBJECT_H
#  include  "cpython/frozendictobject.h"
#  undef Py_CPYTHON_FROZENDICTOBJECT_H
#endif

#ifdef __cplusplus
}
#endif
#endif
