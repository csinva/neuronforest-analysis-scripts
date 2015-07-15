import numpy as np
import matplotlib.pyplot as plt
from loadAffs import loadAffs
import sys
sys.path.append('connectedComponents')
sys.path.append('watershed')
from connDefs import connectedComponents
from waterDefs import markerWatershed
from randStats import randIndex
import scipy.io as sio
import time
'''
dataRoot = 'dataSmall/000'
dims = [73,73,73]
affTrue, affEst = loadAffs(dataRoot,dims)
comp = np.zeros((73,73,73))
compTrue = np.zeros((73,73,73))
affTrue = affTrue.astype(dtype='d',order='F')
nhood = np.eye(3).astype(dtype='d',order='F')
cmpSize = []
cmpSizeTrue = []
thresh=.97

affEst = affEst.astype(dtype='d',order='F') # this has an effect
affEstThresh=(affEst>thresh).astype(dtype='d')
print "sum affEst:",np.sum(affEstThresh)
comp,cmpSize = connectedComponents(affEstThresh,nhood,comp,cmpSize)
compTrue,cmpSizeTrue = connectedComponents(affTrue,nhood,compTrue,cmpSizeTrue)
LEN = min(10,cmpSize.size)
print cmpSize[0:LEN-1],'...'
print "comp sum:",np.sum(comp)

# transpose doesn't do anything
affEst = affEst.astype(dtype='d',order='F')
nhood = -1*np.eye(3).astype(dtype='d')
comp = comp.astype(dtype='d',order='F') #possible that this is already stored in memory as F, shouldn't be converted
compE = np.zeros((73,73,73)).astype(dtype='d',order='F')
compT = np.zeros((73,73,73)).astype(dtype='d',order='F')
print '--------------------ALIGNING---------------------------------------\n'
for x in range(73):
    for y in range(73):
        for z in range(73):
            compE[z,y,x]=comp[x,y,z]
            compT[z,y,x]=compTrue[x,y,z]
# affEst is properly aligned
print "sum",np.sum(affEst)
print affEst[0:10,0,0,0]
print np.sum(affEst[0,0,:,0])
#compT is properly aligned with z,y,x
print compE[0,0,0:10]
print compE[1:20,0,0]
print np.sum(compE[0,0,:])
print '-----------------------------------------------------------\n'

growMask= (compE==0).astype(dtype='d',order='F')
watershed = np.zeros((73,73,73)).astype(dtype='d',order='F')
print "growMask sum:",np.sum(growMask)

watershed = markerWatershed(affEst,nhood,compE,growMask,0,watershed)

print "watershed shape:",watershed.shape
print "watershed sum:",np.sum(watershed) #this should be around 1020717
'''

#need to test this with arrays loaded from matlab
# ri,stats = randIndex(compT,compE)
data = sio.loadmat('matscripts/randSetup.mat')
compTrue = data['compTrue']
watershed = data['watershed']
stats = randIndex(compTrue,watershed)
print stats