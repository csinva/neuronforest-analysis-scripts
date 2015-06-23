from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "conn.h":
    void printlist(list[int] &)

def list_test(list[int] l):
    printlist(l)

cdef extern from "conn.h":
    int printArr(double * conn, double * nhood,int dimX,int dimY,int dimZ)

def arr_test(np.ndarray[np.double_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood):
    # insert in the ascontiguousarray?
    dims = np.shape(conn)
    printArr(<double*> conn.data, <double*> nhood.data,dims[0],dims[1],dims[2])
    #printArr(&x[0])