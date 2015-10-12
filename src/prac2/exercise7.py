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
        offsets = np.unique(dataset['offset'])
        for offset in offsets:
                aoffset = np.abs(offset)
                shift = _lmo_calc(aoffset, kwargs['lmo'])
                shift  = (shift*1000).astype(np.int)
                inds= [dataset['offset'] == offset]
                dataset['trace'][inds] =  np.roll(dataset['trace'][inds], shift, axis=-1) #results[inds]
        return dataset

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        workspace, params = initialise('cdp500.su')
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        params['lmo'] =1000.0
        toolbox.agc(workspace, None, **params)
        lmo(workspace, None, **params)
        workspace['trace'][:,:30] *= 0
        workspace['trace'][:,1850:] *= 0
        params['lmo'] =-1000.0
        lmo(workspace, None, **params)
        
        toolbox.display(workspace, None, **params)
        pylab.show()

