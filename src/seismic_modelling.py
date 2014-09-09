import toolbox
import numpy as np
import su
import pylab
import sys

#spherical divergence
def diverge(distance):
    r = np.abs(1.0/(distance*distance))
    try:
        infinites = np.isinf(r)
        r[infinites] = np.amax(r[~infinites])
    except IndexError:
        pass
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
sutype = su.typeSU(1000)
holder = np.zeros(0, dtype=sutype)

#build wavelet
low = 2. #hz
high = 60. #hz
wavelet = toolbox.build_wavelet(low, high)[75:125]
wavelet = np.convolve(np.ones(3)/3.,wavelet , mode='same')

#make some useful shortcuts
z0 = model['dz'][0]
v0 = model['vp'][0]
v1 = model['vp'][1]

vp = model['model']['vp']
rho = model['model']['rho']
R = model['model']['R']

#define survey geometry, ie shot and reciever points
sx_coords = np.arange(500.0)[::2] + 0.5
rx_coords = np.arange(500.0)
sz = 0
gz = 0

for sx in sx_coords:
    #calculate some commonly used values
    offsets = rx_coords - sx #vector distance from shot
    aoffsets = np.abs(offsets) #absolute value

    #define an output array
    nx = 500 #number of samples in x direction (assume 1m cells)
    ns = 1000 #number of samples in z direction (assume 1ms cells)

    output = np.zeros((nx, ns), 'f') #holds the output

    #---------------------------------------------------------------------------------------
    #calculate direct wave.  direct. assume speed of sound (330m/s)
    #---------------------------------------------------------------------------------------
    velocity = 330.0 #m/s
    direct_times = aoffsets/velocity #seconds

    #now we need to calculate amplitudes. First, lets set all the amplitudes
    # to 0.05 (picked by testing)
    direct_amps = np.ones_like(rx_coords) * 0.05
    #calculate the spherical divergence correction
    direct_correction = diverge(aoffsets)
    #apply correction
    direct_amps *= direct_correction

    #we are not interested in anything after 1 second
    limits = [direct_times < 1]

    x = rx_coords[limits]
    t = direct_times[limits]
    direct_amps = direct_amps[limits]

    #convert to coordinates
    t *= 1000 # milliseconds
    x = np.floor(x).astype(np.int)
    t = np.floor(t).astype(np.int)

    #write to output array
    output[x, t] += direct_amps

    #check plot
    #~ pylab.plot(x, t, '.')

    #------------------------------------------------------------------------------------
    # calculate refraction
    #------------------------------------------------------------------------------------

    #calculate refraction times based upon function written earlier
    refraction_times = refract(aoffsets, v0, v1, z0)

    #create amplitude array
    refract_amps = np.ones_like(rx_coords) * 0.1
    #calculate the spherical divergence correction
    direct_correction = diverge(aoffsets)
    #apply correction
    refract_amps *= direct_correction



    #it probably wont exceed 1s, but to make it look right we 
    #need to limit it so that it doesnt cross over the direct
    limits = [refraction_times < direct_times]
    x = rx_coords[limits]
    t = refraction_times[limits]
    refract_amps = refract_amps[limits]

    #convert coordinates to integers
    x = np.floor(x).astype(np.int)
    t *= 1000 # milliseconds
    t = np.floor(t).astype(np.int)

    #write to output array
    output[x, t] += refract_amps

    #check plot
    #~ pylab.plot(x, t, '.')


    #~ pylab.ylim([1000,0])



    #-----------------------------------------------------------------------------------------------
    # calculate reflection times and amplitudes
    #-----------------------------------------------------------------------------------------------

    numpoints = 100 #used for interpolating through the model
    for gx in rx_coords:
        cmpx = np.floor((gx + sx)/2.).astype(np.int) # nearest midpoint
        h = cmpx - sx #half offset
        #the next line extracts the non-zero reflection points at this midpoint
        #and iterates over them
        for cmpz in (np.nonzero(R[cmpx,:])[0]):
            ds = np.sqrt(cmpz**2 + (h)**2)/float(numpoints) # line step distance
            #predefine outputs
            amp = 1.0
            time = 0.0

            #traveltime from source to cdp
            vp_down = toolbox.find_points(sx, sz, cmpx, cmpz, numpoints, vp)
            time += np.sum(ds/vp_down)

            #traveltime from cdp to geophone
            vp_up = toolbox.find_points(cmpx, cmpz, gx, gz, numpoints, vp)
            time += np.sum(ds/vp_up)

            #loss due to spherical divergence
            amp *= diverge(ds*numpoints*2)#two way
            
            #~ #transmission losses from source to cdp
            rho_down = toolbox.find_points(sx, sz, cmpx, cmpz, numpoints, rho)
            z0s = rho_down * vp_down
            z1s = toolbox.roll(z0s, 1)
            correction = np.cumprod(transmission_coefficient(z0s, z1s))[-1] 
            amp *= correction

            #amplitude loss at reflection point
            correction = R[cmpx,cmpz]
            amp *= correction

            #transmission loss from cdp to source
            rho_up = toolbox.find_points(cmpx, cmpz, gx, gz, numpoints, rho)
            z0s = rho_up * vp_up
            z1s = toolbox.roll(z0s, 1)
            correction = np.cumprod(transmission_coefficient(z0s, z1s))[-1]
            amp *= correction
            
            x = np.floor(gx).astype(np.int) 
            t = np.floor(time*1000).astype(np.int)
            output[x, t] += amp
            #~ pylab.plot(x, t, '.')


    noise = np.random.normal(0.0, 1e-7, size=(output.shape))
    output += noise

    record = toolbox.conv(output, wavelet)

    data = np.zeros(500, dtype=sutype)
    data['gx'] = rx_coords
    data['tracl'] = range(1,501)
    data['sx'] = sx
    data['offset'] = offsets
    data['cdp'] = (data['sx']+data['gx'])/2
    data['trace'] = record.astype('f4')
    data['ns'] = 1000
    data['dt'] = 1000
    data = data[::2]

    holder = np.hstack([holder, data])
    print holder.shape
    
    
su.writeSU(holder, "record.su")

#~ agc = 0
#~ if agc:
    #~ func = toolbox.agc_func(record, 100)
    #~ record /= func

#~ pylab.figure()
#~ pylab.imshow(record.T, aspect='auto', cmap='hsv', vmax=np.amax(record), vmin=-1*np.amax(record))
#~ pylab.colorbar()
#~ pylab.show()


