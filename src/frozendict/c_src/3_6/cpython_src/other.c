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

#if defined(RANDALL_WAS_HERE)
#  define Py_UNREACHABLE() \
    Py_FatalError( \
        "If you're seeing this, the code is in what I thought was\n" \
        "an unreachable state.\n\n" \
        "I could give you advice for what to do, but honestly, why\n" \
        "should you trust me?  I clearly screwed this up.  I'm writing\n" \
        "a message that should never appear, yet I know it will\n" \
        "probably appear someday.\n\n" \
        "On a deep level, I know I'm not up to this task.\n" \
        "I'm so sorry.\n" \
        "https://xkcd.com/2200")
#elif defined(Py_DEBUG)
#  define Py_UNREACHABLE() \
    Py_FatalError( \
        "We've reached an unreachable state. Anything is possible.\n" \
        "The limits were in our heads all along. Follow your dreams.\n" \
        "https://xkcd.com/2200")
#elif defined(__GNUC__) && (__GNUC__ > 4 || (__GNUC__ == 4 && __GNUC_MINOR__ >= 5))
#  define Py_UNREACHABLE() __builtin_unreachable()
#elif defined(__clang__) || defined(__INTEL_COMPILER)
#  define Py_UNREACHABLE() __builtin_unreachable()
#elif defined(_MSC_VER)
#  define Py_UNREACHABLE() __assume(0)
#else
#  define Py_UNREACHABLE() \
    Py_FatalError("Unreachable C code path reached")
#endif

#if defined(__GNUC__) \
    && ((__GNUC__ >= 5) || (__GNUC__ == 4) && (__GNUC_MINOR__ >= 3))
#define _Py_HOT_FUNCTION __attribute__((hot))
#else
#define _Py_HOT_FUNCTION
#endif

