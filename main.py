from evaluateFiles import evaluateFiles
import os
import time

dataRoot = 'dataSmall'
# dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
dirs = [dataRoot+'/000']
start = time.clock()
evaluateFiles(dataRoot,dirs)
end = time.clock()
print (end-start),"seconds elapsed"