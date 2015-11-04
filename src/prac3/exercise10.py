#spectral enhancement


import toolbox
import numpy as np
import pylab

#--------------------------------------------------
#       useful functions
#-------------------------------------------------

None

if __name__ == "__main__":
        #initialise dataset
        print "initialising dataset"
        workspace, params = toolbox.initialise('stack100.su')
        params['primary'] = None
        params['lowcut'] = 30
        params['highcut'] = 100
        toolbox.bandpass(workspace, None, **params)
        
        toolbox.display(workspace, None, **params)
        
        data = np.fft.rfft(workspace['trace'], axis=-1)
        sign = np.sign(data.real)
        amps = np.abs(data)
        factor = np.sqrt(amps)
        data.real = factor
        workspace['trace'] = np.fft.irfft(data*sign, axis=-1)
        
        toolbox.display(workspace, None, **params)
        pylab.show()
