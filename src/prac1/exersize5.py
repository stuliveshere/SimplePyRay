from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize2 import  build_direct
from exersize3 import build_refractor
from exersize4 import build_reflector

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def build_combined(dataset, **kwargs):
        dataset = build_direct(dataset, None, **kwargs)
        dataset = build_refractor(dataset, None, **kwargs)
        dataset = build_reflector(dataset, None, **kwargs)
        return dataset
        
@io
def add_noise(dataset, **kwargs):
        noise = np.random.normal(0.0, 1e-8, size=(dataset.shape))
        dataset += noise
        return dataset
        
@io
def convolve_wavelet(dataset, **kwargs):
        wavelet = toolbox.ricker(60)	
        dataset =  toolbox.conv(dataset, wavelet)
        return dataset

if __name__ == '__main__':
        #initialise
        workspace, params = initialise()
        
        #build record
        build_combined(workspace, None, **params)
        
        #add wavelet
        workspace = convolve_wavelet(workspace, None, **params)
        
        #add noise
        workspace = add_noise(workspace, None, **params)
        
        #display
        toolbox.agc(workspace, None, **params)
        toolbox.display(workspace, None, **params)
