from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "conn.h":
    void printlist(list[int] &)

def list_test(list[int] l):
    printlist(l)

cdef extern from "conn.h":
    list[int] printArr(double * conn, double * nhood,int dimX,int dimY,int dimZ, double * outputComp, list[int] * l)

def arr_test(np.ndarray[np.double_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood, np.ndarray[np.double_t,ndim=3] comp, list[int] cmpSz): #todo: no need for fortran array
    count = 0
    for x in range(25):
        count = count+1
    dims = np.shape(conn)
    c = printArr(<double*> conn.data, <double*> nhood.data,dims[0],dims[1],dims[2],<double*> comp.data,<list[int]*> &cmpSz)
    compOut = <int *> comp.data
    for i in range(73):
        print(compOut[i])
    #cmpSz = np.zeros()
    #print "c:",c
    reverseRenum = np.argsort(c)
    c = np.sort(c)
    #print c
    #print reverseRenum
    renum = np.zeros((len(reverseRenum)))
    dust = c>1
    print "dust:",dust
    #print "reverseRenum:",reverseRenum
    reverseRenum=reverseRenum[dust]
    print "c bef:",c
    c = c[dust]#np.delete(c,dust[:])
    print "c aft:",c
    numObj = len(c)
    print numObj
    renum[reverseRenum]=np.arange(1,numObj+1)
    print "renum:",renum
    print np.shape(comp)
    print "max comp:",np.max(comp)
    print "min comp:",np.min(comp)
    #c = renum[c]
    # print "reached"
    exit(0)
    return c
    #return None
    #printArr(&x[0])