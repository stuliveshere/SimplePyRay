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

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------
def diverge(distance, coefficient):
	'''spherical divergence correction''' 
	r = np.abs(1.0/(distance**coefficient))
	return r


@io
def build_direct(**params):
	'''
	calculates direct wave arrival time and 
	imposes it upon an array. assumes 330 m/s
	surface velocity
	'''
	directv = 330 #m/s
	direct_times = params['aoffsets']/directv
	
	#set base amplitude (from testing)
	direct_amps = np.ones_like(params['rx_coords']) * 0.01
	#calculate the spherical divergence correction
	direct_correction = diverge(params['aoffsets'], 2.0)
	#apply correction
	direct_amps *= direct_correction

	#we are not interested in anything after 1 second
	limits = [direct_times < 1]

	x = params['rx_coords'][limits]
	t = direct_times[limits]
	direct_amps = direct_amps[limits]

	#convert to coordinates
	t *= 1000 # milliseconds
	x = np.floor(x).astype(np.int)
	t = np.floor(t).astype(np.int)
	
	params['dataset'][x, t] += direct_amps
	
	#~ #check plot
	pylab.plot(x, t, '.')
	pylab.ylim(1000,0)
	pylab.show()
	
	return params['dataset']

@io	
def build_refractor(**params):
	result = params['dataset']
	return result

@io	
def build_reflectors(**params):
	result = params['dataset']
	return result
	
if __name__ == '__main__':
	param = {}
	#build our model, which is pre-defined in the toolbox
	param['model'] = toolbox.build_model()
	#have a look at it - it has a build in display routine
	#~ param['model'].display()
	
	#define survey geometry, ie shot and reciever points
	sx_coords = np.arange(500.0)[::2] + 0.5
	param['rx_coords'] = np.arange(500.0)
	
	#add some more useful stuff
	param['sz'] = 0
	param['gz'] = 0
	param['nx'] = param['rx_coords'].size
	param['ns'] = 1000
	param['dt'] = 1e-3
	
	param['sutype'] = toolbox.su.typeSU(1000)
		
	#define calculation array
	workspace = np.empty((param['nx'], param['ns']), 'f')
	
	for sx in sx_coords:
		
		#keep adding useful stuff
		param['sx'] = sx
		param['offsets'] = param['rx_coords'] - param['sx']
		param['aoffsets'] = np.abs(param['offsets'])
		
		#reset the workspace
		workspace.fill(0)
		
		#lets set up for calculating direct wave
		print build_direct(workspace, None, **param)
		#~ break
		

		
		
	
	
	

	
	
	