import scipy.ndimage as sp
from scipy.signal import fftconvolve
import numpy as np
import toolbox
import matplotlib.pyplot as pylab
import cProfile


def numpy_style(wavelet, workspace):
	toolbox.conv(workspace, wavelet)
	return workspace
	
	
def scipy_style(wavelet, workspace):
	workspace['trace'] =  sp.convolve1d(workspace['trace'], wavelet, axis=-1)
	return workspace

def scipy_fft(wavelet, workspace):
	workspace['trace'] = np.apply_along_axis(lambda m: fftconvolve(m, wavelet, mode='same'), axis=-1, arr=workspace['trace'])
	return workspace
	
	

params = {}
wavelet = toolbox.ricker(60)
sutype = toolbox.typeSU(1000)


workspace1 = np.zeros(500, dtype=sutype)
workspace1['trace'][:,500] = 1
cProfile.run('numpy_style(wavelet, workspace1)')



workspace2 = np.zeros(500, dtype=sutype)
workspace2['trace'][:,500] = 1
cProfile.run('scipy_style(wavelet, workspace2)')



workspace3 = np.zeros(500, dtype=sutype)
workspace3['trace'][:,500] = 1
cProfile.run('scipy_fft(wavelet, workspace3)')
toolbox.display(workspace3, None, **params)




