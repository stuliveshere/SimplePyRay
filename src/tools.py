import numpy as np

def build_wavelet(lowcut, highcut, ns=200, dt = 0.001):
	'''builds a band limited zero
	phase wavelet by filtering in the 
	frequency domain. quick and dirty - 
	i've used a smoother to reduce 
	wavelet ring
	
	use:
	low = 5. #hz
	high = 140. #hz
	wavelet = build_wavelet(low, high)
	'''
	
	signal = np.zeros(ns)
	signal[np.int(ns/2.)] = 1.0
	fft = np.fft.fft(signal)
	n = signal.size
	timestep = dt
	freq = np.fft.fftfreq(n, d=timestep)
	filter = (lowcut < np.abs(freq)) & (np.abs(freq) < highcut)
	filter = np.convolve(filter, np.ones(100, 'f')/100., mode='same')
	fft *= filter
	signal=np.fft.ifft(fft)
	return signal.real