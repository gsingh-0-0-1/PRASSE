#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

'''This script will make any directories needed to get the main.py file
up and running'''

import os

contents = os.listdir()

dirs_to_make = ['images', 'pulsar', 'not_pulsar']

for d in dirs_to_make:
    if d not in contents:
        os.mkdir(d)
