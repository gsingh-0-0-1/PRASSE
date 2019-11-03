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
import pygame
import pytesseract
import sys
from crop_phase_sub import crop

startdir='images/'

args = sys.argv

subbandsetting = args[1]
xmult = float(args[2])
ymult = float(args[3])
y_rel = int(args[4])
gui = args[5]

for fname in os.listdir(startdir):
    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
        continue
    print(fname)

    #Open image, basic initial processing
    
    try:
        img = Image.open(startdir+fname)
        img.resize([780, 582])
        canvas = Image.new('RGBA', img.size, (255,255,255,255)) 
        canvas.paste(img, mask=img) 
        canvas.save(startdir+fname, format="PNG")
        img = cv2.imread(startdir+fname)
    except ValueError: #for alpha channel errors
        img = cv2.imread(startdir+fname)

    #gbncc demos setting below
    if subbandsetting == 'demo':
        phasesubband = img[200:380, 350:500]
    if subbandsetting == 'reg':
        phasesubband = img[170:370, 320:470]
    if subbandsetting == 'auto':
        phasesubband = crop(img)

    #set up x and y lists
    xlist = np.zeros(len(phasesubband[0]))
    ylist = np.zeros(len(phasesubband))

    #fill up the lists
    for y in range(len(phasesubband)):
        for x in range(len(phasesubband[y])):
            s = sum(phasesubband[y][x])
            newsum = 765 - s
            xlist[x] += newsum
            ylist[y] += newsum

    #find basic values
    xstd = np.std(xlist)
    xmean = np.mean(xlist)
    xpeak = np.amax(xlist)

    #parse input
    thresh = 1


    sigpoints = 0 #need *thresh* points above mult * std to call it a pulsar, accounting for regularities between phases

    #add to sig points based on x points peaks
    for point in xlist:
        if point > xmean + xmult*xstd:
            sigpoints += 1

    #start y list analysis
    y_measures = []
    for ind in range(len(ylist)):
        #the y-list broadband detector uses mean and standard deviations in the relative area
        #of the point rather than of the entire list, to detect horizontal lines and also account
        #for whitewashed areas of the phase subband plot                
        point = ylist[ind]
        
        bottom = ind-y_rel
        top = ind+y_rel
        while bottom < 0:
            bottom += 1
        while top > len(ylist): #not subracting 1 here since indexing excludes the finish
            top -= 1

        tlist = ylist[bottom:top]
        
        ystd = np.std(tlist)
        ymean = np.median(tlist)
        
        y_measures += [ymean+ystd*ymult]
        
        if point > ymean + ymult*ystd:
            sigpoints -= 1

    f = open('stats.txt', 'a+')

    override = 4

    if sigpoints >= thresh or xpeak >= xmean+override*xstd: #if the spike is *really* large, then count it a pulsar anyway
        shutil.move(startdir+fname, 'pulsar/'+fname)
        f.write(fname+": Pulsar\n")
    else:
        shutil.move(startdir+fname, 'not_pulsar/'+fname)
        f.write(fname+": Not a Pulsar\n")

    ##print(sigpoints)

    if gui == 'gui':
        plt.subplot(2, 1, 1)
        plt.plot(y_measures, 'red')
        plt.plot(ylist, 'blue')

        plt.subplot(2, 1, 2)
        plt.plot(xlist)
        plt.axhline(y=xmean+xmult*xstd, color='red')
        plt.axhline(y=xmean+4*xstd, color='red')
    ##plt.imshow(phasesubband)

    plt.show()
        

    
