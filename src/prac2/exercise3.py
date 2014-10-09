#write a function which will flatten a cdp

from toolbox import io
import toolbox
import numpy as np

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
		ns = trace['ns']
		dt = trace['dt'] * 1e-6
		tx = np.linspace(dt, dt*ns, ns)
		t0 = _nmo_calc(tx, kwargs['vels'], aoffset)
		stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
		filter = [(stretch >0.0) & ( stretch < kwargs['smute'])]
		values = np.interp(tx, t0[filter], trace['trace'][filter])
		values[tx < np.amin(t0[filter])] = 0.0
		values[tx > np.amax(t0[filter])] = 0.0
		dataset[index]['trace'] *= 0
		dataset[index]['trace'] += values
	return dataset
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	cdp200 = toolbox.cp('cdp200.su', None, None)
	params = {}
	params['smute'] = 100.0
	params['vels'] = np.ones(1000, 'f') * 1500.0
	nmo_cdp = nmo(cdp200, None, **params)
	
	
	toolbox.agc(nmo_cdp, None, None)
	toolbox.display(nmo_cdp, None, None)


