#ifndef Py_FROZENDICTOBJECT_H
#define Py_FROZENDICTOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

PyAPI_DATA(PyTypeObject) PyFrozenDict_Type;
#define PyFrozenDict_Check(op) \
                 Py_IS_TYPE(op, &PyFrozenDict_Type)

#define PyFrozenDict_CheckExact(op) Py_IS_TYPE(op, &PyFrozenDict_Type)

#define PyAnyDict_Check(ob) \
    ( \
        Py_IS_TYPE(ob, &PyDict_Type) || Py_IS_TYPE(ob, &PyFrozenDict_Type) || \
        PyType_IsSubtype(Py_TYPE(ob), &PyDict_Type) || \
        PyType_IsSubtype(Py_TYPE(ob), &PyFrozenDict_Type) \
    )

#define PyAnyDict_CheckExact(op) ( \
    (Py_IS_TYPE(op, &PyDict_Type)) || \
    (Py_IS_TYPE(op, &PyFrozenDict_Type)) \
)

PyAPI_FUNC(PyObject *) PyFrozenDict_New(PyObject* arg, PyObject* kwds);

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
