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

None
        
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        workspace, params = initialise('survey.su')
        
        #~ #set our TAR
        #~ params['gamma'] = 10
        #~ tar(workspace, None, **params)
        
       
        #~ #apply LMO
        #~ params['lmo'] =2200.0
        #~ lmo(workspace, None, **params)
        #~ workspace['trace'][:,80:110] *= 0
        #~ params['lmo'] = -2200.0
        #~ lmo(workspace, None, **params)
        
        #~ #apply our NMO
        #~ params['smute'] = 100.0
        #~ v = [1417, 1510,1878]
        #~ t = [0.171, 0.215, 0.381]
        #~ params['vels'] = toolbox.build_vels(t, v)
        #~ nmo(workspace, None, **params)
        
        #~ #apply AGC
        #~ toolbox.agc(workspace, None, **params)
        
        #~ #stack
        #~ stack(workspace, 'stack1.su', **params)
        
        #view
        toolbox.display('stack1.su', None, **params)
        
        pylab.show()
        
        

        
        
