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

dirs = ['pulsar/', 'not_pulsar/']

for d in dirs:
    items = os.listdir(d)
    for item in items:
        if item[0] == '.':
            continue
        shutil.move(d+item, 'images/'+item)
