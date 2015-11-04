#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
np.seterr(all='ignore')
import os
import matplotlib.pyplot as pylab
from exercise1 import initialise
from exercise3 import tar
from exercise4 import nmo
from exercise5 import _stack_gather


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def semb(workspace,**kwargs):
        vels = kwargs['velocities']
        nvels = vels.size
        ns = kwargs['ns']
        result = np.zeros((nvels,ns),'f')
        for v in range(nvels):
                panel = workspace.copy()
                kwargs['vels'] = np.ones(kwargs['ns'], 'f') * vels[v]
                nmo(panel, None, **kwargs)
                result[v,:] += np.abs(_stack_gather(panel)['trace'])
                
                
        pylab.imshow(result.T, aspect='auto', extent=(min(vels), max(vels),kwargs['ns']*kwargs['dt'],0.), cmap='gist_heat')
        pylab.xlabel('velocity')
        pylab.ylabel('time')
        pylab.colorbar()
        pylab.show()

        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        workspace, params = initialise('cdp500.su')
        velocities = np.arange(500, 4000, 100)
        params['velocities'] = velocities
        params['smute'] =30
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        #~ toolbox.agc(workspace, None, None)
        #~ semb(workspace, **params)
        v = [1000, 1510,3000]
        t = [0.214, 1.03, 1.71]
        params['vels'] = toolbox.build_vels(t, v, ns=params['ns'])
        nmo(workspace, None, **params)
        #~ 
        toolbox.display(workspace, None, **params)

        
        pylab.show()
        
        
        
