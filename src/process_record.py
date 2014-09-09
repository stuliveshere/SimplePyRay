import toolbox
import numpy as np
import su
import pylab
import sys

data = su.readSU('record.su')

cdps = np.unique(data['cdp'])

for cdpn in cdps[30:31]:
	cdp = data[data['cdp'] == cdpn]
	sorted_cdp = np.sort(cdp, order=['cdp', 'offset'])
	
	raw = sorted_cdp['trace']
	func = toolbox.agc_func(raw, 100)
	print func.shape
	raw /= func

	pylab.imshow(sorted_cdp['trace'].T, aspect='auto', cmap='gray')
	pylab.show()
	
	