#* Copyright (C) Gurmehar Singh - All Rights Reserved
#* Unauthorized copying or distribution of this file, via any medium is strictly prohibited
#* Proprietary and confidential
#* Written by Gurmehar Singh <gurmehar@gmail.com>, October 2019
#*/

import numpy as np

#********#********#********#********#********#********#********#
#********#********#CLASS DEFINITIONS#********#********#********#
#********#********#********#********#********#********#********#

class neuron:
    def __init__(self, thresh):
        self.thresh = thresh
        self.val = None

    def reset(self):
        self.val = None

    def inp(self, val):
        self.val = val

    def pval(self):
        print(self.val)

class layer:
    def __init__(self, shape):
        self.shape = shape
        self.struc = np.zeros(shape)
        
    def regenerate(self):
        del self.struc
        self.struc = np.zeros(shape)

    def inp(self, arr):
        if np.shape(arr) == np.shape(self.struc):
            pass
        else:
            raise Exception("Shape of input is not same as shape of layer.")

        self.struc = arr

    def genthresh(self, thresh):
        self.thresh = np.full(self.shape, thresh)
            
        
def passvals(layer1, layer2, transformation): #layer1, layer2, then a list of transformations to find the index to pass the value to
    if len(transformation) == len(np.shape(layer1)):
        pass
    else:
        raise Exception("Length of transformations is not equal to number of dimensions in first array.")
    
    for idx in np.ndindex(np.shape(layer1.struc)):
        newind = []
        for ind in range(len(idx)):
            if transformation[ind] == None:
                continue
            else:
                newind += [int( eval( str(idx[ind]) + transformation[ind] ) )]

        newind = tuple(newind)
        if layer1.struc[idx] > layer1.thresh[idx]:
            layer2.struc[newind] += layer1.struc[idx]
            
        

#********#********#********#********#********#********#********#
