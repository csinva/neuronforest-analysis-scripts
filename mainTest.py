import numpy as np
import matplotlib.pyplot as plt
from loadAffs import loadAffs
import sys
sys.path.append('cythonTest')
from connDefs import list_test
from connDefs import arr_test

dataRoot = 'dataSmall/000'
dims = [73,73,73]
affTrue, affEst = loadAffs(dataRoot,dims)
compOutput = np.zeros((73,73,73))
#list_test(dims)
#print compOutput[0,0,0:5]
# affTrue = np.transpose(affTrue) #this will get it to return and then error
affTrue = np.asfortranarray(affTrue)
# affTrue = affTrue.astype(dtype='d',order='F')
# print affEst[0,0,0:5,0]
nhood = -1*np.eye(3)
nhood = nhood.astype(dtype='d',order='F')
cmpSize = []
cmpSize = arr_test(affTrue,nhood,compOutput,cmpSize)
print cmpSize
print "returned"
# print "outputs..."
# print compOutput[0,0,0:5]
# print cmpSize
