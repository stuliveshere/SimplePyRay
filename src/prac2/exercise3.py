#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
import os
import matplotlib.pyplot as pylab
from exercise1 import initialise


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------
@io
def tar(dataset, **kwargs):
	gamma = kwargs['gamma']
	t = kwargs['times']
	r  = np.exp(gamma * t)
	dataset['trace'] *= r
	return dataset

	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('cdp201.su')

	params['gamma'] = 20
	tar(workspace, None, **params)
	toolbox.display(workspace, None, **params)
	pylab.show()
	
	
	
