

from toolbox import io
import toolbox
import numpy as np
from exercise3 import tar
from exercise4 import nmo
from exercise1 import initialise
import pylab

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def stack_gather(gather):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	gather['trace'][0] = np.mean(gather['trace'], axis=-2)
	return gather[0]

@io	
def stack(dataset, **kwargs):
	cdps = np.unique(dataset['cdp'])
	sutype = np.result_type(dataset)
	result = np.zeros(cdps.size, dtype=sutype)
	for index, cdp in enumerate(cdps):
		gather = dataset[dataset['cdp'] == cdp]
		trace = _stack_gather(gather)
		result[index] = trace
	return result
	
if __name__ == '__main__':
	workspace, params = initialise('survey.su')
	params['vels'] = np.ones(1000)*1500.0
	params['smute'] = 100
	params['gamma'] = 10
	params['clip'] = 1e-5
	
	tar(workspace, None, **params)
	nmo(workspace, None, **params)
	

	section = stack(workspace, None, **params)
	toolbox.display(section, None, **params)
	
	pylab.show()
	
	