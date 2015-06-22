from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "conn.h":
    void printlist(list[int] &)

def list_test(list[int] l):
    printlist(l)

cdef extern from "conn.h":
    int printArr(double * conn)

def arr_test(np.ndarray[np.double_t,ndim=4] conn):
    x = np.ascontiguousarray(conn)
    print "test.pyx:\n",x
    printArr(<double*> conn.data)
    #printArr(&x[0])