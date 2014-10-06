from toolbox import io
import toolbox
import numpy as np

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def spike(dataset, **kwargs):
	dataset['trace'][:,500] = 1
	return dataset

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
	workspace = np.zeros(500, dtype=parameters['sutype'])	
	
	#define survey geometry, ie shot and reciever points
	parameters['sx_coords'] = np.arange(500.0)[::2] + 1
	workspace['gx'] = np.arange(500.0)+1
	parameters['gx'] = np.arange(500.0)
	
	#add some more useful stuff
	workspace['ns'] = 1000
	workspace['dt'] = 1000 #* 1e-6
	parameters['dt'] = 1e-3	
	parameters['sz'] = 0
	parameters['gz'] = 0
	parameters['nx'] = workspace['gx'].size	
	return workspace, parameters
	
if __name__ == '__main__':
	workspace, param = initialise()
	spike(workspace, None, **param)
	toolbox.display(workspace, None, **param)
	

		


		
		
	
	
	

	
	
	