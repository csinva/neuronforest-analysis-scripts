import sys
sys.path.append('connectedComponents')
sys.path.append('watershed')
sys.path.append('randStats')
import numpy as np
from loadAffs import loadAffs
from pixelStats import pixelSquareError,pixelStatsForThreshold
from randStats import randStatsForThreshold
from connDefs import connectedComponents
from multiprocessing import Pool
import pickle
import time
p = 0
def evaluateFiles(root,dirs):
    print "evaluating files..."
    minStep = .0002
    initialThresholdsPixel = np.arange(.2,.9+minStep,.1)#np.arange(-.5,1.6,.4) #-0.5:0.4:1.5;
    initialThresholdsRand = np.arange(.96,1.0+minStep,.01)
    # minStep=.2
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

    numJobs = len(dirs)*max(len(initialThresholdsRand),len(initialThresholdsPixel))
    numWorkers = min(50,numJobs)
    # print "lenThresholds:",len(thresholds),"lenFiles:",len(files)
    print "Parallel Pool:",numWorkers,"numJobs:",numJobs
    global p
    p = Pool(numWorkers)

    rThresholds, rErr, rTp, rFp, rPos, rNeg, _ = evaluateFilesAtThresholds(dirs,dims,initialThresholdsRand,'rand',minStep)
    pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr = evaluateFilesAtThresholds(dirs,dims,initialThresholdsPixel,'pixel',minStep)


    minThreshIdxPixel = (int) (np.floor((len(initialThresholdsPixel)-1)/2))
    maxThresIdxPixel = (int) (np.ceil(len(pThresholds) - 1 - minThreshIdxPixel))

    minThreshIdxRand = (int) (np.floor((len(initialThresholdsRand)-1)/2))
    maxThreshIdxRand = (int) (np.ceil(len(pThresholds) - 1 - minThreshIdxRand))

    # save everything
    saveAndPrint(f,"Mean Pixel Square Error:",pSqErr)

    bestErr,bestIdx = np.min(pErr),np.argmin(pErr)
    bestThreshold = pThresholds[bestIdx]
    saveAndPrint(f,"Best Threshold for Pixel Error:",bestThreshold)
    saveAndPrint(f,"Best Pixel Error:",bestErr)

    bestErr,bestIdx = np.max(rErr),np.argmin(rErr)
    bestThreshold = rThresholds[bestIdx]
    saveAndPrint(f,"Best Threshold for Rand F-Score:",bestThreshold)
    saveAndPrint(f,"Best Rand F-Score:",bestErr)
    f.close()

    datafile = open(root+'/errData.pkl','wb')
    pickle.dump([(pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr),(minThreshIdxPixel,maxThresIdxPixel),
                 (rThresholds, rErr, rTp, rFp, rPos, rNeg),(minThreshIdxRand,maxThreshIdxRand)],datafile)
    datafile.close()

    # make plots
    # makeErrorCurves((pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr),(minThresholdIdx,maxThresholdIdx))

def evaluateFilesAtThresholds(files, dims, thresholds, randOrPixel, minStep):
    # initialize all variables
    err,tp,fp = (np.empty([len(files),len(thresholds)]) for i in range(3))
    pos,neg,pSqErr,nExamples = (np.empty([len(files),1]) for i in range(4))

    # This loop should be parallelized
    '''
    # Not parallel
    for i in range(len(files)):
        err[i,:], tp[i,:], fp[i,:], pos[i], neg[i], pSqErr[i], nExamples[i] = evaluateFileAtThresholds(files[i], thresholds, dims[i], randOrPixel)
    '''
    # Parallel implementation
    print time.clock()*60

    argsArr=[]
    for i in range(len(files)):
        for j in range(len(thresholds)):
            argsArr.append([files[i], thresholds[j], dims[i], randOrPixel])
    mappedValues = p.map(evaluateFileAtThreshold,argsArr)
    print time.clock()*60

    count = 0
    for i in range(len(files)):
        for j in range(len(thresholds)):
            err[i,j], tp[i,j], fp[i,j], pos[i], neg[i], pSqErr[i], nExamples[i] = mappedValues[count]
            count = count+1
    # aggregate statistics over all examples
    sumOverExamples = lambda x: np.sum(x*nExamples,axis=0) #todo: don't keep redefining this
    tp,fp,pos,neg = map(sumOverExamples,[tp,fp,pos,neg])

    pSqErr = np.sum(pSqErr*nExamples,axis=0)/np.sum(nExamples)
    if randOrPixel=="rand":
        prec = tp/(tp+fp)
        rec = tp/pos
        err = 2*(prec*rec)/(prec+rec) # todo: this can be done in parallel
        bestErr = np.nanmax(err)
        bestIdx = np.nanargmax(err)
    else:
        err = np.sum(err*nExamples,axis=0)/np.sum(nExamples)
        bestErr = np.nanmin(err) # todo: this is unnecessary
        bestIdx = np.nanargmin(err)


    #Call again with new thresholds, append results todo: make it load aff graph less
    step = thresholds[1] - thresholds[0]
    bestThreshold = thresholds[bestIdx]
    print "Thresholds:",thresholds[0],":",step,":",thresholds[-1],"\tBest",randOrPixel,"=",bestErr
    if step>minStep:
        newStep = 2*step/(len(thresholds)-1)
        innerThresholds=np.arange(bestThreshold-step,bestThreshold+step+minStep/100,newStep)  #this could yield slightly different results than matlab code
        if randOrPixel=="rand":
            thresholds_, err_, tp_, fp_,_,_,_ = evaluateFilesAtThresholds(files,dims,innerThresholds,'rand',minStep)
        else:
            thresholds_, err_, tp_, fp_,_,_,_ = evaluateFilesAtThresholds(files,dims,innerThresholds,'pixel',minStep)

        thresholds = np.concatenate([thresholds[0:bestIdx],thresholds_,thresholds[bestIdx+1:-1]])
        err = np.concatenate([err[0:bestIdx],err_,err[bestIdx+1:-1]])
        tp = np.concatenate([tp[0:bestIdx],tp_,tp[bestIdx+1:-1]])
        fp = np.concatenate([fp[0:bestIdx],fp_,fp[bestIdx+1:-1]])
    return thresholds,err,tp,fp,pos,neg,pSqErr

def evaluateFileAtThreshold(args):
    file,threshold,dims,randOrPixel=args
    affTrue,affEst = loadAffs(file,dims)
    nExamples = (affTrue.size)/3
    if(randOrPixel=="rand"):
        pSqErr=-1
        nhood = np.eye(3)
        compTrue = connectedComponents(affTrue,nhood).astype('d',order='F')
    else:
        pSqErr=pixelSquareError(affTrue,affEst) #todo: make this inline

    if(randOrPixel=="rand"):
        err,tp,fp,pos,neg = randStatsForThreshold(compTrue,affEst,threshold)  # this might give an error for making pos, neg nan (if(~isnan(pos_)) pos=pos_; end)
        # print threshold,tp[0,i]
    else:
        err,tp,fp,pos,neg = pixelStatsForThreshold(affTrue,affEst,threshold) #todo: pos, neg can be taken out of the loop (put with pSqErr)
    return err,tp,fp,pos,neg,pSqErr,nExamples


def saveAndPrint(file,arg,val):
    print arg,val
    file.write(arg+" "+str(val)+"\n")