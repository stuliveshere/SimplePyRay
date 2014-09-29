# in prac 1 we will build a synthetic shot record. 
# it will compose of 3 separate components
#	direct wave
#	refracted wave
#	reflected wave
# based up on a predefined model.

from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize2 import diverge


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def refract(x, v0, v1, z0):
	ic = np.arcsin(v0/v1)
	t0 = 2.0*z0*np.cos(ic)/v0
	t = t0 + x/v1
	return t
	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

@io
def build_refractor(workspace, **params):
	'''
	builds refractor
	'''
	
	#some shortcuts
	v0 = params['model']['vp'][0]
	v1 = params['model']['vp'][1]
	z0 = params['model']['dz'][0]
	
	refraction_times = refract(params['aoffsets'], v0, v1, z0)

	#create amplitude array
	refract_amps = np.ones_like(params['gx']) * 0.01
	#calculate the spherical divergence correction
	refract_correction = diverge(params['aoffsets'], 2.0)
	#apply correction
	refract_amps *= refract_correction
	refract_amps[~np.isfinite(refract_amps)] = 0.01

	#it probably wont exceed 1s, but to make it look right we 
	#need to limit it so that it doesnt cross over the direct
	directv = 330.0 #m/s
	direct_times = params['aoffsets']/directv
	limits = [refraction_times < direct_times]
	x = params['gx'][limits]
	t = refraction_times[limits]
	refract_amps = refract_amps[limits]

	#convert coordinates to integers
	x = np.floor(x).astype(np.int)
	t *= 1000 # milliseconds
	t = np.floor(t).astype(np.int)

	workspace['trace'][x, t] += refract_amps
	return workspace


	
if __name__ == '__main__':
	workspace, param = initialise()
	
	sx = 100

	workspace['sx'] = sx
	workspace['offset'] = workspace['gx'] - workspace['sx']
	param['aoffsets'] = np.abs(workspace['offset'])
	

	build_refractor(workspace, 'refractor.su', **param)
	tmp = toolbox.agc('refractor.su', None, **param)
	toolbox.display(tmp, None, **param)

		

		
		
	
	
	

	
	
	