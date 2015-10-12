#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np
from exercise1 import initialise
import pylab
import cProfile

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def _nmo_calc(tx, vels, offset):
        '''calculates the zero offset time'''
        t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
        return t0
        
@io
def nmo(workspace, **kwargs):
        it = np.nditer(workspace, flags=['f_index'])
        if 'smute' not in kwargs.keys(): kwargs['smute'] = 10000.0
        for trace in it:
                index= it.index
                aoffset = np.abs(trace['offset']).astype(np.float)
                ns = kwargs['ns']
                dt = kwargs['dt'] 
                tx = kwargs['times']
                

                #calculate time shift for each sample in trace
                t0 = _nmo_calc(tx, kwargs['vels'], aoffset)
                
                #calculate stretch between each sample
                stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
                
                #filter stretch
                filter = [(stretch >0.0) & ( stretch < kwargs['smute'])]
                values = np.interp(tx, t0[filter], trace['trace'][filter])
                values[tx < np.amin(t0[filter])] = 0.0
                values[tx > np.amax(t0[filter])] = 0.0
                
                #write corrected values back to workspace
                workspace[index]['trace'] *= 0
                workspace[index]['trace'] += values
        return workspace

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise dataset and parameter dictionary
        dataset, params = initialise('cdp500.su')
        params['primary'] = 'cdp'
        params['secondary'] = 'offset'
        
        #set stretch mute and vels
        #~ params['smute'] = 100.0
        params['vels'] = toolbox.build_vels([0.5], [800.0], ns = params['ns'])
        dataset = nmo(dataset, None, **params)

        toolbox.display(dataset, None, **params)
        pylab.show()


