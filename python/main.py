from evaluateFiles import evaluateFiles
import os
import time

dataRoot = 'data'
dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
# dirs = [dataRoot+'/000',dataRoot+'/001']
start = time.clock()
evaluateFiles(dataRoot,dirs)
end = time.clock()
print (end-start)*60,"seconds elapsed"