# function [ affTrue, affEst, dimensions ] = load_affs( file, dims )
# Takes a directory with predictions and labels, and their dimensions, returns affinity graphs
import struct
import numpy as np
def loadAffs(filename, dims):
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
  dims_ = (dims[0],dims[1],dims[2],3)
  affTrue = np.reshape(labels,dims_).astype(dtype='d',order='F')
  affEst = np.reshape(predictions,dims_).astype(dtype='d',order='F')
  return (affTrue,affEst)
  
