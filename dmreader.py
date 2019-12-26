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


def dmfind(img):
    dm = img[50:63, 386:620]
    dm = pytesseract.image_to_string(dm)
    newstr = ''

    for i in dm:
        if i.isdigit() or i == '.':
            newstr = newstr + i

    print("DM: "+newstr)

    try:
        if newstr[-1] == '.': #sometimes dots can end up at the end of strings
            newstr = newstr[:-1]
    except IndexError:
        newstr = '100'
    
    newstr = float(newstr)
    return newstr
