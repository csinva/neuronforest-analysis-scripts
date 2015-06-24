from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "conn.h":
    void printlist(list[int] &)

def list_test(list[int] l):
    printlist(l)

cdef extern from "conn.h":
    list[int] printArr(double * conn, double * nhood,int dimX,int dimY,int dimZ, double * outputComp, list[int] * l)

def arr_test(np.ndarray[np.double_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood, np.ndarray[np.double_t,ndim=3] comp, list[int] cmpSz):
    # insert in the ascontiguousarray?
    count = 0
    for x in range(25):
        #print count,conn[0][0][0][x]
        count = count+1
    #print conn[0,0,0:5,0]
    #print conn.flatten()[0:10]
    dims = np.shape(conn)
    c = printArr(<double*> conn.data, <double*> nhood.data,dims[0],dims[1],dims[2],<double*> comp.data,<list[int]*> &cmpSz)
    return c
    #return None
    #printArr(&x[0])