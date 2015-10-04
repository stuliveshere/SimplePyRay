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
from exersize2 import diverge, build_direct


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def refract(x, v0, v1, z0):
        ic = np.arcsin(v0/v1)
        t0 = 2.0*z0*np.cos(ic)/v0
        t = t0 + x/v1
        return t
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

@io
def build_refractor(dataset, **kwargs):
        '''
        builds refractor
        '''
        
        R =  kwargs['model']['R']
        x = np.where(R != 0)[0][::4]
        z0 = np.where(R != 0)[1][::4]
        
        v1 = kwargs['model']['vp'][x, z0]
        v0 = kwargs['model']['vp'][x, z0-1]
        
        refraction_times = refract(kwargs['aoffsets'], v0, v1, z0)

        #create amplitude array
        refract_amps = np.ones_like(kwargs['gx']) * 0.01
        #calculate the spherical divergence correction
        refract_correction = diverge(kwargs['aoffsets'], 2.0)
        #apply correction
        refract_amps *= refract_correction
        refract_amps[~np.isfinite(refract_amps)] = 0.01

        #it probably wont exceed 1s, but to make it look right we 
        #need to limit it so that it doesnt cross over the direct
        directv = 330.0 #m/s
        direct_times = kwargs['aoffsets']/directv
        limits = [refraction_times < direct_times]
        x = kwargs['gx'][limits]
        t = refraction_times[limits]
        refract_amps = refract_amps[limits]

        #convert coordinates to integers
        x = np.floor(x).astype(np.int)
        t *= 1000 # milliseconds
        t = np.floor(t).astype(np.int)

        dataset[x, t] += refract_amps
        return dataset


        
if __name__ == '__main__':
        workspace, params = initialise()
        
        build_direct(workspace, None, **params)
        build_refractor(workspace, None, **params)
        tmp = toolbox.agc(workspace, None, **params)
        toolbox.display(tmp, None, **params)

                

                
                
        
        
        

        
        
        