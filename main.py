from loadAffs import loadAffs
from pixelStats import pixelSquareError,pixelStatsForThreshold
from connectedComponents import connectedComponents
from evaluateFiles import evaluateFiles
import os

dataRoot = 'dataSmall'
dirs =  [dataRoot+'/'+d for d in os.listdir(dataRoot) if os.path.isdir(os.path.join(dataRoot,d))]
evaluateFiles(dataRoot,dirs)