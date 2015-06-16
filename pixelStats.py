import numpy as np
def pixelSquareError(affTrue,affEst):
  err=0
  print "calculating pixel error..."
  affTrue = affTrue.flatten()
  affEst = affEst.flatten()
  err = np.dot((affEst-affTrue).transpose(),(affEst-affTrue)) / len(affEst)
  #print len(affEst)
  #err = np.subtract(affTrue,affEst).transpose() 
  return err

def pixelStatsForThreshold(affTrue,affEst,threshold):
  print "calculating pixel stats for threshold..."
  affTrue = affTrue.flatten()
  affEst = affEst.flatten()
  p_err = 1-np.sum((affEst>threshold)==affTrue)/((float)(len(affEst)))
  p_tp = np.sum(np.logical_and(affEst>threshold,affTrue))
  p_fp = np.sum(np.logical_and(affEst>threshold,np.logical_not(affTrue)))
  p_pos = np.sum(affTrue)
  p_neg = np.sum(np.logical_not(affTrue))
  return p_err,p_tp,p_fp,p_pos,p_neg