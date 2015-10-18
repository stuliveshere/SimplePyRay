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
from exercise9 import trace_mix
from exercise10 import fk


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

None
        
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        print 'initialising'
        workspace, params = initialise('survey.su')

  
        
        #set our TAR
        print "applying tar"
        params['gamma'] = 3
        tar(workspace, None, **params)
        
       
        #apply LMO
        print "applying lmo"
        params['lmo'] =1000.0
        lmo(workspace, None, **params)
        workspace['trace'][:,:30] *= 0
        workspace['trace'][:,1850:] *= 0
        params['lmo'] = -1000.0
        lmo(workspace, None, **params)
        
        #~ #apply fk
        #~ print "applying fk"
        #~ params['lmo'] =500.0
        #~ fk(workspace, None, **params)
        
        #apply our NMO
        print "applying nmo"
        params['smute'] = 30
        v = [1000, 1510,3000]
        t = [0.214, 1.03, 1.71]
        params['vels'] = toolbox.build_vels(t, v, ns=params['ns'])
        nmo(workspace, None, **params)
        
        #apply AGC
        toolbox.agc(workspace, None, **params)
        
        #apply trace mix
        params['mix'] = 10
        trace_mix(workspace, None, **params)
        
        #stack
        print "stacking"
        stack(workspace, 'stack1.su', **params)
        
        #view
        params['primary'] = None
        toolbox.display('stack1.su', None, **params)
        
        pylab.show()
        
        

        
        
