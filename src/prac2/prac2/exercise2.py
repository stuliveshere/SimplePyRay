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

None

        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise dataset and parameter dictionary
        dataset, params = initialise('cleaned.su')
        
        # we are going to pull out 1 cdp for testing with.
        #firstly, use the scroll tool to view the cdps, and 
        #then pick one near the middle of the volume
        
        print dataset['cdp']
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        params['step'] = 20	
        #~ toolbox.display(dataset, None, **params)
        #we then want to extract that single cdp
        #for testing with later. we can do that 
        #the following way
        cdp500 = dataset[dataset['cdp'] == 500]
        toolbox.scan(cdp500)
        #view it
        #~ toolbox.display(cdp500, None, **params)
        #we have the right cdp = but the traces are in the wrong 
        #order. lets sort by offset
        
        cdp500 = np.sort(cdp500, order=['cdp', 'offset'])
                
        #output it for later
        toolbox.cp(cdp500, 'cdp500.su', None)       
        params['clip'] = 6e-4

        toolbox.display(cdp500, None, **params)
        pylab.show()
        
        
        
        
        
        
