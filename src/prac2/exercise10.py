#we need a velocity filter

from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exercise1 import initialise
from exercise3 import tar
from exercise4 import nmo
from exercise5 import stack
from exercise7 import lmo

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def fk2(dataset, **kwargs):
        shots = np.unique(dataset['sx'])
        for shot in shots:
                inds = [dataset['sx'] == shot]
                slice = dataset[inds]
                slice = np.sort(slice, order=['sx','gx'])
                fft =  np.fft.rfft2(slice['trace'])
                nfft =  fft.shape[0]/2
                #~ fft = np.roll(fft, nfft, axis=-2)
                
                filter = fft.copy()
                filter *= 0
                vmin = 300.0
                vmax = 1000.0
                aoffsets = np.abs(slice['offset'])
                tmax = ((aoffsets/vmin)/kwargs['dt']).astype(np.int)
                tmin =  ((aoffsets/vmax)/kwargs['dt']).astype(np.int)
                
                for index in range(filter.shape[0]):
                        filter[index, tmin[index]:tmax[index]] += 1.0
                smoother = np.sin(np.linspace(0, np.pi, 100))
                fftfilter = np.apply_along_axis(lambda m: np.convolve(m, smoother, mode='same'), axis=-1, arr=filter)
                fftfilter /= np.amax(fftfilter)
                fftfilter = 1 - fftfilter
                fft *= np.abs(fftfilter)
                dataset['trace'][inds] = np.fft.irfft2(fft)
        return dataset
                
                #~ pylab.imshow(np.abs(fftfilter.T), aspect='auto')
                #~ pylab.colorbar()
                #~ pylab.show()

@io
def fk(dataset, **kwargs):
        shots = np.unique(dataset['sx'])
        for shot in shots:
                inds = [dataset['sx'] == shot]
                slice = dataset[inds]
                slice = np.sort(slice, order=['sx','gx'])
                fft =  np.fft.rfft2(slice['trace'])
                ctype = np.dtype([('offset', np.float), ('trace', (np.complex128, fft.shape[1]))])
                workspace = np.zeros(slice.size, dtype=ctype)
                workspace['trace'] = fft
                nfft =  fft.shape[0]/2
                workspace['trace'] = np.roll(workspace['trace'], nfft, axis=-2)
                workspace['offset'] = slice['offset']
                lmo(workspace, None, **kwargs)
                smoother = np.ones(500)/500.
                workspace['trace'][:,-500:]  = np.apply_along_axis(lambda m: np.convolve(m, smoother, mode='same'), axis=-1, arr=workspace['trace'][:,-500:])
                kwargs['lmo'] *= -1
                lmo(workspace, None, **kwargs)
                workspace['trace'] = np.roll(workspace['trace'], nfft, axis=0)
                dataset['trace'][inds] = np.fft.irfft2(workspace['trace'])
        return dataset
        
@io       
def fkdisplay(dataset, **kwargs):
        shots = np.unique(dataset['sx'])
        for shot in shots:
                inds = [dataset['sx'] == shot]
                slice = dataset[inds]
                slice = np.sort(slice, order=['sx','gx'])
                fft =  np.fft.rfft2(slice['trace'])
                ctype = np.dtype([('offset', np.float), ('trace', (np.complex128, fft.shape[1]))])
                workspace = np.zeros(slice.size, dtype=ctype)
                workspace['trace'] = fft
                nfft =  fft.shape[0]/2
                workspace['trace'] = np.roll(workspace['trace'], nfft, axis=-2)
                pylab.imshow(np.abs(workspace['trace'].T), aspect='auto')
                pylab.colorbar()
                pylab.show()              
        
#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

if __name__ == "__main__":
        #intialise workspace and parameter dictionary
        print 'initialising'
        workspace, params = initialise('survey.su')
        workspace = workspace[workspace['sx'] == 500]
        toolbox.display(workspace, None, **params)
        params['lmo'] = 3000.0
        fk = fkdisplay(workspace, None, **params)
        
        
        #~ params['primary'] = None
        #~ toolbox.display(workspace, None, **params)
        #~ pylab.show()
