#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
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
		kwargs['vels'] = np.ones(1000, 'f') * vels[v]
		nmo(panel, None, **kwargs)
		toolbox.agc(panel, None, None)
		result[v,:] += np.abs(_stack_gather(panel)['trace'])
		
		
	pylab.imshow(result.T, aspect='auto', extent=(min(vels), max(vels),1.,0.), cmap='spectral')
	pylab.xlabel('velocity')
	pylab.ylabel('time')
	pylab.colorbar()
	pylab.show()

	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('cdp201.su')
	velocities = np.arange(800, 4000, 50)
	params['velocities'] = velocities
	params['smute'] = 100
	semb(workspace, **params)
	v = [1417, 1510,1878]
	t = [0.171, 0.215, 0.381]
	params['vels'] = toolbox.build_vels(t, v)
	nmo(workspace, None, **params)
	toolbox.agc(workspace, None, None)
	toolbox.display(workspace, None, None)

	
	pylab.show()
	
	
	
