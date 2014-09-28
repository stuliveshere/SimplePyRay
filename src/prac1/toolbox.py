import su
import numpy as np
import matplotlib.pyplot as pylab


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
			kwargs['dataset'] = su.read(args[0])
		else:
			kwargs['dataset'] = args[0]
		result = func(**kwargs)
		if type(result) != type(None):
			if type(args[1]) == type(''):
				return su.write(result, args[1])
			else:
				return result
	return wrapped
	
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