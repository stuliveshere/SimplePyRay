# in prac 1 we will build a synthetic shot record. 
# it will compose of 3 separate components
#	direct wave
#	refracted wave
#	reflected wave
# based up on a predefined model.

from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------
def diverge(distance, coefficient=3.0):
        '''spherical divergence correction''' 
        r = np.abs(1.0/(distance**coefficient))
        return r
        
def direct(distance, velocity):
        '''calculates the direct ray travel time'''
        time = distance/velocity
        return time

        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

@io
def build_direct(dataset, **kwargs):
        '''
        calculates direct wave arrival time and 
        imposes it upon an array. assumes 330 m/s
        surface velocity
        '''
        
        #speed of the direct wave
        directv = 330.0 #m/s
        
        #calculate direct travel times
        direct_times = direct(kwargs['aoffsets'], directv)
        
        #set base amplitude (from testing)
        direct_amps = np.ones_like(kwargs['gx']) * 0.005
        #calculate the spherical divergence correction
        direct_correction = diverge(kwargs['aoffsets'], 2.0)
        #apply correction
        direct_amps *= direct_correction
        direct_amps[~np.isfinite(direct_amps)] = 0.01
        
        #we are not interested in anything after 1 second
        limits = [direct_times < 1]
        x = kwargs['gx'][limits]
        t = direct_times[limits]
        direct_amps = direct_amps[limits]
        
        

        #convert to coordinates
        t *= 1000 # milliseconds
        x = np.floor(x).astype(np.int)
        t = np.floor(t).astype(np.int)
        
        dataset[x, t] += direct_amps
        return dataset


        
if __name__ == '__main__':
        #initialise
        workspace, params = initialise()
        
        #lets set up for calculating direct wave
        build_direct(workspace, None, **params)
        
        #and display
        toolbox.agc(workspace, None, **params)
        toolbox.display(workspace, None, **params)

                

                
                
        
        
        

        
        
        