static const unsigned int BitLengthTable[32] = {
    0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
};

unsigned int _Py_bit_length(unsigned long d) {
   unsigned int d_bits = 0;
   while (d >= 32) {
       d_bits += 6;
       d >>= 6;
   }
   d_bits += BitLengthTable[d];
   return d_bits;
}

typedef struct {
    uintptr_t _gc_next;
    uintptr_t _gc_prev;
} PyGC_Head;

#define _Py_AS_GC(o) ((PyGC_Head *)(o)-1)
#define _PyObject_GC_IS_TRACKED(o) (_Py_AS_GC(o)->_gc_next != 0)

#define _PyObject_GC_MAY_BE_TRACKED(obj) \
    (PyObject_IS_GC(obj) && \
        (!PyTuple_CheckExact(obj) || _PyObject_GC_IS_TRACKED(obj)))

#define PySet_CheckExact(op) Py_IS_TYPE(op, &PySet_Type)

