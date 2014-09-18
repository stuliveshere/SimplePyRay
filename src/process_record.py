import toolbox
import numpy as np
import su
import pylab
import sys



def nmo_calc(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
def nmo(trace, vels, mute):
	''' moves out a single trace (with headers) using
	a single vel vector'''
	dt = trace['dt']*1e-6
	ns = trace['ns']
	offset = np.abs(trace['offset'])
	tx = np.linspace(dt,dt*ns, ns, endpoint=True)
	t0 = nmo_calc(tx, vels, offset)
	stretch = np.hstack([np.diff(t0)/0.001, 1.0])
	limits = np.isfinite(t0) & (stretch < 1.5)
	t0 = t0[limits]
	values = trace['trace'][limits]
	vals =  np.interp(tx, t0, values)
	vals[tx < np.amin(t0)] = 0
	return vals
		
	
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
	result = np.zeros((len(velrange), 1000), 'f')
	for index, veln in enumerate(vels):
		nt = gather.size
		for i in range(nt):
			v = np.ones_like(gather[i]['trace']) * veln
			gather[i] = nmo(gather[i], v, 1.0)
			#~ print gather[i]['trace']
			pylab.plot(gather[i]['trace'])
		#~ pylab.imshow(gather['trace'].T, aspect='auto', cmap='hsv')
			pylab.show()
		sys.exit()
		
		
	
		

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
	
	#~ output = np.zeros_like(holder)
	
	
	#~ 
	
	#~ 
	
		#~ for index, trace in enumerate(holder):
			#~ if trace['offset'] != 0:

		#~ stack = np.sum(output['trace'], axis=0)
		#~ semb[index2,:] = stack
		
	#~ pylab.imshow(semb.T, aspect='auto', cmap='hsv')
	#~ pylab.show()

	
	