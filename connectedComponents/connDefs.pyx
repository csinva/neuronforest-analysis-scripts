from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "conn.h":
    list[int] connectedComponentsCPP(double * conn, double * nhood,int dimX,int dimY,int dimZ, double * outputComp, list[int] * l)

def connectedComponents(np.ndarray[np.double_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood): #todo: no need for fortran array
    dims = np.shape(conn)
    cdef list[int] cmpSz = []
    cdef np.ndarray[np.double_t,ndim=3] comp = np.zeros(dims[0:3])
    c = connectedComponentsCPP(&conn[0,0,0,0], &nhood[0,0],dims[0],dims[1],dims[2],&comp[0,0,0],&cmpSz)
    compReturn=comp.astype(int) #todo make it so it is int the entire time
    reverseRenum = np.argsort(c)[::-1]
    c = np.sort(c)[::-1]
    renum = np.zeros((len(reverseRenum)))
    #remove components with size less than 1
    dust = c>1
    reverseRenum=reverseRenum[dust]
    c = c[dust]
    numObj = len(c)
    renum[reverseRenum]=np.arange(1,numObj+1)

    cdef int i,j,k
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                compReturn[i][j][k]=renum[compReturn[i][j][k]-1]
    return compReturn