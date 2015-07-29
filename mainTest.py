import sys
sys.path.append('connectedComponents')
sys.path.append('watershed')
sys.path.append('randStats')
from randStats import randIndex
import numpy as np
from loadAffs import loadAffs
from connDefs import connectedComponents
from waterDefs import markerWatershed
from randStats import randIndex
import time
t0 = time.clock()
dataRoot = 'dataSmall/000'
dims = [73,73,73]
affTrue, affEst = loadAffs(dataRoot,dims)
affTrue = affTrue.astype(dtype='d',order='F')
nhood = np.eye(3)
thresh=.97
affEst = affEst.astype(dtype='d',order='F')
affEstThresh=(affEst>thresh).astype(dtype='d')
comp = connectedComponents(affEstThresh,nhood).astype(dtype='d',order='F')
compTrue = connectedComponents(affTrue,nhood).astype(dtype='d',order='F')

# transpose doesn't do anything
nhood = -1*np.eye(3)
compE = np.zeros((73,73,73)).astype(dtype='d',order='F')
compT = np.zeros((73,73,73)).astype(dtype='d',order='F')

for x in range(73):
    for y in range(73):
        for z in range(73):
            compE[z,y,x]=comp[x,y,z]
            compT[z,y,x]=compTrue[x,y,z]

watershed = markerWatershed(affEst,nhood,compE,0)

# print "watershed shape:",watershed.shape
print "watershed sum:",np.sum(watershed) #this should be around 1020717

stats = randIndex(compT,watershed)
tf = time.clock()

print stats
print "ri should be about .422"
print "time:",tf-t0,"seconds"