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
        #intialise workspace and parameter dictionary
        workspace, params = initialise('survey.su')
        
        # we are going to pull out 1 cdp for testing with.
        #firstly, use the scroll tool to view the cdps, and 
        #then pick one near the middle of the volume
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        params['step'] = 20	
        #toolbox.scroll(workspace, None, **params)
        
        #we then want to extract that single cdp
        #for testing with later. we can do that 
        #the following way
        cdp201 = workspace[workspace['cdp'] == 201]
        #view it
        #toolbox.agc(cdp201, None ,**params)
        #toolbox.display(cdp201, None, **params)
        
        #we have the right cdp = but the traces are in the wrong 
        #order. lets sort by offset
        
        cdp201 = np.sort(cdp201, order=['cdp', 'offset'])
        #toolbox.display(cdp201, None, **params)
        
        #output it for later
        toolbox.cp(cdp201, 'cdp201.su', None)       
        
        
        pylab.show()
        
        
        
