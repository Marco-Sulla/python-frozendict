#ifndef Py_CPYTHON_FROZENDICTOBJECT_H
#  error "this header file must not be included directly"
#endif

typedef struct {
    PyObject_HEAD
    
    Py_ssize_t ma_used;
    uint64_t ma_version_tag;
    PyDictKeysObject* ma_keys;
    PyObject** ma_values;
    
    Py_hash_t _hash;
    short _hash_calculated;
} PyFrozenDictObject;
