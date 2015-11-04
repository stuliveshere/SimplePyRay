#import su files from prac1
#view the gathers to make sure 
#they imported properly

from toolbox import io
import toolbox
import numpy as np
import os
import matplotlib.pyplot as pylab

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def initialise(file):
        #intialise empty parameter dictionary
        #kwargs stands for keyword arguments
        kwargs = {}
        #load file
        dataset = toolbox.read(file)
        
        #allocate stuff
        ns = kwargs['ns'] = dataset['ns'][0]
        dt = kwargs['dt'] = dataset['dt'][0]/1e6
                       
        #also add the time vector - it's useful later
        kwargs['times'] = np.arange(0, dt*ns, dt)
        
        dataset['trace'] /= np.amax(dataset['trace'])
        kwargs['primary'] = 'sx'
        kwargs['secondary'] = 'gx'
        kwargs['step'] = 1
        
        toolbox.scan(dataset)
        return dataset, kwargs
        
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        workspace, params = initialise('cleaned.su')
        
        #view the dataset
        toolbox.display(workspace, None, **params)
        pylab.show()
        
        
        
