#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np

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
	cdp200 = toolbox.cp('cdp200.su', None, None)
	params = {}
	params['lmo'] =2200.0
	toolbox.agc(cdp200, None, None)
	lmo(cdp200, None, **params)
	cdp200['trace'][:,80:110].fill(0)
	params['lmo'] =-2000.0
	lmo(cdp200, None, **params)
	
	toolbox.display(cdp200, None, None)

