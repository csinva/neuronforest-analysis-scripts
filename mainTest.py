import numpy as np
import matplotlib.pyplot as plt
from loadAffs import loadAffs
import sys
sys.path.append('cythonTest')
from test import list_test
from test import arr_test
# a = np.array([[1,2,3],[2,3,4]])
# b = np.array([[1,0,0],[0,1,1]])
#
# print (a.flatten()>2)
# print (b.flatten())
#
#       #==b.flatten()
# #a = np.ravel(a)
# print a.flatten()
#
# print np.sum(b.flatten())
#
# initialThresholds = np.arange(-.5,.5,.4)
# print initialThresholds

'''
def example_plot(ax, fontsize=12):
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)

plt.close('all')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
example_plot(ax1)
example_plot(ax2)
example_plot(ax3)
example_plot(ax4)
plt.tight_layout()
plt.show()
'''
dataRoot = 'dataSmall/000'
dims = [73,73,73]
affTrue, affEst = loadAffs(dataRoot,dims)
#list_test(dims)
arr_test(affTrue,np.eye(3))