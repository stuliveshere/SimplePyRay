import toolbox
import numpy as np
import su
import pylab

#spherical divergence
def diverge(distance):
    r = np.abs(1.0/(distance*distance))
    infinites = np.isinf(r)
    r[infinites] = np.amax(r[~infinites])
    return r
    
def reflection_coefficient(z0, z1):
    z = ((z1 - z0)**2)/(z1+z0)**2
    if z1 < z0: z*= -1
    return z

def transmission_coefficient(z0, z1):
    return (4*z0*z1)/((z1+z0)**2)
    
def refract(x, v0, v1, z0):
    ic = np.arcsin(v0/v1)
    t0 = 2.0*z0*np.cos(ic)/v0
    t = t0 + x/v1
    return t


#build the pre-defined velocity model
model = toolbox.build_model()

z0 = model['dz'][0]
v0 = model['vp'][0]
v1 = model['vp'][1]

#define survey geometry, ie shot and reciever points
sx_coords = [120.0] #np.arange(99)+0.5
rx_coords = np.arange(500.0)
sz = 0
gz = 0

sx = sx_coords[0] #temporary


#calculate some commonly used values
offsets = rx_coords - sx_coords[0] #exact distance from shot
aoffsets = np.abs(offsets) #absolute value

#define an output array
nx = 500 #number of samples in x direction (assume 1m cells)
ns = 1000 #number of samples in z direction (assume 1ms cells)

output = np.zeros((nx, ns), 'f') #holds the output



#direct. assume speed of sound (330m/s)
velocity = 330.0 #m/s
direct_times = aoffsets/velocity #s 
direct_times *= 1000 # milliseconds

#we need to get rid of those values bigger than one second. 
limits = [direct_times < 1000]
direct_times = direct_times[limits]
#we also need to work out which geophones these are
geophones = rx_coords[limits]

#now we need to calculate amplitudes. First, lets set all the amplitudes
# to 0.05 (picked by testing)
direct_amps = np.ones_like(geophones) * 0.05
#calculate the spherical divergence correction
direct_correction = diverge(aoffsets[limits])
#apply correction
direct_amps *= direct_correction

#convert to integers
x = np.floor(geophones).astype(np.int)
t = np.floor(direct_times).astype(np.int)

#write to output array
output[x, t] += direct_amps

#check plot
pylab.imshow(output.T, aspect='auto', cmap='RdGy', vmax=np.amax(output), vmin=-1*np.amax(output))
pylab.colorbar()
pylab.show()


#~ #refraction



#~ x_locs = np.abs(np.arange(500) - sx_coords[0])
#~ tt = np.floor((refract(x_locs, v0, v1, z0)*1000.0)).astype(np.int)
#~ xx = np.arange(500).astype(np.int)
#~ ampr = np.ones_like(xx, 'f')*diverge(x_locs[tt < 1000])
#~ ampr[np.argmax(ampr)] = 0
#~ ampr *= 0.1
#~ output[xx,tt] += ampr
#~ tmin = np.ceil((z0*2.2/v0)*1000).astype(np.int)
#~ output[:,:tmin] = 0

#~ #calculate traveltimes and amplitudes for each reflection point
#~ num = 100
#~ vp = model['model']['vp']
#~ rho = model['model']['rho']
#~ R = model['model']['R']

#~ for gx in gxs:
    #~ cmpx = np.floor((gx + sx)/2.).astype(np.int)
    #~ h = cmpx - sx
    #~ for cmpz in (np.nonzero(R[cmpx,:])[0]):
        #~ ds = np.sqrt(cmpz**2 + (h)**2)/float(num) # line step distance
        #~ #predefine outputs
        #~ amp = 1.0
        #~ time = 0.0

        #~ #traveltime from source to cdp
        #~ vp_down = toolbox.find_points(sx, sz, cmpx, cmpz, num, vp)
        #~ time += np.sum(ds/vp_down)

        #~ #traveltime from cdp to geophone
        #~ vp_up = toolbox.find_points(cmpx, cmpz, gx, gz, num, vp)
        #~ time += np.sum(ds/vp_up)

        #~ #loss due to spherical divergence
        #~ amp *= diverge(ds*num*2)


        #~ #transmission losses from source to cdp
        #~ rho_down = toolbox.find_points(sx, sz, cmpx, cmpz, num, rho)
        #~ z0 = rho_down * vp_down
        #~ z1 = np.roll(z0, shift=1)
        #~ z1[0] = z0[0]
        #~ z1[-1] = z0[-1]
        #~ correction = np.cumprod(transmission_coefficient(z0, z1))[-1]
        #~ amp *= correction

        #~ #amplitude loss at reflection point
        #~ correction = R[cmpx,cmpz]
        #~ amp *= correction

        #~ #transmission loss from cdp to source
        #~ rho_up = toolbox.find_points(cmpx, cmpz, gx, gz, num, rho)
        #~ z0 = rho_up * vp_up
        #~ z1 = np.roll(z0, shift=-1)
        #~ z1[0] = z0[0]
        #~ z1[-1] = z0[-1]
        #~ correction = np.cumprod(transmission_coefficient(z0, z1))[-1]
        #~ amp *= correction

        #~ z = np.floor(time*1000).astype(np.int)
        #~ x = np.floor(gx).astype(np.int)    
        #~ output[x, z] += amp

#~ noise = np.random.normal(0.0, 1e-9, size=(output.shape))
#~ output += noise
#~ output /= np.amax(output)

#~ #build wavelet
#~ low = 2. #hz
#~ high = 60. #hz
#~ wavelet = toolbox.build_wavelet(low, high)[75:125]
#~ wavelet = np.convolve(np.ones(3)/3.,wavelet , mode='same')

#~ record = np.apply_along_axis(lambda m: np.convolve(m, wavelet, mode='same'), axis=1, arr=output)