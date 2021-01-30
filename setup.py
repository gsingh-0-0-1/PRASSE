#* Copyright (C) Gurmehar Singh 2019 - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

'''This script will make any directories needed to get the main.py file
up and running, as well as install necessary libraries.'''

import os, subprocess, sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install('numpy')
install('matplotlib')
install('opencv-python')
install('scipy')
install('Pillow')
install('pygame')
install('pytesseract')

contents = os.listdir()

dirs_to_make = ['images', 'pulsar', 'not_pulsar', 'rfi']

for d in dirs_to_make:
    if d not in contents:
        os.mkdir(d)
