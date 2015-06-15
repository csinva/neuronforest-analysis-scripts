# function [ affTrue, affEst, dimensions ] = load_affs( file, dims )
# Takes a directory with predictions and labels, and their dimensions, returns affinity graphs
import struct
import numpy as np
def loadAffs(filename, dims):
  print "loading affs..."
  counter=0
  labels = np.zeros(3*np.prod(dims))
  predictions = np.zeros(3*np.prod(dims))
  with open(filename+'/labels.raw','rb') as f:
    while(True):
      chunk = f.read(4)
      if not chunk:
        break
      labels[counter] = struct.unpack('>f',chunk)[0]
      counter = counter+1
  counter=0
  with open(filename+'/predictions.raw','rb') as f:
    while(True):
      chunk = f.read(4)
      if not chunk:
        break
      predictions[counter] = struct.unpack('>f',chunk)[0]
      counter = counter+1
  dims.append(3)
  affTrue = np.reshape(labels,dims)
  affEst = np.reshape(predictions,dims)
  #print affTrue.shape
  return (affTrue,affEst)
  
