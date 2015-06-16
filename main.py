from loadAffs import loadAffs
from pixelStats import pixelSquareError,pixelStatsForThreshold
from connectedComponents import connectedComponents
from evaluateFiles import evaluateFiles
import os

# filename = "data/000"
# dims = [73,73,73]
#
# affTrue,affEst = loadAffs(filename,dims)
# psqErr = pixelSquareError(affTrue,affEst)
# print "psqErr: ", psqErr
# p_err,p_tp,p_fp,p_pos,p_neg = pixelStatsForThreshold(affTrue,affEst,.5)
# print "p_err,p_tp,p_fp,p_pos,p_neg"
# print p_err,p_tp,p_fp,p_pos,p_neg
# connectedComponents(affTrue)
# count = 0


dataRoot = 'dataSmall'
dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
evaluateFiles(dataRoot,dirs)