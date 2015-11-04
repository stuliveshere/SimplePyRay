#spectral analysis, bandpass filters
#test a few filters to find the best

import toolbox
import numpy as np
import pylab

#--------------------------------------------------
#       useful functions
#-------------------------------------------------

None

if __name__ == "__main__":
        #initialise dataset
        print "initialising dataset"
        workspace, params = toolbox.initialise('stack100.su')
        params['primary'] = None

        #basic spectral analysis
        #~ toolbox.fx(workspace, None, **params)
        
        params['highcut'] = 100
        params['lowcut'] = 30
        
        toolbox.bandpass(workspace, None, **params)
        toolbox.display(workspace, None, **params)
        
        pylab.show()
        
