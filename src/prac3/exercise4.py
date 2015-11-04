#spherical divergence correction

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
        workspace, params = toolbox.initialise('foybrook.su')
        
        #find our test CDP
        #~ print np.unique(workspace['cdp'])
        
        #extract it
        cdp = workspace[workspace['cdp'] == 396]
        
        #display it
        #~ toolbox.display(cdp, None, **params)
        
        params['gamma'] = 6
        toolbox.tar(cdp, None, **params)
        
        #display it
        toolbox.display(cdp, None, **params)
        pylab.show()