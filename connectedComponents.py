import numpy as np
# CONNECTEDCOMPONENTS	computes the connected components of a binary graph
# [comp,cmpSz] = connectedComponents(conn,nhood,sizeThreshold)
# conn			a 4d 'conn' style connectivity graph
# nhood			the neighborhood associated with the 'conn' graph giving the interpretation of the edges (default is the nearest neighbor 6-connectivity corresponding to 3 edges per voxel)
# sizeThreshold	objects that have as many voxels or fewer than this threshold are treated as 'dust' and removed from the connected components output
#
# comp			the output connected components labeling (sorted in descending order of size)
# cmpSz			the sizes of each component

def connectedComponents(conn,nhood1=False,nhood2=False,sizeThreshold=1):
    print 'calculating connected components...'

    if not nhood2:
        nhood2 = -np.identity(conn.ndim-1) #This had another line

    if not nhood1:
        # nhood1 = np.zeros(nhood2.shape)
        calculateConnectedComponents(conn,nhood2)
    else:
        calculateConnectedComponents(conn,nhood1,nhood2)


    # print nhood1
    # print nhood2

    # do some calculateions and get comp, cmpsz

    # remove dust


def calculateConnectedComponents(conn,nhood):
    return -1