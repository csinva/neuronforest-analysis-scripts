from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "water.h":
    void watershed(double * conn, double * nhood,double * comp, double* growMask, double lowThreshold, int dimX,int dimY,int dimZ, double * outputComp)

def markerWatershed(np.ndarray[np.float_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood, np.ndarray[np.double_t,ndim=3] comp, np.ndarray[np.double_t,ndim=3] growMask, np.double_t lowThreshold, np.ndarray[np.double_t,ndim=3] outputComp): #todo: no need for fortran array
    dims = np.shape(conn)
    print "lowThreshold:",lowThreshold
    c = watershed(&conn[0,0,0,0], &nhood[0,0], &comp[0,0,0], &growMask[0,0,0],lowThreshold, dims[0],dims[1],dims[2],&outputComp[0,0,0])
    compOut = <int *> outputComp.data
    compReturn = np.zeros((dims[0],dims[1],dims[2]))
    return compReturn