from loadAffs import loadAffs
from pixelStats import pixelSquareError

filename = "testData/000"
dims = [73,73,73]

(affTrue,affEst) = loadAffs(filename,dims)
psqErr = pixelSquareError(affTrue,affEst)
print "psqErr: ", psqErr
