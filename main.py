from evaluateFiles import evaluateFiles
import os
from time import clock,time
dataRoot = 'data'
dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
# dirs = [dataRoot+'/000',dataRoot+'/001']
t0 = clock()
t0time = time()
time = evaluateFiles(dataRoot,dirs)
tf = clock()
tftime = time()
print tf-t0,"seconds elapsed"
print tftime-t0time,"seconds elapsed"