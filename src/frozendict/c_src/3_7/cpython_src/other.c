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

#define Py_IS_TYPE(op, type) (Py_TYPE(op) == type)

#define PySet_CheckExact(op) Py_IS_TYPE(op, &PySet_Type)

