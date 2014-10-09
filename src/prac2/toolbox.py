import numpy as np
import matplotlib.pyplot as pylab
from matplotlib.widgets import Slider
from scipy.signal import fftconvolve



#==================================================
#                                 decorators
#==================================================


def io(func):
	'''
	an io decorator that allows
	input/output to be either a filename 
	(i.e. a string) or an array
	'''
	def wrapped(*args, **kwargs) :
		if type(args[0]) == type(''):
			workspace = read(args[0])
		else:
			workspace = args[0]
		result = func(workspace, **kwargs)
		if type(result) != type(None):
			if type(args[1]) == type(''):
				return write(result, args[1])
			else:
				return result
	return wrapped

#==================================================
#                                 display tools
#==================================================

@io	
def display(workspace, **params):
	
	#~ agc = params['agc']
	
	def update(val):
		vmax = smax.val
		vmin = smin.val
		im.set_clim(vmax=vmax, vmin=vmin)
		fig.canvas.draw_idle()
	
	fig = pylab.figure()
	'''displays a gather using imshow'''

	vmax = np.amax(workspace['trace'])
	vmin = np.amin(workspace['trace'])
	#~ if agc:
		#~ workspace = toolbox.agc(workspace)
	im = pylab.imshow(workspace['trace'].T, aspect='auto', cmap='Greys', vmax =vmax, vmin=vmin)
	pylab.colorbar()
	axcolor = 'lightgoldenrodyellow'
	axmax = pylab.axes([0.08, 0.06, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
	smax = Slider(axmax, 'vmax', vmin, vmax, valinit=vmax)
	smax.on_changed(update)
	axmin = pylab.axes([0.08, 0.03, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
	smin = Slider(axmin, 'vmin', vmin, vmax, valinit=vmin)
	smin.on_changed(update)	
	smin.on_changed(update)
	
	pylab.draw()
	
def scan_headers(input):
	dataset = toolbox.read(input)
	print dataset.shape
	for key, t in toolbox.su_header_dtype.descr:
		print key, np.amin(dataset[key]), np.amax(dataset[key])
		
	
class build_model(dict):
	def __init__(self,*arg,**kw):
		super(build_model, self).__init__(*arg, **kw)
		self['nlayers'] = 5
		self['nx'] = 500
		fault_throw = 20
		
		self['dz'] = np.array([40, 80, 40, 200, 400, ])
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
			self['model'][model][250:500,120:160] = self[model][1]
			self['model'][model][250:500,120+fault_throw:160+fault_throw] = self[model][2]
		
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
			pylab.imshow(self['model'][m].T)
			pylab.colorbar()
			pylab.xlabel('m')
			pylab.ylabel('m')
			pylab.title(m)
		pylab.show()
		
def find_points(x0, z0, x1, z1, nump, model):
	'''
	nearest neighbour search
	'''
	
	x = np.linspace(x0, x1, nump, endpoint=False)
	z = np.linspace(z0, z1, nump, endpoint=False) #generate rays
	xint = np.ceil(x) #round em down
	zint = np.ceil(z) #round em down
	return model[xint.astype(np.int), zint.astype(np.int)] 
	
def roll(input, shift):
	input = np.pad(input, shift, mode='reflect') #pad to get rid of edge effect
	output = np.roll(input, shift=shift) #shift the values by 1
	return output[shift:-1*shift]
	
@io
def cp(workspace, **params):
	return workspace

@io
def agc(workspace, window=100, **params):
	'''
	automatic gain control
	inputs:
	window
	'''
	vec = np.ones(window, 'f')
	func = np.apply_along_axis(lambda m: np.convolve(np.abs(m), vec, mode='same'), axis=-1, arr=workspace['trace'])
	workspace['trace'] /= func
	workspace['trace'][~np.isfinite(workspace['trace'])] = 0
	workspace['trace'] /= np.amax(np.abs(workspace['trace']))
	return workspace
	
def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, length/dt)
    y = (1.0 - 2.0*(np.pi**2)*(f**2)*(t**2)) * np.exp(-(np.pi**2)*(f**2)*(t**2))
    return y
 
 
def conv(workspace, wavelet):
	workspace['trace'] = np.apply_along_axis(lambda m: fftconvolve(m, wavelet, mode='same'), axis=-1, arr=workspace['trace'])
	return workspace
	
import numpy as np
su_header_dtype = np.dtype([
('tracl', np.int32),
('tracr', np.int32),
('fldr', np.int32),
('tracf', np.int32),
('ep', np.int32),
('cdp', np.int32),
('cdpt', np.int32),
('trid', np.int16),
('nvs', np.int16),
('nhs', np.int16),
('duse', np.int16),
('offset', np.int32),
('gelev', np.int32),
('selev', np.int32),
('sdepth', np.int32),
('gdel', np.int32),
('sdel', np.int32),
('swdep', np.int32),
('gwdep', np.int32),
('scalel', np.int16),
('scalco', np.int16),
('sx', np.int32),
('sy', np.int32),
('gx', np.int32),
('gy', np.int32),
('counit', np.int16),
('wevel', np.int16),
('swevel', np.int16),
('sut', np.int16),
('gut', np.int16),
('sstat', np.int16),
('gstat', np.int16),
('tstat', np.int16),
('laga', np.int16),
('lagb', np.int16),
('delrt', np.int16),
('muts', np.int16),
('mute', np.int16),
('ns', np.uint16),
('dt', np.uint16),
('gain', np.int16),
('igc', np.int16),
('igi', np.int16),
('corr', np.int16),
('sfs', np.int16),
('sfe', np.int16),
('slen', np.int16),
('styp', np.int16),
('stas', np.int16),
('stae', np.int16),
('tatyp', np.int16),
('afilf', np.int16),
('afils', np.int16),
('nofilf', np.int16),
('nofils', np.int16),
('lcf', np.int16),
('hcf', np.int16),
('lcs', np.int16),
('hcs', np.int16),
('year', np.int16),
('day', np.int16),
('hour', np.int16),
('minute', np.int16),
('sec', np.int16),
('timebas', np.int16),
('trwf', np.int16),
('grnors', np.int16),
('grnofr', np.int16),
('grnlof', np.int16),
('gaps', np.int16),
('otrav', np.int16), #179,180
('d1', np.float32), #181,184
('f1', np.float32), #185,188
('d2', np.float32), #189,192
('f2', np.float32), #193, 196
('ShotPoint', np.int32), #197,200
('unscale', np.int16), #201, 204
('TraceValueMeasurementUnit', np.int16),
('TransductionConstantMantissa', np.int32),
('TransductionConstantPower', np.int16),
('TransductionUnit', np.int16),
('TraceIdentifier', np.int16),
('ScalarTraceHeader', np.int16),
('SourceType', np.int16),
('SourceEnergyDirectionMantissa', np.int32),
('SourceEnergyDirectionExponent', np.int16),
('SourceMeasurementMantissa', np.int32),
('SourceMeasurementExponent', np.int16),
('SourceMeasurementUnit', np.int16),
('UnassignedInt1', np.int32),
('ns1', np.int32),
])


def typeSU(ns):
	return np.dtype(su_header_dtype.descr + [('trace', ('<f4',ns))])
	
		
def readSUheader(filename):
	raw = open(filename, 'rb').read()
	return np.fromstring(raw, dtype=su_header_dtype, count=1)

def read(filename=None):
	if filename == None:
		raw= sys.stdin.read()
	else:
		raw = open(filename, 'rb').read()
	return readData(raw)
	
def readData(raw):
	su_header = np.fromstring(raw, dtype=su_header_dtype, count=1)
	ns = su_header['ns'][0]
	file_dtype = typeSU(ns)
	data = np.fromstring(raw, dtype=file_dtype)
	return data	
	
def write(data, filename=None):
	if filename == None:
		data.tofile(sys.stdout)
	else:
		data.tofile(filename)
		





