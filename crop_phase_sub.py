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

startdir = 'images/'

for fname in os.listdir(startdir):
    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
        continue

    print(fname)

    #get the image open, crop it but with a lot of "legroom" or buffer
    img = Image.open(startdir+fname)
    img.resize([780, 582])
    img.save(startdir+fname)
    img = cv2.imread(startdir+fname)

    img = img[120:400, 300:600]

    xlist = np.zeros(len(img[0]))

    ylist = np.zeros(len(img))

    #get the xlist sums
    for y in range(len(img)):
        for x in range(len(img[0])):
            s = sum(img[y][x])
            newsum = 765 - s
            xlist[x] += newsum

    #get the ylist sums
    for y in range(len(img[0])):
        for x in range(len(img)):
            s = sum(img[x][y])
            newsum = 765 - s
            ylist[x] += newsum

    plt.plot(ylist)
    plt.show()
    #extract values to crop image

    #first x index
    xmax = np.amax(xlist)
    xind1 = np.where(xlist == xmax)[0][0]
    #xind1 = xlist.index(xmax) 
    xlist[xind1] = 0 #set max to 0, then we extract second-highest value

    #second x index
    xmax = np.amax(xlist)
    xind2 = np.where(xlist == xmax)[0][0]
    #xind2 = xlist.index(xmax)

    #first y index
    ymax = np.amax(ylist)
    yind1 = np.where(ylist == ymax)[0][0]
    #yind1 = ylist.index(ymax)
    ylist[yind1] = 0

    #second y index
    ymax = np.amax(ylist)
    yind2 = np.where(ylist == ymax)[0][0]
    while abs(yind1-yind2) < 75:     
        ymax = np.amax(ylist)
        yind2 = np.where(ylist == ymax)[0][0]
        ylist[yind2] = 0
    #yind2 = ylist.index(ymax)

    xvals = [xind1, xind2]
    yvals = [yind1, yind2]
    xvals.sort()
    yvals.sort()

    print(xvals, yvals)

    img = img[yvals[0] : yvals[1], xvals[0] : xvals[1]]
    
    plt.imshow(img)
    plt.show()
    #plt.imshow(img)
