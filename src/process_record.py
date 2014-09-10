import toolbox
import numpy as np
import su
import pylab
import sys

def nmo(tx, vels, offset):
	t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
	return t0
	
def agc(output): #with headers
	func = toolbox.agc_func(output['trace'], 100)
	output['trace'] /= func
	return output
		

data = su.readSU('record.su')

cdps = np.unique(data['cdp'])

for cdpn in cdps[30:31]:
	cdp = data[data['cdp'] == cdpn]
	sorted_cdp = np.sort(cdp, order=['cdp', 'offset'])
	
	#~ pylab.imshow(agc(sorted_cdp)['trace'].T, aspect='auto', cmap='hsv')
	
	output = np.zeros_like(sorted_cdp)
	
	velrange = range(500, 4500, 100)
	semb = np.zeros((len(velrange), 1000), 'f')
	
	for index2, vel in enumerate(velrange):
	

		for index, trace in enumerate(sorted_cdp):
			if trace['offset'] != 0:
				tx = np.linspace(0.001,1.0, 1000, endpoint=True)
				vels = np.ones_like(tx)*vel
				offset = np.abs(trace['offset'])
				t0 = nmo(tx, vels, offset)
				stretch = np.hstack([np.diff(t0)/0.001, 1.0])
				limits = np.isfinite(t0) & (stretch < 1.5)
				t0 = t0[limits]
				values = trace['trace'][limits]
				vals =  np.interp(tx, t0, values)
				print np.amin(t0), offset
				vals[tx < np.amin(t0)] = 0
				output['trace'][index,:] = vals
		stack = np.sum(output['trace'], axis=0)
		semb[index2,:] = stack
		
	
	#~ pylab.figure()
	pylab.imshow(semb[:200,:].T, aspect='auto', cmap='hsv', extent=(500,4500, 0.2, 0))
	pylab.show()
	
	