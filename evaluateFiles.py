import sys
sys.path.append('connectedComponents')
sys.path.append('watershed')
sys.path.append('randStats')
sys.path.append('pixelStats')
import numpy as np
from loadAffs import loadAffs
from pixelStats import pixelSquareError,pixelStatsForThreshold
from randStats import randStatsForThreshold
from connDefs import connectedComponents
from multiprocessing import Pool
import pickle
import time
p=0
t0=0
def evaluateFiles(root,dirs):
    minStep = .005
    initialThresholdsPixel = np.arange(.2,.9+minStep,.1)#np.arange(-.5,1.6,.4) #-0.5:0.4:1.5;
    initialThresholdsRand = np.arange(.96,1.0+minStep,.01)

    # read description and dimensions
    with open(dirs[0]+'/description.txt', 'r') as f2:
        description = f2.read()
    f = open(root+'/errOverview.txt','w')
    saveAndPrint(f,"Description:",description)
    dims = np.zeros([len(dirs),3])
    for dimCount in range(len(dirs)):
        with open(dirs[dimCount]+'/dimensions.txt', 'r') as f2:
            dim = f2.read()
        dims[dimCount,:] = dim.split(" ")

    # set up parallel pool
    numWorkers = min(50,len(dirs))
    global t0
    t0=time.time()
    global p
    p = Pool(numWorkers)
    print "Parallel Pool:",numWorkers


    pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr = evaluateFilesAtThresholds(dirs,dims,initialThresholdsPixel,'pixel',minStep)
    rThresholds, rErr, rTp, rFp, rPos, rNeg, _ = evaluateFilesAtThresholds(dirs,dims,initialThresholdsRand,'rand',minStep)

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

    bestErr,bestIdx = np.nanmax(rErr),np.nanargmax(rErr)
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

    # Parallel implementation
    argsArr=[]
    for i in range(len(files)):
        argsArr.append([files[i], thresholds, dims[i], randOrPixel])
    mappedValues = p.map(evaluateFileAtThresholds,argsArr)
    for i in range(len(files)):
        err[i,:], tp[i,:], fp[i,:], pos[i], neg[i], pSqErr[i], nExamples[i] = mappedValues[i]

    # aggregate statistics over all examples
    sumOverExamples = lambda x: np.sum(x*nExamples,axis=0)
    tp,fp,pos,neg = map(sumOverExamples,[tp,fp,pos,neg])

    pSqErr = np.sum(pSqErr*nExamples,axis=0)/np.sum(nExamples)
    if randOrPixel=="rand":
        prec = tp/(tp+fp)
        rec = tp/pos
        err = 2*(prec*rec)/(prec+rec)
        bestErr,bestIdx = np.nanmax(err),np.nanargmax(err)
    else:
        err = np.sum(err*nExamples,axis=0)/np.sum(nExamples)
        bestErr,bestIdx = np.nanmin(err),np.nanargmin(err)

    #Call again with new thresholds, append results
    step = thresholds[1] - thresholds[0]
    bestThreshold = thresholds[bestIdx]
    print "Thresholds:",thresholds[0],":",step,":",thresholds[-1],"\tBest",randOrPixel,"=",bestErr
    print "time:",time.time()-t0,"seconds"
    global t0
    t0 = time.time()
    if step>minStep:
        newStep = 2*step/(len(thresholds))
        innerThresholds=np.arange(bestThreshold-step,bestThreshold+step+minStep/100,newStep)  #this could yield slightly different results than matlab code
        if randOrPixel=="rand":
            thresholds_, err_, tp_, fp_,_,_,_ = evaluateFilesAtThresholds(files,dims,innerThresholds,'rand',minStep)
        else:
            thresholds_, err_, tp_, fp_,_,_,_ = evaluateFilesAtThresholds(files,dims,innerThresholds,'pixel',minStep)
        insertInMiddle = lambda x,x_: np.concatenate([x[0:bestIdx],x_,x[bestIdx+1:-1]])
        thresholds,err,tp,fp = map(insertInMiddle,[thresholds,err,tp,fp],[thresholds_,err_,tp_,fp_])

    return thresholds,err,tp,fp,pos,neg,pSqErr

def evaluateFileAtThresholds(args):
    file,thresholds,dims,randOrPixel=args
    affTrue,affEst = loadAffs(file,dims)
    nExamples = (affTrue.size)/3
    if(randOrPixel=="rand"):
        pSqErr=-1
        nhood = np.eye(3)
        compTrue = connectedComponents(affTrue,nhood).astype('d',order='F')
    else:
        pSqErr=pixelSquareError(affTrue,affEst) #todo: make this inline

    err,tp,fp = (np.empty([1,len(thresholds)]) for i in range(3))

    for i in range(len(thresholds)):
        threshold = thresholds[i]
        if(randOrPixel=="rand"):
            err[0,i],tp[0,i],fp[0,i],pos,neg = randStatsForThreshold(compTrue,affEst,threshold)  # this might give an error for making pos, neg nan (if(~isnan(pos_)) pos=pos_; end)
            # print threshold,tp[0,i]
        else:
            err[0,i],tp[0,i],fp[0,i],pos,neg = pixelStatsForThreshold(affTrue,affEst,threshold) #todo: pos, neg can be taken out of the loop (put with pSqErr)

    return err,tp,fp,pos,neg,pSqErr,nExamples


def saveAndPrint(file,arg,val):
    print arg,val
    file.write(arg+" "+str(val)+"\n")