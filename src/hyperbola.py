#this time calculator works by storing the earth model in a 2d array in memory, effectively drawing a line of points 
#between source and reciever, then finding the velocity nearest to each point.  
#currently only valid for laterally homogeneous models, but is easily extended.
#straight ray assumption only - this is not so easily extended.

import numpy as np
import matplotlib.pyplot as pylab
from toolbox import build_wavelet, build_model, agc_func, find_points
import sys


def reflection_coefficient(z0, z1):
	z = ((z1 - z0)**2)/(z1+z0)**2
	if z1 < z0: z*= -1
	return z
	
def transmission_coefficient(z0, z1):
	return (4*z0*z1)/((z1+z0)**2)


	


	
# survey geometry.
sx_coords = [120.5] #np.arange(99)+0.5
rx_coords = np.arange(240)

num=1000 #number of interpolation points


model = build_model()

nt = 1000
dt = 0.001
nx = rx_coords.size
output = np.zeros((nx, nt), 'f')



##################################
#       travel time calculations
##################################

for layer in [1, 2,3]: #not going to bother with base of weathering or bottom of model
	depth = model['depths'][layer]
	for sx in sx_coords:
		for rx in rx_coords:
			offset = rx - sx #calculate shot-reciever offset from coordinates)
			h = offset/2. #half offset
			ds = np.sqrt(depth**2 + (h)**2)/float(num) # line step distance
			amp = 1.0
			#generate ray beginning and end
			velocity_steps_down = find_points(sx, 0, sx+h, depth, num, model['model']['vp'])
			velocity_steps_up = find_points(sx+h, depth, rx, 0, num, model['model']['vp'])
			traveltime = np.sum(ds/velocity_steps_down) +  np.sum(ds/velocity_steps_up)#time = distance/speed
			#amplitude due to spherical divergence
			s = ds*num*2
			amp /= s*s			
			#amplitude due to transmission downwards
			density_steps_down = find_points(sx, 0, sx+h, depth, num, model['model']['rho'])
			z0 = density_steps_down * velocity_steps_down
			z1 = np.roll(z0, shift=1)
			amp *= np.cumprod(transmission_coefficient(z0, z1))[-1] #transmission coefficients on the way down
			#amps due to reflection
			z0 = model['vp'][layer]*model['rho'][layer]
			z1 = model['vp'][layer+1]*model['rho'][layer+1]
			amp *= reflection_coefficient(z0, z1)
			#amps due to transmission upwards
			density_steps_up = find_points(sx+h, depth, rx, 0, num, model['model']['rho'])
			z0 = density_steps_up * velocity_steps_up
			z1 = np.roll(z0, shift=-1)
			amp *= np.cumprod(transmission_coefficient(z0, z1))[-1] #transmission coefficients on the way down	
			output[np.floor(rx), np.floor(traveltime/dt)] += amp


#add noise
noise = np.random.normal(0.0, 0.5e-7, size=(output.shape))
output += noise

#convolve wavelet
wavelet = build_wavelet(6, 140)
for rx in rx_coords:
	output[rx,:] = np.convolve(output[rx,:], wavelet, mode='same')

#agc for viewing
agc =1
amp_func = agc_func(data=output,window=50)
if agc:
	output /= amp_func		
	scale = 5.0
else:
	scale = np.mean(np.abs(output))*5e1
	
#view
pylab.imshow(output[:,:200].T, aspect='auto', vmin=-1*scale, vmax=scale, cmap='RdGy')
pylab.colorbar()
pylab.figure()
pylab.plot(wavelet)
pylab.show()
		