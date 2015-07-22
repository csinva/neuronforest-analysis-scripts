import numpy as np
cimport numpy as np
from connDefs import connectedComponents
from waterDefs import markerWatershed

def randStatsForThreshold(compTrue, affEst, threshold):
    cdef int x,y,z
    if (np.all(affEst >= threshold) or np.all(affEst < threshold)):  # check for trivial case
        return (np.nan,) * 5
    else:
        nhood = np.eye(3)
        affEstThresh=(affEst>threshold).astype(dtype='d')
        dims = np.shape(compTrue)[0:3]
        compEst = connectedComponents(affEstThresh,nhood).astype(dtype='d',order='F')
        compE = np.zeros(dims).astype(dtype='d',order='F')
        compT = np.zeros(dims).astype(dtype='d',order='F')
        for x in range(dims[0]):
            for y in range(dims[1]):
                for z in range(dims[2]):
                    compE[z,y,x]=compEst[x,y,z]
                    compT[z,y,x]=compTrue[x,y,z]

        nhoodNeg = -1*np.eye(3)
        watershed = markerWatershed(affEst,nhoodNeg,compE,0)
        stats = randIndex(compT,watershed)
        return 1-stats['ri'],stats['truePos'],stats['falsePos'],stats['pos'],stats['neg']


def randIndex(compTrue, compEst, normalize=False):  # todo: this can store less values
    # condition input (also shift to make positive)
    # insert line to make double and positive
    compTrue = compTrue.flatten() #don't have to add 1 for python
    compEst = compEst.flatten()  #should be 0-indexed
    maxCompTrue = np.max(compTrue)
    maxCompEst = np.max(compEst)

    #truePos: supposed to be same segment and is
    #falsePose: supposed to be different segment, but is predicted same

    #overlap
    cdef int i
    cdef double pos,neg,truePos,trueNeg,falsePos,falseNeg, ri
    cdef np.ndarray[double,ndim=2] overlap = np.zeros((maxCompTrue+1,maxCompEst+1))
    # print overlap.shape
    for i in range(compTrue.size):
        overlap[(compTrue[i],compEst[i])] += 1
    compTrueSizes = np.sum(overlap[1:,:],axis=1)


    # prune out the zero component
    zeroEst = overlap[1:,0]
    overlap = overlap[1:,1:]
    indexes = np.where(overlap)
    idTrue = indexes[0]
    idEst = indexes[1]

    overlapSz = np.sort(overlap[indexes])[::-1] #might not be necessary



    #not normalizing
    nPixTotal = np.sum(compTrueSizes)
    pixSz = 1/nPixTotal
    fracTrue = compTrueSizes/nPixTotal

    overlapFrac = overlapSz * pixSz
    overlapFracUnsorted = overlap[idTrue,idEst] * pixSz


    overlap = np.zeros((overlap.shape[0]+1,overlap.shape[1]+1))

    for i in range(overlapFracUnsorted.size):
        overlap[idTrue[i],idEst[i]] += overlapFracUnsorted[i]

    #recalculate overlap
    pos = (np.sum(fracTrue**2) - np.sum(pixSz**2 * compTrueSizes)) / 2
    neg = (np.sum(fracTrue)**2-np.sum(fracTrue**2)) / 2
    total = pos+neg
    truePos = np.sum(overlapFrac*(overlapFrac-pixSz))/2
    falsePos = (np.sum(np.sum(overlap,0)**2) - np.sum(np.sum(overlap**2,0)))/2
    falseNeg = np.sum((compTrueSizes-zeroEst)*zeroEst*pixSz**2) + (np.sum((zeroEst*pixSz)**2)-np.sum(pixSz**2 * zeroEst))/2 +(np.sum(np.sum(overlap,1)**2) - np.sum(np.sum(overlap**2,1)))/2
    trueNeg = (pos+neg) - (truePos+falsePos+falseNeg)

    ri = (truePos+trueNeg) / (truePos+trueNeg+falsePos+falseNeg)


    # derived statistics
    stats = {}
    stats['ri']=ri
    stats['pos']=pos
    stats['neg']=neg
    stats['truePos']=truePos
    stats['trueNeg']=trueNeg
    stats['falsePos']=falsePos
    stats['falseNeg']=falseNeg
    stats['total']=total

    return stats