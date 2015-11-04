#restack the data with new vels 
#and the refractor muted out
from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
#~ from exercise1 import initialise
from exercise3 import tar
#~ from exercise4 import nmo
from exercise5 import stack
from exercise7 import lmo
from exercise9 import trace_mix
from exercise10 import fk


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

None
	
	
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
	#intialise workspace and parameter dictionary
	print 'initialising'
	workspace, params = toolbox.initialise('../../../../foybrook.su')
	cdp400 = workspace[workspace['cdp'] ==480]
	toolbox.agc(cdp400, None, **params)
	
	params['velocities'] = np.arange(2000,7000,50)
	toolbox.semb(cdp400,  **params)

	#set our TAR
	#~ print "applying tar"
	#~ params['gamma'] = 3
	#~ tar(workspace, None, **params)
	

	#apply LMO
	#~ print "applying lmo"
	#~ params['lmo'] =1000.0
	#~ lmo(workspace, None, **params)
	#~ workspace['trace'][:,:30] *= 0
	#~ workspace['trace'][:,1850:] *= 0
	#~ params['lmo'] = -1000.0
	#~ lmo(workspace, None, **params)
	
	#~ #apply fk
	#~ print "applying fk"
	#~ params['lmo'] =500.0
	#~ fk(workspace, None, **params)
	
	#apply our NMO
	#~ print "applying nmo"
	#~ params['smute'] = 30
	
	#~ vels = {}
	#~ vels['400'] = (0.086, 2604), (0.267, 3310), (0.59, 3891)
	#~ vels[800] = (0.0,1000.), (0.5, 2000.), (0.8, 3000.), (2.0, 5000.)
	#~ vels[100] = (0.0,200.), (0.3, 500.), (0.5, 800.), (2.0, 1000.)

	
	#~ params['vels'] = toolbox.build_vels(vels, **params)
	
	#~ workspace = toolbox.co_nmo(workspace, None, **params)
	
	#apply AGC
	#~ toolbox.agc(workspace, None, **params)
	
	#~ #apply trace mix
	#~ params['mix'] = 10
	#~ trace_mix(workspace, None, **params)
	
	#stack
	#~ print "stacking"
	#~ section = stack(workspace, None, **params)
	#~ params['lowcut'] = 30
	#~ params['highcut'] =  100
	#~ toolbox.bandpass(section, None, **params)	
	
	#~ toolbox.fx(section, None, **params)

	
	
	
	#view
	#~ params['primary'] = None
	#~ workspace = np.sort(workspace, order =['cdp', 'offset'])
	#~ toolbox.display(section, None, **params)
	
	#~ pylab.show()
	
	

	
	
