import numpy as np
import scipy as sp
from collections import namedtuple


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
    compTrue = compTrue.flatten()
    compEst = compEst.flatten()
    maxCompTrue = np.max(compTrue)
    maxCompEst = np.max(compEst)

    # compute the overlap or confusion matrix
    # this computes the fraction of each true component
    # overlapped by an estimated component
    # the sparse() is used to compute a histogram over object pairs
    overlap = sp.sparse(compTrue, compEst, 1, maxCompTrue, maxCompEst);

    # compute the effective sizes of each set of objects
    # computing it from the overlap matrix normalizes the sizes
    # of each set of objects to the intersection of assigned space
    compTrueSizes = np.full(np.sum(overlap[2:-1, :], 2))
    compEstSizes = np.full(np.sum(overlap[2:-1, 2:-1], 1))

    # derived statistics
    stats = namedtuple('stats', 'total', 'pos', 'neg', 'prec', 'rec', 'posEst', 'negEst', 'truePos', 'falsePos','trueNeg', 'falseNeg', 'truePosRate', 'falsePosRate', 'mergeRate', 'splitRate','clusteringError')
    stats.clusteringError = (falsePos + falseNeg) / total
    ri = 1 - stats.clusteringError

    stats.total = total
    stats.truePosRate = truePos / pos
    stats.falsePosRate = falsePos / neg
    stats.prec = truePos / posEst
    stats.rec = stats.truePosRate
    stats.mergeRate = falsePos / pos
    stats.splitRate = falseNeg / negEst

    stats.truePos = truePos
    stats.falsePos = falsePos
    stats.trueNeg = trueNeg
    stats.falseNeg = falseNeg

    stats.pos = pos
    stats.neg = neg
    stats.posEst = posEst
    stats.negEst = negEst

    return ri, stats