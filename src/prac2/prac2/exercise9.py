#restack the data with new vels 
#and the refractor muted out
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
def trace_mix(dataset, **kwargs):
        ns = kwargs['ns']
        window = np.ones(kwargs['mix'], 'f')/kwargs['mix']
        for i in range(ns):
                dataset['trace'][:,i] = np.convolve(dataset['trace'][:,i], window, mode='same')
        return dataset
                
        
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        workspace, params = initialise('stack1.su')
        params['mix'] = 10
        trace_mix(workspace, None, **params)
        toolbox.display(workspace, None, **params)
        pylab.show()
        

        
        

        
        
