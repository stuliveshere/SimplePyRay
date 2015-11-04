#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
import os
import matplotlib.pyplot as pylab
from exercise1 import initialise


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------
@io
def tar(data, **kwargs):
        #pull some values out of the
        #paramter dictionary
        gamma = kwargs['gamma']
        t = kwargs['times']
        
        #calculate the correction coeffieicnt
        r  = np.exp(gamma * t)
        
        #applyt the correction to the data
        data['trace'] *= r
        return data

        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise dataset and parameter dictionary
        dataset, params = initialise('cdp500.su')
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'

        #set the value of gamma you want to test here
        params['gamma'] = 3
        #and apply
        tar(dataset, None, **params)
        
        toolbox.display(dataset, None, **params)
        toolbox.cp(dataset, "tar.su", **params)
        pylab.show()
        
        
        
