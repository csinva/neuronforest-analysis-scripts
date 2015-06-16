import matplotlib.pyplot as plt

def makeErrorCurves((pThresholds, pErr, pTp, pFp, pPos, pNeg, pSqErr)):
    plt.close('all')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    customPlot(ax1)
    customPlot(ax2)

    #customPlot(ax3)
    customPlot(ax4)
    plt.tight_layout()
    plt.show()
    ax3.plot(pThresholds,pErr)
    '''
    subplot(2,2,3);
    plot(p_thresholds, p_err);
    title('Pixel Error');
    xlabel('Threshold');
    ylabel('Pixel Error');
    xlim([p_thresholds(min_threshold_idx), p_thresholds(max_threshold_idx)]);
    ylim([0, 1]);

    subplot(2,2,4);
    plot(p_fp/p_neg, p_tp/p_pos);
    title('Pixel Error ROC');
    xlabel('False Positive');
    ylabel('True Positive');
    xlim([0, 1]);
    ylim([0, 1]);
    '''

def customPlot(ax, x='x-label',y='y-label',title='title',fontsize=15):
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel(x, fontsize=fontsize)
    ax.set_ylabel(y, fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize+10)


