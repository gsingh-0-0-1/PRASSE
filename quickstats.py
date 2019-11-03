#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

import os, sys

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

total = pulsars+non

print("Pulsars: "+str(pulsars))
print("Not pulsars: "+str(non))
print("Total: "+str(total))
print("Filter percentage: "+str(pulsars/total))
