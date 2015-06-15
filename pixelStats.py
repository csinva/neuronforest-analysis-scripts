import numpy as np
def pixelSquareError(affTrue,affEst):
  err=0
  print "calculating pixel error..."
  affTrue = np.ravel(affTrue)
  affEst = np.ravel(affEst)
  err = np.dot((affEst-affTrue).transpose(),(affEst-affTrue)) / len(affEst)
  #print len(affEst)
  #err = np.subtract(affTrue,affEst).transpose() 
  return err

def pixelStatsForThreshold(affTrue,affEst,threshold):
  return 3