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

startdir='images/'

args = sys.argv

subbandsetting = args[1]
if args[2] == 'default': #make the default settings internal, easier for UI
    xmult = 2.8
    x_rel = 20
    ymult = 2.5
    y_rel = 42
    override = 40000
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

##function definitions

def calclists(phasesubband):
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

    return xlist, ylist

def calcvals(xlist):
    xstd = np.std(xlist)
    xmean = np.mean(xlist)
    xpeak = np.amax(xlist)
    xmin = np.amin(xlist)

    return xstd, xmean, xpeak, xmin
    

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
    if subbandsetting == 'none':
        phasesubband = img
    if subbandsetting == 'inp':
        x1 = int(input("Enter first x-value: "))
        x2 = int(input("Enter second x-value: "))
        y1 = int(input("Enter first y-value: "))
        y2 = int(input("Enter second y-value: "))
        phasesubband = img[y1:y2, x1:x2]

    xlist, ylist = calclists(phasesubband)

    #find basic values
##    xstd = np.std(xlist)
##    xmean = np.mean(xlist)
##    xpeak = np.amax(xlist)
##    xmin = np.amin(xlist)

    xstd, xmean, xpeak, xmin = calcvals(xlist)

    sigpoints = 0 #need *thresh* points above mult * std to call it a pulsar, accounting for regularities between phases
    
    #add to sig points based on x points peaks
    x_measures = []
    for ind in range(len(xlist)):
        point = xlist[ind]

        bottom = ind-x_rel
        top = ind+x_rel

        while bottom < 0:
            bottom += 1
        while top > len(xlist):
            top -= 1

        tlist = xlist[bottom:top]

        xstd = np.std(tlist)
        xmean = np.median(tlist) #X-MEAN IS ACTUALLY THE MEDIAN

        x_measures += [xmean+xstd*xmult]
        
        if point > xmean + xmult*xstd:
            sigpoints += 1

    #start y list analysis
    y_measures = []
    persist = 1 #to stop a thick line from counting as too many points
    current_p = 0
    for ind in range(len(ylist)):
        if current_p > 0:
            current_p -= 1
            continue #make use of the threshold here
        point = ylist[ind]
        
        bottom = ind-y_rel
        top = ind+y_rel
        
        while bottom < 0:
            bottom += 1
        while top > len(ylist): #not subracting 1 here since indexing excludes the finish
            top -= 1

        tlist = ylist[bottom:top]
        
        ystd = np.std(tlist)
        ymean = np.mean(tlist)
        
        y_measures += [ymean+ystd*ymult]
        
        if point > ymean + ymult*ystd:
            sigpoints -= 1
            current_p = persist

    f = open('stats.txt', 'a+')

    
    if (sigpoints >= thresh and xmin > obj_min) or xpeak >= override:
        shutil.move(startdir+fname, 'pulsar/'+fname)
        f.write(fname+": Pulsar\n")
    else:
        shutil.move(startdir+fname, 'not_pulsar/'+fname)
        f.write(fname+": Not a Pulsar\n")

    print(sigpoints)

    if gui == 'gui':
        plt.subplot(2, 2, 1)
        plt.plot(y_measures, 'red')
        plt.plot(ylist, 'blue')

        plt.subplot(2, 2, 2)
        plt.plot(xlist, 'blue')
        plt.plot(x_measures, 'red')
        plt.axhline(y=override, color='red')
        plt.axhline(y=obj_min, color='red')
        
        plt.subplot(2, 2, 3)
        plt.axhline(y=0)
        plt.axhline(y=len(xlist)*765)
        plt.plot(xlist, 'blue')

        ##plt.imshow(phasesubband)

    plt.show()
        

    
