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

None

	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	workspace, params = initialise('survey.su')
	
	cdp_gathers = np.sort(workspace, order=['cdp', 'offset'])
	cdp201 = cdp_gathers[cdp_gathers['cdp'] == 201]
	toolbox.cp(cdp201, 'cdp201.su', None)
	
	
	params['primary'] = 'cdp'
	params['secondary'] = 'offset'
	params['step'] = 20
	
	toolbox.scroll(cdp_gathers, None, **params)
	
	pylab.show()
	
	
	
