import numpy as np
import scipy as sp
from collections import namedtuple
from sklearn import metrics


def randStatsForThreshold(compTrue, affEst, threshold):
    if (np.all(affEst >= threshold) or np.all(affEst < threshold)):  # check for trivial case
        return (np.nan,) * 5
    else:
        compEst = connectedComponents(affEst > threshold)
        watershed = markerWatershed(affEst, -np.eye(3), compEst)
        ri, stats = randIndex(compTrue, watershed)
        r_err = 1 - ri
        r_tp = stats.truePos
        r_fp = stats.falsePos
        r_pos = stats.pos
        r_neg = stats.neg
        # r_fscore = 2 * (stats.prec * stats.rec) / (stats.prec + stats.rec);
        return r_err, r_tp, r_fp, r_pos, r_neg


def randIndex(compTrue, compEst, normalize=False):  # todo: this can store less values
    # condition input (also shift to make positive)
    # insert line to make double and positive
    compTrue = compTrue.flatten() #don't have to add 1 for python
    compEst = compEst.flatten()  #should be 0-indexed
    maxCompTrue = np.max(compTrue)
    maxCompEst = np.max(compEst)
    print "maxCompTrue:",maxCompTrue
    print "maxCompEst:",maxCompEst

    truePos=0  #it's supposed to be same segment and is
    falsePos=0 #supposed to be different segment, but is predicted same
    trueNeg=0
    falseNeg=0
    overlap = np.zeros((maxCompTrue+1,maxCompEst+1))
    print overlap.shape
    for i in range(compTrue.size):
        overlap[(compTrue[i],compEst[i])] += 1
    # print overlap[0][0:10]
    compTrueSizes = np.sum(overlap[1:,:],axis=1)
    compEstSizes = np.sum(overlap[1:,1:],axis=0)
    print "compTrueSizes:",compTrueSizes[0:4]

    # prune out the zero component
    zeroEst = overlap[1:,1]
    overlap = overlap[1:,1:]
    indexes = np.where(overlap)
    idTrue = indexes[0]
    idEst = indexes[1]
    print "indexes shape:",idTrue.shape
    # print "indexes:",indexes[0,0:4]
    # print "indexes1:",indexes[1,0:4]
    # print "maxIndes:",np.max(indexes[:,0])
    overlapSz = np.sort(overlap[indexes])[::-1]
    print "overlapSz.shape:",overlapSz.shape
    print "overlapSz:",overlapSz[0:5]


    #not normalizing
    nPixTotal = np.sum(compTrueSizes)
    pixSz = 1/nPixTotal
    fracTrue = compTrueSizes/nPixTotal

    overlapFrac = overlapSz * pixSz
    overlap = np.zeros((overlap.shape[0]+1,overlap.shape[1]+1))
    print "overlap shape:",overlap.shape
    print "max idTrue",np.max(idTrue)
    for i in range(overlapFrac.size):
        overlap[idTrue[i],idEst[i]] += overlapFrac[i]
    print "overlap sum:",np.sum(overlap)
    print "overlap shape:",overlap.shape
    #recalculate overlap
    pos = (np.sum(fracTrue**2) - np.sum(pixSz**2 * compTrueSizes)) / 2 #these don't have to be computed, just = truePos+falseNeg
    neg = (np.sum(fracTrue)**2-np.sum(fracTrue**2)) / 2
    total = pos+neg
    truePos = np.sum(overlapFrac*(overlapFrac-pixSz))/2
    falsePos = (np.sum(np.sum(overlap,1)**2) - np.sum(np.sum(overlap**2,1)))/2

    print np.sum(overlap,1)
    #print np.sum(np.sum(overlap**2,1))

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