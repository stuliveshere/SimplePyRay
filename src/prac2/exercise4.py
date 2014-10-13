#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np
from exercise1 import initialise
import pylab

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def _nmo_calc(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
@io
def nmo(dataset, **kwargs):
	for index, trace in enumerate(dataset):
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
		
		#write corrected values back to dataset
		dataset[index]['trace'] *= 0
		dataset[index]['trace'] += values
	return dataset
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('cdp201.su')
	params['smute'] = 100.0
	params['vels'] = np.ones(1000, 'f') * 1500.0
	nmo(workspace, None, **params)
	
	
	toolbox.agc(workspace, None, None)
	toolbox.display(workspace, None, None)
	pylab.show()


