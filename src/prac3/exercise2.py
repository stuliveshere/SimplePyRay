#last time we did a very simplistic velocity analysis. 
#this time we want to do a few more locations

import toolbox
import numpy as np
import pylab
pylab.rcParams['image.interpolation'] = 'sinc'

#--------------------------------------------------
#       useful functions
#-------------------------------------------------

None

if __name__ == "__main__":
        #initialise dataset
        print "initialising dataset"
        workspace, params = toolbox.initialise('stack.su')
        
        #turn off gather sort
        params['primary'] = None
        params['clip'] = 0.2
        #display check
        toolbox.display(workspace, None, **params)
        
        #do an fx spectrum, to get an idea of the frequency content
        #~ toolbox.fx(workspace, None, **params)
        
        #set bandpass
        params['lowcut'] = 20
        params['highcut'] = 100
        
        toolbox.bandpass(workspace, None, **params)
        toolbox.display(workspace, None, **params)
        
        pylab.show()
