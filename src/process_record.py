import toolbox
import numpy as np
import su
import pylab
import sys


def nmo_calc(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
def nmo_trace(trace, vels, mute):
	''' moves out a single trace (with headers) using
	a vector of velocities'''
	holder = np.zeros_like(trace)
	offset = np.abs(trace['offset']).astype(np.float)
	ns = trace['ns']
	dt = trace['dt'] * 1e-6
	tx = np.linspace(dt, dt*ns, ns)
	t0 = nmo_calc(tx, vels, offset)
	stretch = 100.*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt

	filter = [(stretch >0) & ( stretch < mute)]
	vals = np.interp(tx, t0[filter], trace['trace'][filter])
	vals[tx < np.amin(t0[filter])] = 0.0
	holder['trace'] = vals
	return holder
	
	
def stack(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	fold = dataset.size
	holder = np.sum(dataset['trace'], axis=-2)/np.float(fold)
	return holder


			
def semb(gather, vels):
	holder = np.zeros_like(gather)
	sutype = np.result_type(gather)
	nvels = vels.size
	nt = gather.size
	ns = gather['ns'][0]
	
	result = np.zeros(nvels, dtype=sutype)
	for v in range(nvels):
		vector = np.ones(ns) * vels[v]
		for i in range(nt):
			#~ pylab.plot(gather[i]['trace'])
			holder[i] = nmo_trace(gather[i], vector, 100)
			#~ pylab.plot(holder[i]['trace'])
			#~ pylab.show()

		#~ toolbox.display(holder)
		result[v] = stack(holder)
		
	return result	
			
		
		
	
if __name__ == '__main__':
	
	data = su.readSU('record.su')
	sutype = np.result_type(data)
	cdps = np.unique(data['cdp'])
	offsets = np.unique(data['offset'])
	aoffsets = sorted(np.abs(offsets))
	
	supergathers = toolbox.build_supergather(10, 3, aoffsets[::2], data)

	inds = supergathers['ns1']
	for ind in inds[50:]:
		supergather = supergathers[supergathers['ns1'] == ind]
		sorted_supergather = np.sort(supergather, order=['offset'])

		supergather = toolbox.agc(supergather)

		velrange = np.arange(800.0, 4500.0, 100.0)
		velan = semb(supergather, velrange)
		toolbox.display(velan)

		
	

	
	