import numpy, random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import cv2
import pygame
import os
import sys
import scipy.stats
import time
import PIL
from PIL import Image
import shutil
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import io
import getpass
 
user = requests.Session()

arglist = sys.argv
arglist[1] = int(arglist[1]) #where to start
arglist[2] = int(arglist[2]) #iterations
savedir = arglist[3]

print('sys.argv is', sys.argv)

url = 'http://psrsearch.wvu.edu/psc/index.php/'
url2 = "http://psrsearch.wvu.edu/psc/"

user.get(url)

username = input("Enter username: ")
password = getpass.getpass()
print(username)
payload = {"username": username, "password": password, "submit": "Sign in"}

resp = user.post(url, data=payload)

resp1 = user.get('http://psrsearch.wvu.edu/psc/skymap.php')
resp1 = resp1.text

resp1 = resp1.replace("preview.php?datasetID", '', arglist[1])
resp1 = resp1.replace(">View", '', arglist[1])

for i in range(arglist[2]):
    dataset = resp1[resp1.index("preview.php?datasetID"):resp1.index('''>View''')]
    resp1 = resp1.replace(dataset+">View", '')
    print(dataset)
    dataset = user.get(url2+dataset)
    dataset = dataset.content
    dataset = str(dataset)
    dataset = dataset[0:dataset.index("SinglePulse")]
    while "display_plot.php?" in dataset:
        index = dataset.index("display_plot.php?")
        plot = dataset[index:index+35]
        plot = plot[0:plot.index(">")]
        dataset = dataset.replace(plot, '')
        plot = user.get(url2+plot)
        plot = plot.content
        plot = str(plot)
        plot = plot[plot.index('''/results'''):plot.index('''class="fft"''')]
        plot = plot[0:plot.index('''"''')]
        plot = plot.replace("/results/", '')
        print(plot)

        plot1 = user.get('http://psrsearch.wvu.edu/psc/results/'+plot)
        im = Image.open(io.BytesIO(plot1.content))
        plot = plot.replace("/", "@")
        im.save(savedir+plot)
