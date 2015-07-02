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
    dims = np.shape(conn)
    c = printArr(&conn[0,0,0,0], &nhood[0,0],dims[0],dims[1],dims[2],&comp[0,0,0],&cmpSz)
    compOut = <int *> comp.data
    compReturn = np.zeros((dims[0],dims[1],dims[2]))

    #copy ints into compReturn #todo: return values in proper variables
    count = 0
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                 compReturn[i][j][k]= compOut[count]#(compOut[i*dims[0]+j*dims[1]+k])
                 count = count+1
                 #print(compOut[i],": ",comp.data[i])
    #cmpSz = np.zeros()
    #print "c:",c
    compReturn=compReturn.astype(int)
    reverseRenum = np.argsort(c)
    c = np.sort(c)
    #print c
    #print reverseRenum
    renum = np.zeros((len(reverseRenum)))
    dust = c>1
    #print "dust:",dust
    #print "reverseRenum:",reverseRenum
    reverseRenum=reverseRenum[dust]
    #print "c bef:",c
    c = c[dust]#np.delete(c,dust[:])
    #print "c aft:",c
    numObj = len(c)
    #print numObj
    renum[reverseRenum]=np.arange(1,numObj+1)
    # print "renum:",renum
    # print "shape:",np.shape(compReturn)
    # print "max comp:",np.max(compReturn)
    # print "min comp:",np.min(compReturn)
    #a = renum[a]
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                compReturn[i][j][k]=renum[compReturn[i][j][k]-1]

    return compReturn,c