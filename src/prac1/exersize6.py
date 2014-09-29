from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize5 import build_combined, add_noise, convolve_wavelet

if __name__ == "__main__":
	workspace, param = initialise()
	
	output = np.zeros(0, dtype=param['sutype'])
	
	for sx in param['sx_coords']:
		print sx
		workspace['sx'] = sx
		param['sx'] = sx
		workspace['offset'] = workspace['gx'] - workspace['sx']
		param['aoffsets'] = np.abs(workspace['offset'])	
		workspace['trace'].fill(0)
		workspace = build_combined(workspace, None, **param)
		workspace = convolve_wavelet(workspace, None, **param)
		workspace = add_noise(workspace, None, **param)
		output = np.hstack([output, workspace])
		#need to add cdp locations to workspace
	toolbox.cp(output, 'survey.su', **param)
		
		