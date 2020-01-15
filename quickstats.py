#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

import os, sys
import matplotlib.pyplot as plt
import time

ls = []

args = sys.argv

gui = args[1]
loop = int(args[2])


if gui == 'gui':

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)

for i in range(loop):
    pulsars = 0
    for i in os.listdir('pulsar/'):
        if i[0] == '.':
            continue
        pulsars += 1

    non = 0
    for i in os.listdir('not_pulsar/'):
        if i[0] == '.':
            continue
        non += 1

    rfi = 0
    for i in os.listdir('rfi/'):
        if i[0] == '.':
            continue
        rfi += 1

    total = pulsars+non+rfi

    print("Pulsars: "+str(pulsars))
    print("Not pulsars: "+str(non))
    print("Total: "+str(total))
    print("Filter percentage: "+str(100*pulsars/total))

    val = 100*pulsars/total
    ls += [val]

    if gui == 'gui':
        ax.clear()
        ax.plot(ls, color='red')
    ##    ax.axhline(y=val+bound)
    ##    ax.axhline(y=val-bound)
        fig.canvas.draw()
        fig.canvas.flush_events()
    time.sleep(1)

