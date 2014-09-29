from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def spike(workspace, **params):
	workspace['trace'][:,500] = 1
	return workspace

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

def initialise():
	parameters = {}
	#build our model, which is pre-defined in the toolbox
	parameters['model'] = toolbox.build_model()
	#have a look at it - it has a build in display routine
	#~ parameters['model'].display()
	
	#initialise data workspace
	parameters['sutype'] = toolbox.typeSU(1000)
	template = np.zeros(500, dtype=parameters['sutype'])	
	
	#define survey geometry, ie shot and reciever points
	parameters['sx_coords'] = np.arange(500.0)[::2] + 1
	template['gx'] = np.arange(500.0)+1
	parameters['gx'] = np.arange(500.0)
	
	#add some more useful stuff
	template['ns'] = 1000
	template['dt'] = 1000 #* 1e-6
	parameters['dt'] = 1e-3	
	parameters['sz'] = 0
	parameters['gz'] = 0
	parameters['nx'] = template['gx'].size	
	return template, parameters
	
if __name__ == '__main__':
	workspace, param = initialise()
	spike(workspace, None, **param)
	toolbox.display(workspace, None, **param)
	

		


		
		
	
	
	

	
	
	