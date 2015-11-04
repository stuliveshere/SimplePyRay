#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np
from exercise1 import initialise
import pylab
import cProfile
import sys
#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def _nmo_calc(tx, vels, offset):
        '''calculates the zero offset time'''
        t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
        return t0
        
@io
def nmo(dataset, **kwargs):
        offsets = np.unique(dataset['offset'])
        if 'smute' not in kwargs.keys(): kwargs['smute'] = 10000.
        ns = kwargs['ns']
        dt = kwargs['dt'] 
        tx = kwargs['times']
        
        for offset in offsets:
                aoffset = np.abs(offset.astype(np.float))
                #calculate time shift for each sample in trac
                t0 = _nmo_calc(tx, kwargs['vels'], aoffset)
                t0 = np.nan_to_num(t0)
                #calculate stretch between each sample
                stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
                filter = [(stretch >0.0) & ( stretch < kwargs['smute'])]
                
                inds = [dataset['offset'] == offset]
                subset = np.apply_along_axis(lambda m: np.interp(tx, t0[filter], m[filter]), axis=-1, arr=dataset['trace'][inds])
                subset[:,tx < np.amin(t0[filter])]  = 0.0
                subset[:,tx > np.amax(t0[filter])] = 0.0
                dataset['trace'][inds] = subset

        return dataset

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise dataset and parameter dictionary
        dataset, params = initialise('cdp500.su')
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        
        #set stretch mute and vels
        params['smute'] = 100.0
        params['vels'] = toolbox.build_vels([0.5], [800.0], ns = params['ns'])
        dataset = nmo(dataset, None, **params)

        toolbox.display(dataset, None, **params)
        pylab.show()


