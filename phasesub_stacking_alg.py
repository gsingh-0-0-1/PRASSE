#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

import numpy as np, random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
import scipy.stats
import time
import PIL
from PIL import Image
import shutil
import pytesseract
import sys
from dmreader import dmfind

startdir='images/'

args = sys.argv

subbandsetting = args[1]
if args[2] == 'default': #make the default settings internal, easier for UI
    xmult = 2.75
    x_rel = 10
    ymult = 2.5
    y_rel = 35
    override = 50000
    obj_min = 10000
    gui = args[3]
else:
    xmult = float(args[2])
    x_rel = int(args[3])
    ymult = float(args[4])
    y_rel = int(args[5])
    override = float(args[6])
    obj_min = float(args[7])
    gui = args[8]
thresh = 1

if subbandsetting == 'inp':
    x1 = int(input("Enter x-value of top left corner: "))
    y1 = int(input("Enter y-value of top left corner: "))
    x2 = int(input("Enter x-value of bottom right corner: "))
    y2 = int(input("Enter y-value of bottom right corner: "))

##function definitions

def calclists(phasesubband):
    phasesubband = np.sum(255-phasesubband, axis=2)

    xlist = np.sum(phasesubband, axis=0)
    ylist = np.sum(phasesubband, axis=1)

    return xlist, ylist

def calcvals(xlist):
    xstd = np.std(xlist)
    xmean = np.mean(xlist)
    xpeak = np.amax(xlist)
    xmin = np.amin(xlist)

    return xstd, xmean, xpeak, xmin

def get_img_phasesub(fname):
    #Open image, basic initial processing
    
    try:
        img = Image.open(startdir+fname)
        img = np.array(img)
    except OSError:
        return

    #gbncc demos setting below
    if subbandsetting == 'demo':
        origphasesubband = img[200:380, 350:500]
    if subbandsetting == 'reg':
        origphasesubband = img[170:355, 320:470]
    if subbandsetting == 'none':
        origphasesubband = img
    if subbandsetting == 'inp':
        x1 = int(input("Enter first x-coordinate: "))
        x2 = int(input("Enter second x-coordinate: "))
        y1 = int(input("Enter first y-coordinate: "))
        y2 = int(input("Enter second y-coordinate: "))
        origphasesubband = img[y1:y2, x1:x2]
    if subbandsetting == 'skynet':
        img = Image.open(startdir+fname)
        img = img.resize([725, 540])
        cv2.imwrite('new.png', np.array(img))
        img = np.array(img)
        origphasesubband = img[170:355, 320:470]

    return img, origphasesubband

def x_analysis(sigpoints, xlist):
    sigpoints = sigpoints
    x_measures = []
    for ind in range(len(xlist)):
        point = xlist[ind]


        tlist = np.roll(xlist, (-ind)+x_rel)
        tlist = tlist[:x_rel*2]

        xstd = np.std(tlist)
        xmean = np.median(tlist) #X-MEAN IS ACTUALLY THE MEDIAN

        x_measures += [xmean+xstd*xmult]
        
        if point > xmean + xmult*xstd:
            sigpoints += 1

    return x_measures, sigpoints

def get_status(sigpoints, thresh, obj_min, override, xpeak, img):
    status = ''
    
    if (sigpoints >= thresh and xpeak > obj_min) or xpeak >= override:
        if subbandsetting == 'reg':
            dm = dmfind(img)
            if dm < 2:
                status = 'rfi'
            else:
                status = 'pulsar'
        else:
            status = 'pulsar'
    else:
        status = 'not_pulsar'

    return status

        
def main(fname):
    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
        return
    print(fname)
    
    img, phasesubband = get_img_phasesub(fname)

    xlist, ylist = calclists(phasesubband)

    xstd, xmean, xpeak, xmin = calcvals(xlist)

    sigpoints = 0
    
    x_measures, sigpoints = x_analysis(sigpoints, xlist)

    status = get_status(sigpoints, thresh, obj_min, override, xpeak, img)

    shutil.move(startdir+fname, status+'/'+fname)

    if gui == 'gui':
        plt.subplot(2, 2, 1)
        plt.imshow(phasesubband)

        plt.subplot(2, 2, 2)
        plt.xlabel('Pixels (Phase x 75)')
        plt.ylabel('Intensity')
        plt.plot(xlist, 'blue')
        plt.plot(x_measures, 'red')
        plt.axhline(y=override, color='orange')
        plt.axhline(y=obj_min, color='orange')
        
        plt.subplot(2, 2, 3)
        plt.axhline(y=0)
        print(len(phasesubband)*765)
        plt.axhline(y=len(phasesubband)*765)
        plt.xlabel('Pixels (Phase x 75)')
        plt.ylabel('Intensity')
        plt.plot(xlist, 'blue')

        ##plt.imshow(phasesubband)

    plt.show()


for fname in os.listdir(startdir):
    main(fname)
