# These are a set of functions to aid viewing of 3D EM images and their
# associated affinity graphs

import os
import time

import numpy as np
import pylab
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.pyplot as plt
import h5py

#from analysis import *


## Just to access the images...
data_folder = 'nobackup/turaga/data/fibsem_medulla_7col/trvol-250-1-h5/'
os.chdir('/.')

#Open training data
f = h5py.File(data_folder + 'img_normalized.h5', 'r')
data_set = f['main']

#Open training labels
g = h5py.File(data_folder + 'groundtruth_aff.h5', 'r')
label_set = g['main']

#Displays three images: the raw data, the corresponding labels, and the predictions
def display(raw, label, pred, im_size):
    fig = plt.figure()
    ax1 = fig.add_subplot(1,3,1)
    ax2 = fig.add_subplot(1,3,2)
    ax3 = fig.add_subplot(1,3,3)
    fig.subplots_adjust(left=0.25, bottom=0.25)
    depth0 = 0
    zoom0 = 250
    
    #All these images are in gray-scale
    plt.gray()
    im1 = ax1.imshow(raw[0,:,:])
    ax1.set_title('raw image')
    
    im2 = ax2.imshow(label[0,0,:,:])
    ax2.set_title('groundtruth')
    
    im3 = ax3.imshow(pred[0,0,:,:])
    ax3.set_title('prediction')     
    
    axcolor = 'blue'
    axdepth = fig.add_axes([0.25, 0.3, 0.65, 0.03], axisbg=axcolor)
    #axzoom  = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

    depth = Slider(axdepth, 'Min', 0, 250, valinit=depth0)
    #zoom = Slider(axmax, 'Max', 0, 250, valinit=max0)
    
    def update(val):
        zlayer = int(depth.val)
        im1.set_data(raw[zlayer,:,:])
        im2.set_data(label[0,zlayer,:,:])
        im3.set_data(pred[0,zlayer,:,:])
        fig.canvas.draw()
    depth.on_changed(update)
    #smax.on_changed(update)
    
    plt.show()

display(data_set, label_set, label_set, 250)
