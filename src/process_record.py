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
	offset = np.abs(trace['offset']).astype(np.float)
	ns = trace['ns']
	dt = trace['dt'] * 1e-6
	tx = np.linspace(dt, dt*ns, 
	print tx
	sys.exit()
	
	


	return trace
	
	
def stack(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	header = dataset[0]
	fold = dataset.size
	trace = np.sum(dataset['trace'], axis=-2)/np.float(fold)
	header['trace'] = trace
	return header


			
def semb(gather, vels):
	sutype = np.result_type(gather)
	nvels = vels.size
	nt = gather.size
	ns = gather['ns'][0]
	
	result = np.zeros(nvels, dtype=sutype)
	for v in range(nvels):
		for i in range(nt):
			vector = np.ones(ns) * vels[v]
			gather[i] = nmo_trace(gather[i], vector, 1.0)
		result[v] = stack(gather)
		
	#~ return result	
			
		
		
	
if __name__ == '__main__':
	
	data = su.readSU('record.su')
	sutype = np.result_type(data)
	cdps = np.unique(data['cdp'])
	offsets = np.unique(data['offset'])
	aoffsets = sorted(np.abs(offsets))
	
	supergathers = toolbox.build_supergather(10, 3, aoffsets[::2], data)

	inds = supergathers['ns1']
	for ind in inds:
		supergather = supergathers[supergathers['ns1'] == ind]
		sorted_supergather = np.sort(supergather, order=['offset'])

		supergather = toolbox.agc(supergather)

		velrange = np.arange(500, 4500, 100)
		velan = semb(supergather, velrange)

		
	

	
	