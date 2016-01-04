from evaluateFiles import evaluateFiles
import os
import time

#setup list of directories
dataRoot = '../testData'
dirs = [dataRoot+'/000',dataRoot+'/001']
# dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
start = time.clock()

#calculations
numWorkers = min(50,len(dirs))
evaluateFiles(dataRoot,dirs,numWorkers)

#output
end = time.clock()
print (end-start)*60,"seconds elapsed"