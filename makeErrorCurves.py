import matplotlib.pyplot as plt
import numpy as np
from pylab import figure

def makeErrorCurves((pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr),(minThresholdIdx,maxThresholdIdx)):
    plt.close('all')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)


    labels(ax1,"Threshold","Rand F-Score","Rand F-Score")
    labels(ax2,"False Positive","True Positive","Rand Error ROC")
    ax3.plot(pThresholds,pErr)
    labels(ax3,"Threshold","Pixel Error","Pixel Error")
    ax3.set_xlim([pThresholds[minThresholdIdx], pThresholds[maxThresholdIdx]])
    #customPlot(ax3)
    ax4.plot(pFp/pNeg,pTp/pPos)
    labels(ax4,"False Positive","True Positive","Pixel Error ROC")


    plt.tight_layout()
    plt.show()

def labels(ax, x='x-label',y='y-label',title='title',fontsize=15):
    ax.set_xlabel(x, fontsize=fontsize)
    ax.set_ylabel(y, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize+10)


