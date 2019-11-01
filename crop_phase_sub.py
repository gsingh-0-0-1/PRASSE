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

startdir = 'images/'

def crop(img):
#for fname in os.listdir(startdir):
##    if fname[0] == '.' or fname == 'temp.png' or 'single' in fname:
##        continue
##
##    #get the image open, crop it but with a lot of "legroom" or buffer
##    img = Image.open(startdir+fname)
##    img.resize([780, 582])
##    img.save(startdir+fname)
##    img = cv2.imread(startdir+fname)

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
    for y in range(len(img)):
        for x in range(len(img[0])):
            s = sum(img[y][x])
            newsum = 765 - s
            ylist[y] += newsum         

    #extract values to crop image

    #first x index
    xmax = np.amax(xlist)
    xind1 = np.where(xlist == xmax)[0][0]
    xlist[xind1] = 0 #set max to 0, then we extract second-highest value

    #second x index
    xmax = np.amax(xlist)
    xind2 = np.where(xlist == xmax)[0][0]

    #first y index
    ymax = np.amax(ylist)
    yind1 = np.where(ylist == ymax)[0][0]
    ylist[yind1] = 0

    #second y index
    ymax = np.amax(ylist)
    yind2 = np.where(ylist == ymax)[0][0]

    xcheck = 0
    while abs(xind1 - xind2) < 100:
        if xcheck >= 10:
            break
        xlist[xind2] = 0
        xmax = np.amax(xlist)
        xind2 = np.where(xlist == xmax)[0][0]
        xcheck += 1

    ycheck = 0
    while abs(yind1 - yind2) < 180:
        if ycheck >= 10:
            break
        ylist[yind2] = 0
        ymax = np.amax(ylist)
        yind2 = np.where(ylist == ymax)[0][0]
        ycheck += 1

    xvals = [xind1, xind2]
    yvals = [yind1, yind2]
    xvals.sort()
    yvals.sort()

    img = img[yvals[0]+3 : yvals[1]-3, xvals[0]+3 : xvals[1]-3]

    return img
