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

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------
def diverge(distance, coefficient=3.0):
	'''spherical divergence correction''' 
	r = np.abs(1.0/(distance**coefficient))
	return r

	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

@io
def build_direct(workspace, **params):
	'''
	calculates direct wave arrival time and 
	imposes it upon an array. assumes 330 m/s
	surface velocity
	'''

	directv = 330.0 #m/s
	direct_times = params['aoffsets']/directv
	
	#set base amplitude (from testing)
	direct_amps = np.ones_like(params['gx']) * 0.01
	#calculate the spherical divergence correction
	direct_correction = diverge(params['aoffsets'], 2.0)
	#apply correction
	direct_amps *= direct_correction
	direct_amps[~np.isfinite(direct_amps)] = 0.01
	
	#we are not interested in anything after 1 second
	limits = [direct_times < 1]
	x = params['gx'][limits]
	t = direct_times[limits]
	direct_amps = direct_amps[limits]
	


	#convert to coordinates
	t *= 1000 # milliseconds
	x = np.floor(x).astype(np.int)
	t = np.floor(t).astype(np.int)
	
	workspace['trace'][x, t] += direct_amps
	return workspace


	
if __name__ == '__main__':
	workspace, param = initialise()
	
	sx = 100

	workspace['sx'] = sx
	workspace['offset'] = workspace['gx'] - workspace['sx']
	param['aoffsets'] = np.abs(workspace['offset'])
	

	#lets set up for calculating direct wave
	build_direct(workspace, 'direct.su', **param)
	tmp = toolbox.agc('direct.su', None, **param)
	toolbox.display(tmp, None, **param)

		

		
		
	
	
	

	
	
	