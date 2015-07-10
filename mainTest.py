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
affTrue = affTrue.astype(dtype='d',order='F')
nhood = np.eye(3).astype(dtype='d')
cmpSize = []
thresh=.97


affEst = affEst.astype(dtype='d',order='F') # this has an effect
affEstThresh=(affEst>thresh).astype(dtype='d')
print "sum affEst:",np.sum(affEstThresh)
comp,cmpSize = arr_test(affTrue,nhood,compOutput,cmpSize)
LEN = min(10,cmpSize.size)
print cmpSize[0:LEN-1],'...'
print "comp sum:",np.sum(comp)



# transpose doesn't do anything
affEst = affEst.astype(dtype='d',order='F')
nhood = -1*np.eye(3).astype(dtype='d') #.transpose()
comp = comp.astype(dtype='d',order='F') #.transpose((2,0,1))
growMask= (comp==0).astype(dtype='d',order='F')
watershed = np.zeros((73,73,73)).astype(dtype='d',order='F')
print "growMask sum:",np.sum(growMask)

watershed = markerWatershed(affTrue,nhood,comp,growMask,0,watershed) #putting in affEst or affTrue doesn't matter here

print "watershed shape:",watershed.shape
print "watershed sum:",np.sum(watershed)
if np.sum(watershed)==1020717:
    print "SUCCESS"
else:
    print "FAILURE"