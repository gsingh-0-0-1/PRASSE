#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying of this file, via any medium is strictly prohibited
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

for fname in os.listdir(startdir):
    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
        continue
    print(fname)

    try:
        img = Image.open(startdir+fname)
        canvas = Image.new('RGBA', img.size, (255,255,255,255)) 
        canvas.paste(img, mask=img) 
        canvas.save(startdir+fname, format="PNG")
        img = cv2.imread(startdir+fname)
    except ValueError: #for alpha channel errors
        img = cv2.imread(startdir+fname)

    #img = img[120:410, 300:600]

    #gbncc demos setting below
    if subbandsetting == 'demo':
        phasesubband = img[200:380, 350:500]
    if subbandsetting == 'reg':
        phasesubband = img[170:350, 320:470]
    if subbandsetting == 'auto':
        phasesubband = crop(img)
        
    xlist = np.zeros(len(phasesubband[0]))

    for y in range(len(phasesubband)):
        for x in range(len(phasesubband[y])):
            s = sum(phasesubband[y][x])
            newsum = 765 - s
            xlist[x] += newsum

    for point in range(len(xlist)):
        xlist[point] /= len(phasesubband[0])

    base = np.min(xlist)

    for point in range(len(xlist)):
        xlist[point] -= base

    std = np.std(xlist)
    mean = np.mean(xlist)

    mult = float(args[2])
    thresh = 1

    sigpoints = 0 #need *thresh* points above mult * std to call it a pulsar, accounting for regularities between phases

    for point in xlist:
        if point > mean + mult*std:
            sigpoints += 1

    f = open('stats.txt', 'a+')

    if sigpoints >= thresh:
        shutil.move(startdir+fname, 'pulsar/'+fname)
        f.write(fname+": Pulsar\n")
    else:
        shutil.move(startdir+fname, 'not_pulsar/'+fname)
        f.write(fname+": Not a Pulsar\n")

##    plt.plot(xlist)
##    plt.axhline(y=mean+mult*std, color='red')
##
##    plt.show()
        

    
