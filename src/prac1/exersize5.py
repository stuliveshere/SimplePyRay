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
def build_combined(workspace, **params):
	workspace = build_direct(workspace, None, **param)
	workspace = build_refractor(workspace, None, **param)
	workspace = build_reflector(workspace, None, **param)
	return workspace
	

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
	wavelet = toolbox.ricker(60)	
	workspace =  toolbox.conv(workspace, wavelet)
	toolbox.cp(workspace, 'record.su', **param)
	workspace = toolbox.agc(workspace, None, **param)
	toolbox.display(workspace, None, **param)
	
