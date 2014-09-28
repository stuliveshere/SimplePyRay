# all processes read from and write to hdd.
# this allows "checkpointing",
# i.e. you dont have to rerun everything just to plot the answer.

import toolbox
import numpy as np
import pylab
from matplotlib.widgets import Slider


#==================================================
#                                 decorators
#==================================================


def io(func):


	def wrapped(*args, **kwargs) :
		
		if type(args[0]) == type(''):
			kwargs['dataset'] = toolbox.read(args[0])
		else:
			kwargs['dataset'] = args[0]
		
		result = func(**kwargs)
			
		if type(args[1]) == type(''):
			
			return toolbox.write(result, args[1])
		else:
			return result
		
	return wrapped


    
def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper

#==================================================
#                                  misc functions
#==================================================

def build_vel_trace(times, velocities, ns=1000, dt=0.001):
	tx = np.linspace(dt, dt*ns, ns)
	vels = np.interp(tx, times, velocities)
	vels = np.pad(vels, (100,100), 'reflect')
	vels = np.convolve(np.ones(100.0)/100.0, vels, mode='same')
	vels = vels[100:-100]
	#~ pylab.plot(vels)
	#~ pylab.show()
	return vels

#==================================================
#                                  method functions
#==================================================

def _stack_gather(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	holder = dataset[0].copy()
	holder['trace'].fill(0.0)
	fold = dataset.size
	holder['trace'] += np.sum(dataset['trace'], axis=-2) /np.float(fold)
	return holder

def _nmo_calc(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0

def _nmo_trace(trace, vels, mute):
	output = trace.copy()
	output['trace'].fill(0.0)
	offset = np.abs(trace['offset']).astype(np.float)
	ns = trace['ns']
	dt = trace['dt'] * 1e-6
	tx = np.linspace(dt, dt*ns, ns)
	t0 = _nmo_calc(tx, vels, offset)
	stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
	filter = [(stretch >0.0) & ( stretch < mute)]
	vals = np.interp(tx, t0[filter], trace['trace'][filter])
	vals[tx < np.amin(t0[filter])] = 0.0
	vals[tx > np.amax(t0[filter])] = 04.0
	output['trace'] += vals
	return output
	
#==================================================
#                                  display functions
#==================================================
	

def display(input, agc=1):
	
	def update(val):
		vmax = smax.val
		vmin = smin.val
		im.set_clim(vmax=vmax, vmin=vmin)
		fig.canvas.draw_idle()
	
	fig = pylab.figure()
	'''displays a gather using imshow'''
	dataset = toolbox.read(input)
	vmax = np.amax(dataset['trace'])
	vmin = np.amin(dataset['trace'])
	if agc:
		dataset = toolbox.agc(dataset)
	im = pylab.imshow(dataset['trace'].T, aspect='auto', cmap='spectral', vmax =vmax, vmin=vmin)
	pylab.colorbar()
	axcolor = 'lightgoldenrodyellow'
	axmax = pylab.axes([0.08, 0.06, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
	smax = Slider(axmax, 'vmax', vmin, vmax, valinit=vmax)
	smax.on_changed(update)
	axmin = pylab.axes([0.08, 0.03, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
	smin = Slider(axmin, 'vmin', vmin, vmax, valinit=vmin)
	smin.on_changed(update)	
	smin.on_changed(update)
	
	pylab.show()
	
def scan_headers(input):
	dataset = toolbox.read(input)
	print dataset.shape
	for key, t in toolbox.su_header_dtype.descr:
		print key, np.amin(dataset[key]), np.amax(dataset[key])
		
def semb(input, vels):
	dataset = toolbox.read(input)
	nvels = vels.size
	ns = dataset['ns'][0]
	result = np.zeros((nvels,ns),'f')
	for v in range(nvels):
		gather = nmo(input, None, [vels[v]], [0],  20)
		gather = toolbox.agc(gather)
		result[v,:] += np.abs(_stack_gather(gather)['trace'])
		
		
	pylab.imshow(result.T, aspect='auto', extent=(800.,4400.,1.,0.), cmap='spectral', vmin=0, vmax=0.6)
	pylab.colorbar()
	pylab.show()
		
#==================================================
#                                  processing functions
#==================================================

@benchmark
@io	
def sort(**param):
	return np.sort(param['dataset'], order=param['order'])
	
def slice(input, output, key, values):
	dataset = toolbox.read(input)
	filter = ~np.isfinite(dataset['tracl'])
	for value in values:
		bool = dataset[key] == value
		filter = (bool) | (filter)
	toolbox.write(dataset[filter], output)
	
def nmo(input, output, vels, times, smute):
	dataset = toolbox.read(input)
	nt = dataset.size
	holder = dataset.copy()
	holder['trace'].fill(0)
	
	vector = build_vel_trace(times, vels)

	for i in range(nt):
		holder[i]['trace'] += _nmo_trace(dataset[i], vector, smute)['trace']
	if output:
		toolbox.write(holder, output)
	else:
		return holder

	
def agc(input, output, window=100):
	dataset = toolbox.read(input)
	dataset = toolbox.agc(dataset, window=window)
	toolbox.write(dataset, output)
	
	
def stack(input, output):
	dataset = toolbox.read(input)
	cdps = np.unique(dataset['cdp'])
	sutype = np.result_type(dataset)
	holder = np.zeros(cdps.size, dtype=sutype)
	for index, cdp in enumerate(cdps):
		gather = dataset[dataset['cdp'] == cdp]
		trace = _stack_gather(gather)
		holder[index] = trace
	toolbox.write(holder, output)
	
if __name__ == '__main__':
	sort('record.su', 'cdp-gathers.su', order=['cdp', 'offset'])
	#~ slice('cdp-gathers.su', 'cdp300.su', key='cdp', values=range(300,310))
	#~ display('cdp300.su')
	#~ nmo('cdp300.su', 'nmo300.su', vels, times, 30)
	#~ display('nmo300.su')
	#~ semb('cdp300.su', np.arange(800.0, 4500.0, 100.0))	
	
	#~ vels = [1425,1550, 1829]
	#~ times = [0.19,0.23,0.38]
	#~ nmo('cdp-gathers.su', 'nmo-gathers.su', vels, times, 30)
	#~ agc('nmo-gathers.su', 'agc-nmo-gathers.su')
	#~ mix('agc-nmo-gathers.su', 'mixed-gathers.su')
	#~ stack('mixed-gathers.su', 'mixed-agc-stack.su')
	#~ display('mixed-agc-stack.su')

	
	
	
	
	

