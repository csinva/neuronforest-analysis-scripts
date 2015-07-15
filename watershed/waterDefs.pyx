from libcpp.list cimport list
import numpy as np
cimport numpy as np

cdef extern from "water.h":
    void watershed(double * conn, double * nhood,double * comp, double* growMask, double lowThreshold, int dimX,int dimY,int dimZ, double * outputComp)

def markerWatershed(np.ndarray[np.double_t,ndim=4] conn, np.ndarray[np.double_t,ndim=2] nhood, np.ndarray[np.double_t,ndim=3] comp, np.ndarray[np.double_t,ndim=3] growMask, np.double_t lowThreshold, np.ndarray[np.double_t,ndim=3] outputComp): #todo: no need for fortran array
    dims = np.shape(conn)
    print "lowThreshold:",lowThreshold
    #c = watershed(&conn[0,0,0,0], &nhood[0,0], &comp[0,0,0], &growMask[0,0,0],lowThreshold, dims[0],dims[1],dims[2],&outputComp[0,0,0])
    c = watershed(&conn[0,0,0,0], &nhood[0,0], &comp[0,0,0], &growMask[0,0,0],lowThreshold, 73,73,73,&outputComp[0,0,0])

    minW = (int) (np.min(outputComp))
    maxW = (int) (np.max(outputComp))

    print "minW",minW
    print "maxW",maxW
    sizes = []
    for i in range(minW,maxW+1):
        sizes.append(np.sum(outputComp==i))
    # print np.array(sizes)
    print np.sort(np.array(sizes))#[-10:]
    print "    219   478   945   2739   379545"
    if np.sort(np.array(sizes))[-1]==379545:
        print "SUCCESS"
    print "size:",len(sizes)
    return outputComp