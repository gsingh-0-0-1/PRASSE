#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, November 2019
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
from cnnstructure import layer, passvals
from dmreader import dmfind

startdir='images/'

args = sys.argv

subbandsetting = args[1]
thresh1 = 0
thresh2 = 40000
thresh3 = thresh2+1
thresh4 = thresh2
thresh5 = 0
thresh6 = 0
noise = 0

imgshape = [780, 582]

for fname in os.listdir(startdir):
    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
        continue
    print(fname)

    #Open image, basic initial processing
    
    try:
        img = Image.open(startdir+fname)
        img.resize(imgshape)
        canvas = Image.new('RGBA', img.size, (255,255,255,255)) 
        canvas.paste(img, mask=img) 
        canvas.save(startdir+fname, format="PNG")
        img = cv2.imread(startdir+fname)
    except ValueError: #for alpha channel errors
        img = cv2.imread(startdir+fname)
    except OSError:
        continue

    if subbandsetting == 'reg':
        y1 = 170
        y2 = 370
        x1 = 320
        x2 = 470
        origphasesubband = np.copy(img[y1:y2, x1:x2])
    if subbandsetting == 'demo':
        origphasesubband = np.copy(img[180:380, 350:500])
    if subbandsetting == 'none':
        origphasesubband = np.copy(img)

##    second = np.sum(origphasesubband, axis=2) #create a copy to determine means from
##    #necessary because numpy does not allow setting array values with a sequence
##    
##    for y in range(len(origphasesubband)):
##        m = np.mean(second[y])
####        ma = np.amax(second[y])
####        mi = np.amin(second[y])
####        m = (ma+mi)/2
##        for x in range(len(origphasesubband[y])):
##            if sum(origphasesubband[y][x]) > m:
##                origphasesubband[y][x] = [255, 255, 255]
##            else:
##                origphasesubband[y][x] = [0, 0, 0]

    phasesubband = np.sum(origphasesubband, axis=2)
    phasesubband = 765 - phasesubband

    #generate first layer, create thresholds, input
    layer1len = len(phasesubband)
    layer1wid = len(phasesubband[0])
    layer1 = layer([layer1len, layer1wid])
    layer1.genthresh(thresh1)
    layer1.inp(phasesubband)

    #generate the second layer
    layer2len = layer1wid
    layer2 = layer([layer2len])
    layer2.genthresh(thresh2)

    #generate the third layer
    layer3len = int(layer2len/2)
    layer3 = layer([layer3len])
    layer3.genthresh(thresh3)

    #generate the fourth layer
    layer4len = int(layer3len/3)
    layer4 = layer([layer4len])
    layer4.genthresh(thresh4)

    #generate the fifth layer
    layer5len = int(layer4len/5)
    layer5 = layer([layer5len])
    layer5.genthresh(thresh5)

    #generate the sixth layer
    layer6len = int(layer5len/5)
    layer6 = layer([layer6len])
    layer6.genthresh(thresh6)

    #connect the layers
    passvals(layer1, layer2, [None, '/1'])
    passvals(layer2, layer3, ['/2'])
    passvals(layer3, layer4, ['/3'])
    passvals(layer4, layer5, ['/5'])
    passvals(layer5, layer6, ['/6'])

    print(len(layer6.struc))
    finalval = layer6.struc[0]

##    plt.subplot(5, 1, 1)
##    plt.plot(layer2.struc)
##    plt.subplot(5, 1, 2)
##    plt.plot(layer3.struc)
##    plt.subplot(5, 1, 3)
##    plt.plot(layer4.struc)
##    plt.subplot(5, 1, 4)
##    plt.plot(layer5.struc)
##    plt.subplot(5, 1, 5)
##    plt.imshow(origphasesubband)
##    plt.show()

    if finalval == 0:
        shutil.move(startdir+fname, 'not_pulsar/'+fname)
    else:
        if subbandsetting == 'reg':
            dm = dmfind(img)
            if dm < 3:
                shutil.move(startdir+fname, 'not_pulsar/'+fname)
            else:
                shutil.move(startdir+fname, 'pulsar/'+fname)
        else:
            shutil.move(startdir+fname, 'pulsar/'+fname)
