import pickle
from makeErrorCurves import makeErrorCurves
dataFile = open("../data_network/errData.pkl",'rb')
pData = pickle.load(dataFile)
print pData[0][0]
makeErrorCurves(pData[0],pData[1],pData[2],pData[3])
dataFile.close()
