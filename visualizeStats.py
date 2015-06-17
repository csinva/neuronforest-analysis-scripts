import pickle
from makeErrorCurves import makeErrorCurves
dataFile = open("dataSmall/errData.pkl",'rb')
pData = pickle.load(dataFile)
# print pData
makeErrorCurves(pData[0],pData[1])
dataFile.close()
