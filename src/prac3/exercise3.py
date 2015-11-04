#processing a real dataset
#step 1 - import dataset and check the gathers

import toolbox
import numpy as np
import pylab

if __name__ == "__main__":
        #import dataset
        print "initialising dataset"
        workspace, params = toolbox.initialise('al_dynamite.su')
        
        #set gather order to shot gather
        params['primary'] = 'sx'
        params['secondary'] = 'gx'
        
        #display
        toolbox.display(workspace, None, **params)
        pylab.show()