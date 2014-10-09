

from toolbox import io
import toolbox
import numpy as np
from exercise3 import nmo

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def _stack_gather(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	holder = dataset[0].copy()
	holder['trace'].fill(0.0)
	fold = dataset.size
	holder['trace'] += np.sum(dataset['trace'], axis=-2) /np.float(fold)
	return holder

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
	params = {}
	params['vels'] = np.ones(1000)*1500.0
	params['smute'] = 100
	workspace = nmo('cdp200.su', None, **params)
	toolbox.agc(workspace, None, None)
	toolbox.display(workspace, None, None)
	
	