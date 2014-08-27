import numpy as np
import matplotlib.pyplot as pylab

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
	
class build_model(dict):
	def __init__(self,*arg,**kw):
		super(build_model, self).__init__(*arg, **kw)
		self['nlayers'] = 5
		self['nx'] = 500
		fault_throw = 10
		
		self['dz'] = np.array([20, 40, 20, 100, 200, ])
		self['vp'] = np.array([800., 2200., 1800., 2400., 4500., ])
		self['vs'] = self['vp']/2.
		self['rho'] = np.array([1500., 2500., 1400., 2700., 4500., ])
		self['depths'] = np.cumsum(self['dz'])
		
		self['model'] = {}
		for model in ['vp', 'vs', 'rho']:
			layer_list = []
			for index in range(self['nlayers']):
				layer = np.ones((self['nx'], self['dz'][index]), 'f')
				layer *= self[model][index]
				layer_list.append(layer)
			self['model'][model] = np.hstack(layer_list)
			self['model'][model][250:500,60:80] = self[model][1]
			self['model'][model][250:500,60+fault_throw:80+fault_throw] = self[model][2]
		
		self['model']['z'] = self['model']['vp'] * self['model']['rho']
		self['model']['R'] = (np.roll(self['model']['z'], shift=-1) - self['model']['z'])/(np.roll(self['model']['z'], shift=-1) + self['model']['z'])
		self['model']['R'][:,0] *= 0
		self['model']['R'][:,-1:] *= 0
		self['model']['R'][:,:self['dz'][0]+2] = 0
		
		
	#def __repr__(self):
		#return repr(self['model'])
			
	def display(self):
		for m in self['model'].keys():
			pylab.figure()
			pylab.imshow(a['model'][m].T)
			pylab.colorbar()
			pylab.xlabel('m')
			pylab.ylabel('m')
			pylab.title(m)
		pylab.show()
		
def agc_func(data, window):
    vec = np.ones(window)/(window/2.)
    func = np.apply_along_axis(lambda m: np.convolve(np.abs(m), vec, mode='same'), axis=0, arr=data)
    return func
    
def find_points(x0, z0, x1, z1, nump, model):
	'''
	nearest neighbour search
	'''
	
	x = np.linspace(x0, x1, nump, endpoint=False)
	z = np.linspace(z0, z1, nump, endpoint=False) #generate rays
	xint = np.floor(x) #round em down
	zint = np.floor(z) #round em down
	return model[xint.astype(np.int), zint.astype(np.int)] 

def traveltime(x0, z0, x1, z1, model, nump, ds):
	x = np.linspace(x0, x1, nump, endpoint=False)
	z = np.linspace(z0, z1, nump, endpoint=False) #generate rays
	xint = np.floor(x) #round em down
	zint = np.floor(z) #round em down
	vel_points = model[xint.astype(np.int), zint.astype(np.int)] 
	return np.sum(ds/vel_points)
	