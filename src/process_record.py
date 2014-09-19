import toolbox
import numpy as np
import su
import pylab
import sys


def nmo_calc(tx, vels, offset):
	np.seterr(all='ignore')
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
def nmo_trace(trace, vels, mute):
	''' moves out a single trace (with headers) using
	a single vel vector'''
	dt = np.float(trace['dt']*1e-6)
	ns = np.float(trace['ns'])
	offset = np.float(np.abs(trace['offset']))
	mute += 1
	tx = np.linspace(dt,dt*ns, ns, endpoint=True)
	t0 = nmo_calc(tx, vels, offset)
	nmo_limit = np.isfinite(t0)
	
	t0 = t0[nmo_limit]
	stretch = np.hstack([np.diff(t0)/0.001, t0[-1]])
	
	stretch_limit = [stretch < mute]
	
	t0 = t0[stretch_limit]


	values = trace['trace'][nmo_limit][stretch_limit]

	vals =  np.interp(tx, t0, values)
	
	vals[tx < np.amin(t0)] = 0
	trace['trace'] = vals
	return trace
	

	
		
	
def agc(output): #with headers
	func = toolbox.agc_func(output['trace'], 100)
	output['trace'] /= func
	return output
	
def stack(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	header = dataset[0]
	fold = dataset.size
	trace = np.sum(dataset['trace'], axis=-2)/np.float(fold)
	header['trace'] = trace
	return header
	
def supergather(step, width, bins, dataset):
	sutype = np.result_type(dataset)
	cdps = np.unique(dataset['cdp'])
	dataset['offset'] = np.abs(dataset['offset'])
	supergather_centres = range(min(cdps)+width, max(cdps)-width, step)
	supergather_slices = [cdps[a-width:a+width] for a in supergather_centres]
	for index, inds in enumerate(supergather_slices):
		for cdpn, cdp in enumerate(dataset['cdp']):
			if cdp in inds:
				dataset['ns1'][cdpn] = index
				
	dataset = dataset[dataset['ns1'] != 0]
	output = np.empty(0, dtype=sutype)
	for ind in np.unique(dataset['ns1']):
		sg = dataset[dataset['ns1'] == ind]
		hist = np.digitize(sg['offset'], bins)
		sg['ep'] = hist
		vals = np.unique(sg['ep'])
		holder = np.zeros(len(vals), dtype=sutype)
		for v in vals:
			traces = sg[sg['ep'] == v]
			header = traces[0]
			fold = traces.size
			trace = np.sum(traces['trace'], axis=-2)/np.float(fold)
			header['trace'] = trace
			holder[v-1] = header
		output = np.concatenate([output, holder])
		
	return output
			
def semb(gather, vels):
	holder = gather.copy()
	holder['trace'] = 0
	result = np.zeros((len(velrange), 1000), 'f')
	for index, veln in enumerate(vels):
		nt = gather.size
		for i in range(nt):
			trace_in = gather[i]
			v = np.ones_like(gather[i]['trace']) * veln
			#~ nmo(gather[i], v, 1.0)
			trace_out = nmo_trace(trace_in, v, 1.0)
			pylab.plot(trace_in)
			pylab.plot(trace_out)
			
		
	
		

			pylab.show()
		
		result[index] = stack(holder)['trace']
		
	return result	
			
		
		
	
		

data = su.readSU('record.su')
sutype = np.result_type(data)
cdps = np.unique(data['cdp'])
offsets = np.unique(data['offset'])
aoffsets = sorted(np.abs(offsets))


supergathers = supergather(10, 3, aoffsets[::2], data)

inds = supergathers['ns1']
for ind in inds:
	supergather = supergathers[supergathers['ns1'] == ind]
	sorted_supergather = np.sort(supergather, order=['offset'])
	supergather = agc(supergather)

	velrange = range(500, 4500, 100)
	velan = semb(supergather, velrange)
	
	print velan.shape
	#~ break
	
	#~ output = np.zeros_like(holder)
	
	
	#~ 
	
	#~ 
	
		#~ for index, trace in enumerate(holder):
			#~ if trace['offset'] != 0:

		#~ stack = np.sum(output['trace'], axis=0)
		#~ semb[index2,:] = stack
		
	pylab.imshow(velan.T, aspect='auto', cmap='hsv')
	pylab.show()

	
	