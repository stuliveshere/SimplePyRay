#import su files from prac1
#view the gathers to make sure 
#they imported properly

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
        #intialise empty parameter dictionary
        #kwargs stands for keyword arguments
        kwargs = {}
        #load file
        dataset = toolbox.read(file)
        
        #allocate stuff
        dataset['cdp'] = (dataset['gx'] + dataset['sx'])/2.
        kwargs['ns'] = 1000
        kwargs['dt'] = 0.001
        
        #also add the time vector - it's useful later
        kwargs['times'] = np.linspace(0.001, 1.0, 1000)
        return dataset, kwargs
        
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        workspace, params = initialise('survey.su')
        
        #the scan tool scans the file headers for non-zero values
        toolbox.scan(workspace)
        
        #the scroll tool allows you to skip through an entire volume, but
        #you have to define the sort keys, and step size
        params['primary'] = 'sx'
        params['secondary'] = 'gx'
        params['step'] = 20
        
        #the scroll tool is like the display tool, but
        #you can use the left and right arrows to
        #scroll through a volume
        toolbox.scroll(workspace, None, **params)
        
        #the viewing tools have been changed so that 
        #you can view more than one thing at once.
        #but you need to put this at the end.
        pylab.show()
        
        
        
