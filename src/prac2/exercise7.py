#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np
from exercise1 import initialise
import pylab

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def _lmo_calc(aoffset, velocity):
        t0 = -1.0*aoffset/velocity
        return t0
        
@io
def lmo(dataset, **kwargs):
        for index, trace in enumerate(dataset):
                aoffset = np.abs(trace['offset']).astype(np.float)
                ns = trace['ns']
                dt = trace['dt'] * 1e-6
                tx = np.linspace(dt, dt*ns, ns)
                #calculate time shift
                shift = _lmo_calc(aoffset, kwargs['lmo'])
                #turn into samples
                shift  = (shift*1000).astype(np.int)
                #roll
                result = np.roll(trace['trace'], shift)
                dataset[index]['trace'] *= 0
                dataset[index]['trace'] += result
        return dataset

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        workspace, params = initialise('cdp500.su')
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        params['lmo'] =1000.0
        toolbox.agc(workspace, None, None)
        lmo(workspace, None, **params)
        workspace['trace'][:,:30] *= 0
        workspace['trace'][:,1850:] *= 0
        params['lmo'] =-1000.0
        lmo(workspace, None, **params)
        
        toolbox.display(workspace, None, **params)
        pylab.show()

