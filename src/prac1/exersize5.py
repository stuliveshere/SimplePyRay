from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize2 import  build_direct
from exersize3 import build_refractor
from exersize4 import build_reflector

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def build_combined(dataset, **kwargs):
	dataset = build_direct(dataset, None, **kwargs)
	dataset = build_refractor(dataset, None, **kwargs)
	dataset = build_reflector(dataset, None, **kwargs)
	return dataset
	
@io
def add_noise(dataset, **kwargs):
	noise = np.random.normal(0.0, 1e-8, size=(dataset['trace'].shape))
	dataset['trace'] += noise
	return dataset
	
@io
def convolve_wavelet(dataset, **kwargs):
	wavelet = toolbox.ricker(60)	
	dataset =  toolbox.conv(dataset, wavelet)
	return dataset

if __name__ == '__main__':
	workspace, param = initialise()
	
	sx = 100

	workspace['sx'] = sx
	param['sx'] = sx
	workspace['offset'] = workspace['gx'] - workspace['sx']
	param['aoffsets'] = np.abs(workspace['offset'])
	
	#build record
	workspace = build_combined(workspace, None, **param)
	
	#build wavelet
	convolve_wavelet(workspace, 'test.su', **param)

	workspace = toolbox.agc(workspace, None, **param)
	#~ workspace = add_noise(workspace, 'record.su', **param)
	toolbox.display(workspace, None, **param)
