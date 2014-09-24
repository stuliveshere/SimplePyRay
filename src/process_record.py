import toolbox
import numpy as np
import su
import pylab
import sys

def stack(dataset):
	'''stacks a single gather into a trace.
	uses header of first trace. normalises
	by the number of traces'''
	holder = dataset[0].copy()
	holder['trace'].fill(0.0)
	fold = dataset.size
	holder['trace'] += np.sum(dataset['trace'], axis=-2) /np.float(fold)
	return holder

def nmo_calc(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
def nmo_trace(trace, vels, mute):
	''' moves out a single trace (with headers) using
	a vector of velocities'''
	output = trace.copy()
	output['trace'].fill(0.0)
	offset = np.abs(trace['offset']).astype(np.float)
	ns = trace['ns']
	dt = trace['dt'] * 1e-6
	tx = np.linspace(dt, dt*ns, ns)
	t0 = nmo_calc(tx, vels, offset)
	stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
	filter = [(stretch >0.0) & ( stretch < mute)]
	vals = np.interp(tx, t0[filter], trace['trace'][filter])
	vals[tx < np.amin(t0[filter])] = 0.0
	vals[tx > np.amax(t0[filter])] = 0.0
	output['trace'] += vals
	return output
	
def nmo_gather(gather, vector, smute):
	output = gather.copy()
	output['trace'].fill(0.0)
	nt = gather.size
	for i in range(nt):
		output[i]['trace'] += nmo_trace(gather[i], vector, smute)['trace']
	return output

			
def semb(sgather, vels):
	nvels = vels.size
	sutype = np.result_type(sgather)
	ns = sgather['ns'][0]
	result = np.zeros((nvels,ns),'f')
	print sgather['offset']
	

	for v in range(nvels):
		nmo = nmo_gather(sgather, vels[v], 100.0)
		nmo['trace'][:80] *= 0
		result[v,:] += np.abs(stack(nmo)['trace'])
		
		
	pylab.imshow(result.T, aspect='auto', extent=(800.,4400.,1.,0.), cmap='spectral') #, vmin=0, vmax=1)
	pylab.colorbar()
	pylab.show()
				
		
		
	
if __name__ == '__main__':
	
	data = su.readSU('record.su')
	
	cdp_gathers = np.sort(data, order=['cdp', 'offset'])
	cdp300 = cdp_gathers[cdp_gathers['cdp'] == 300]
	#~ toolbox.display(cdp300)
	su.writeSU(cdp_gathers, 'cdps.su')

	
	velrange = np.arange(800.0, 4500.0, 100.0)
	result = semb(toolbox.agc(cdp300), velrange)
	
	
	#~ offsets = np.unique(data['offset'])
	#~ aoffsets = sorted(np.abs(offsets))
	#~ print aoffsets
	#~ supergathers = toolbox.build_supergather(10, 3, aoffsets[::2], data)

	#~ inds = supergathers['ns1']
	
	#~ print inds
	
	#~ for ind in inds[20:]:
		#~ sg = supergathers[supergathers['ns1'] == ind]
		
		#~ ssg = np.sort(sg, order=['offset'])

		#~ toolbox.display(toolbox.agc(ssg))

		#~ semb(toolbox.agc(ssg), velrange)

		
	

	
	