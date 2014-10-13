#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
import os
import matplotlib.pyplot as pylab
import pprint


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def initialise(file):
	kwargs = {}
	dataset = toolbox.read(file)
	dataset['cdp'] = (dataset['gx'] + dataset['sx'])/2.
	kwargs['ns'] = 1000
	kwargs['dt'] = 0.001
	kwargs['times'] = np.linspace(0.001, 1.0, 1000)
	return dataset, kwargs
	




	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('survey.su')
	params['primary'] = 'sx'
	params['secondary'] = 'gx'
	params['step'] = 20
	
	toolbox.scan(workspace)
	
	toolbox.scroll(workspace, None, **params)
	
	pylab.show()
	
	
	
