from toolbox import io
import toolbox
import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize5 import build_combined, add_noise, convolve_wavelet

def run(sx):
	dataset, kwargs = initialise()
	print sx
	dataset['sx'] = sx
	kwargs['sx'] = sx
	dataset['offset'] = dataset['gx'] - dataset['sx']
	kwargs['aoffsets'] = np.abs(dataset['offset'])	
	dataset['trace'].fill(0)
	dataset = build_combined(dataset, None, **kwargs)
	dataset = convolve_wavelet(dataset, None, **kwargs)
	dataset = add_noise(dataset, None, **kwargs)
	#need to add cdp locations to dataset
	toolbox.cp(dataset[::2], 'shot%d.su' %sx, **kwargs)	

if __name__ == "__main__":
	workspace, param = initialise()
	pool = Pool(processes=8)
	result = pool.map(run, param['sx_coords'])
	#workspace = toolbox.agc('shot201.su', None, None)
	#toolbox.display(workspace, None, None)

		
		