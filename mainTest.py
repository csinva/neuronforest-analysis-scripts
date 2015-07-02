import numpy as np
import matplotlib.pyplot as plt
from loadAffs import loadAffs
import sys
sys.path.append('connectedComponents')
sys.path.append('watershed')
from connDefs import arr_test
from waterDefs import markerWatershed

dataRoot = 'dataSmall/000'
dims = [73,73,73]
affTrue, affEst = loadAffs(dataRoot,dims)
compOutput = np.zeros((73,73,73))
affTrue = np.asfortranarray(affTrue)
affEst = np.asfortranarray(affEst)

nhood = np.eye(3).astype(dtype='d',order='F')
cmpSize = []
thresh=.97

affEst=(affEst>thresh).astype('float')
comp,cmpSize = arr_test(affEst,nhood,compOutput,cmpSize)
print cmpSize
print "comp size:",np.shape(comp)
print "comp max:",np.max(comp)
print "comp min:",np.min(comp)


nhood = np.eye(3).astype(dtype='d',order='F')
#growMask = comp==0
#growMask=growMask.astype('float',order='F')

growMask=np.zeros((73,73,73))
lowThreshold=0.0
watershed = np.zeros((73,73,73))
comp = comp.astype('float')
watershed = markerWatershed(affEst,nhood,comp,growMask,lowThreshold,watershed)
# print "outputs..."
# print compOutput[0,0,0:5]
# print cmpSize
