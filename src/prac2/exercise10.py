#we need a velocity filter

from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exercise1 import initialise
from exercise3 import tar
from exercise4 import nmo
from exercise5 import stack
from exercise7 import lmo

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def fk(dataset, **kwargs):
        test =  np.fft.rfft2(dataset['trace'])
        c =  test.shape[0]/2
        #y = mx + c
        x = np.arange(test.shape[1])
        m = kwargs['test']
        y = m*x + c
        filter = 
        coords = zip(x,y)
        for i in coords:
                test[i[0],:i[1]] = 0
        pylab.imshow(np.abs(test), aspect='auto')
        #~ dataset['trace'] = np.fft.irfft2(test)
        #~ return dataset
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        print 'initialising'
        workspace, params = initialise('cdp500.su')
        params['test'] = 30.0
        fk = fk(workspace, None, **params)
        
        #~ 
        #~ params['primary'] = None
        #~ toolbox.display(fk, None, **params)
        pylab.show()
