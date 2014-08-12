import numpy as np
import matplotlib.pyplot as pylab

##################################
#          model definition stuff
##################################

#model uses a 1m per sample grid for simplicity

class seismic_model(dict):
	def __init__(self,*arg,**kw):
		super(seismic_model, self).__init__(*arg, **kw)
		self['nlayers'] = 5
		self['nx'] = 500
		
		self['dz'] = np.array([10, 20, 10, 50, 100, ])
		self['vp'] = np.array([800., 3200., 1800., 3600., 4500., ])
		self['vs'] = self['vp']/2.
		self['rho'] = np.array([1500., 3000., 1800., 3500., 4500., ])
		self['depths'] = np.cumsum(self['dz'])
		
		self['model'] = {}
		for model in ['vp', 'vs', 'rho']:
			layer_list = []
			for index in range(self['nlayers']):
				layer = np.ones((self['nx'], self['dz'][index]), 'f')
				layer *= self[model][index]
				layer_list.append(layer)
			self['model'][model] = np.hstack(layer_list)
				
if __name__ == "__main__":
	a = seismic_model()
	for m in ['vp', 'vs', 'rho']:
		pylab.figure()
		pylab.imshow(a['model'][m].T)
		pylab.colorbar()
		pylab.xlabel('m')
		pylab.ylabel('m')
		pylab.title(m)
	pylab.show()

