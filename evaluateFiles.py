import numpy as np
from loadAffs import loadAffs
from pixelStats import pixelSquareError,pixelStatsForThreshold
from makeErrorCurves import makeErrorCurves
import pickle
def evaluateFiles(root,dirs):
    print "evaluating files..."
    initialThresholds = np.arange(-.5,1.6,.4) #-0.5:0.4:1.5;
    #initialThresholds = [.5];
    minStep = .002
    f = open(root+'/errOverview.txt','w')

    # read description and dimensions
    with open(dirs[0]+'/description.txt', 'r') as f2:
        description = f2.read()
    saveAndPrint(f,"Description:",description)
    dims = np.zeros([len(dirs),3])
    for dimCount in range(len(dirs)):
        with open(dirs[dimCount]+'/dimensions.txt', 'r') as f2:
            dim = f2.read()
        dims[dimCount,:] = dim.split(" ")
        dimCount=dimCount+1

    pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr = evaluateFilesAtThresholds(dirs,dims,initialThresholds,'pixel',minStep)
    minThresholdIdx = np.floor((len(initialThresholds)-1)/2)
    maxThresholdIdx = np.ceil(len(pThresholds) - 1 - minThresholdIdx)

    # save everything
    saveAndPrint(f,"Mean Pixel Square Error:",pSqErr)

    bestErr,bestIdx = np.min(pErr),np.argmin(pErr)
    bestThreshold = pThresholds[bestIdx]
    saveAndPrint(f,"Best Threshold for Pixel Error:",bestThreshold)
    saveAndPrint(f,"Best Pixel Error:",bestErr)
    f.close()

    datafile = open(root+'/errData.pkl','wb')
    pickle.dump([(pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr),(minThresholdIdx,maxThresholdIdx)],datafile)
    #pickle.dump(min_threshold_idx,max_threshold_idx,datafile)
    datafile.close()


    # make plots
    makeErrorCurves((pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr),(minThresholdIdx,maxThresholdIdx))

    #evaluateThresholds()

def evaluateFilesAtThresholds(files, dims, thresholds, randOrPixel, minStep):
    # initialize all variables
    err = np.empty([len(files),len(thresholds)])
    tp = np.empty([len(files),len(thresholds)])
    fp = np.empty([len(files),len(thresholds)])
    pos = np.empty([len(files),1])
    neg = np.empty([len(files),1])
    pSqErr = np.empty([len(files),1])
    nExamples = np.empty([len(files),1])

    # This loop should be parallelized
    for i in range(len(files)):
        err[i,:], tp[i,:], fp[i,:], pos[i], neg[i], pSqErr[i], nExamples[i] = evaluateFileAtThresholds(files[i], thresholds, dims[i], randOrPixel)

    # aggregate statistics over all examples todo: make this one line
    tp = np.sum(tp*nExamples,axis=0)
    fp = np.sum(fp*nExamples,axis=0)
    pos = np.sum(pos*nExamples,axis=0)
    neg = np.sum(neg*nExamples,axis=0)
    pSqErr = np.sum(pSqErr*nExamples,axis=0)/np.sum(nExamples)
    if randOrPixel=="rand":
        print "rand calculation"
    else:
        err = np.sum(err*nExamples,axis=0)/np.sum(nExamples)
        bestErr = np.min(err) # todo: this is unnecessary
        bestIdx = np.argmin(err)

    print "Thresholds:",thresholds[0],":",thresholds[-1],"\tBest",randOrPixel,"=",bestErr
    #Call again with new thresholds, append results

    return thresholds,err,tp,fp,pos,neg,pSqErr
    #return -1

def evaluateFileAtThresholds(file,thresholds,dims,randOrPixel):
    affTrue,affEst = loadAffs(file,dims)
    nExamples = (affTrue.size)/3
    if(randOrPixel=="rand"):
        print "rand"
    else:
        pSqErr=pixelSquareError(affTrue,affEst) #todo: make this inline
    err = np.empty([1,len(thresholds)])
    tp = np.empty([1,len(thresholds)])
    fp = np.empty([1,len(thresholds)])
    for i in range(len(thresholds)):
        threshold = thresholds[i]
        if(randOrPixel=="rand"):
            print "rand"
        else:
            err[0,i],tp[0,i],fp[0,i],pos,neg = pixelStatsForThreshold(affTrue,affEst,threshold) #todo: pos, neg can be taken out of the loop (put with pSqErr)

    return err,tp,fp,pos,neg,pSqErr,nExamples


def saveAndPrint(file,arg,val):
    print arg,val
    file.write(arg+" "+str(val)+"\n")