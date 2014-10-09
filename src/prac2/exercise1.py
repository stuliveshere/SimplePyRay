#import su files from prac1
#sort into cdp/offsets
#view a cdp gather

from toolbox import io
import toolbox
import numpy as np
import os
import matplotlib.pyplot as pylab


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def initialise(file):
	kwargs = {}
	dataset = toolbox.read(file)
	dataset['cdp'] = (dataset['gx'] + dataset['sx'])/2.
	return dataset, kwargs

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('survey.su')
	shot250 =  workspace[workspace['sx'] == 251]
	toolbox.agc(shot250, None, **params)
	toolbox.display(shot250, None, **params)
	
	cdp200 = workspace[workspace['cdp'] == 250]
	cdp200 = np.sort(cdp200, order=['cdp', 'offset'])
	toolbox.agc(cdp200, None, **params)
	toolbox.display(cdp200, None, **params)

	pylab.show()
	
	
	
