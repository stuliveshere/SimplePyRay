import numpy as np
import matplotlib.pyplot as pylab
from matplotlib.widgets import Slider
from scipy.signal import fftconvolve
import matplotlib.image as image



#==================================================
#                                 decorators
#==================================================


def io(func):
        '''
        an io decorator that allows
        input/output to be either a filename 
        (i.e. a string) or an array
        args[0] = input filename
        args[1] = output filename
        '''
        def wrapped(*args, **kwargs) :
                nx = kwargs['nx']
                nz = kwargs['nz']
                if type(args[0]) == type(''):
                        workspace = np.fromfile(args[0], dtype= np.float32).reshape(nx, nz)
                else:
                        workspace = args[0]
                result = func(workspace, **kwargs)
                if type(result) != type(None):
                        if type(args[1]) == type(''):
                                result.astype(np.float32).tofile(args[1])
                        else:
                                return result
        return wrapped

#==================================================
#                                 display tools
#==================================================

@io	
def display(workspace, **params):
        
        def update(val):
                vmax = smax.val
                vmin = smin.val
                im.set_clim(vmax=vmax, vmin=vmin)
                fig.canvas.draw_idle()
        
        fig = pylab.figure()
        '''displays a gather using imshow'''

        vmax = np.amax(workspace)
        vmin = np.amin(workspace)

        im = pylab.imshow(workspace.T, aspect='auto', cmap='Greys', vmax =vmax, vmin=vmin)
        pylab.colorbar()
        axcolor = 'lightgoldenrodyellow'
        axmax = pylab.axes([0.08, 0.06, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
        smax = Slider(axmax, 'vmax', vmin, vmax, valinit=vmax)
        smax.on_changed(update)
        axmin = pylab.axes([0.08, 0.03, 0.65, 0.01], axisbg=axcolor) #rect = [left, bottom, width, height] in normalized (0, 1) units
        smin = Slider(axmin, 'vmin', vmin, vmax, valinit=vmin)
        smin.on_changed(update)	
        smin.on_changed(update)
        
        pylab.show()
        
def scan_headers(input):
        dataset = toolbox.read(input)
        print dataset.shape
        for key, t in toolbox.su_header_dtype.descr:
                print key, np.amin(dataset[key]), np.amax(dataset[key])
                
        
class build_model(dict):
        '''
        create an RGB image called model.png
        red = vp
        green = vs
        blue = rho
        divide true value by 100
        i.e. vp = 1000m/s becomes r=10        
        '''
        def __init__(self,*arg,**kw):
                super(build_model, self).__init__(*arg, **kw)

                #import model and rescale values
                im = np.floor(image.imread("model.png")*25500).T
                
                #build model dictionary
                self['vp'] = im[0,:,:]
                self['vs'] = im[1,:,:]
                self['rho'] = im[2,:,:]
                
                #create accoustic impedance lookup
                z = self['z'] =  self['vp'] * self['rho']
                self['nx'], self['nz'] = z.shape
                
                #calculte local refleciton coefficients
                z1 =  np.roll(z, shift=1)
                z2 =  z.copy()              
                self['R'] = (z2 - z1)/(z2 + z1)
                self['R'][:,-1] *= 0
                self['R'][:,0] *= 0
                
                
        def display(self):
                for m in ['vp', 'vs', 'rho', 'R']:
                        pylab.figure()
                        pylab.imshow(self[m].T)
                        pylab.colorbar()
                        pylab.xlabel('m')
                        pylab.ylabel('m')
                        pylab.title(m)
                pylab.show()
                
def find_points(x0, z0, x1, z1, nump, model):
        '''
        nearest neighbour search
        '''
        
        x = np.linspace(x0, x1, nump, endpoint=False)
        z = np.linspace(z0, z1, nump, endpoint=False) #generate rays
        xint = np.ceil(x) #round em up
        zint = np.ceil(z) #round em up
        return model[xint.astype(np.int), zint.astype(np.int)] 
        
def roll(input, shift):
        input = np.pad(input, shift, mode='reflect') #pad to get rid of edge effect
        output = np.roll(input, shift=shift) #shift the values by 1
        return output[shift:-1*shift]
        
@io
def cp(workspace, **params):
        return workspace

@io
def agc(workspace, window=100, **params):
        '''
        automatic gain control
        inputs:
        window
        '''
        vec = np.ones(window, 'f')
        func = np.apply_along_axis(lambda m: np.convolve(np.abs(m), vec, mode='same'), axis=-1, arr=workspace)
        workspace /= func
        workspace[~np.isfinite(workspace)] = 0
        workspace /= np.amax(np.abs(workspace))
        return workspace
        
def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, length/dt)
    y = (1.0 - 2.0*(np.pi**2)*(f**2)*(t**2)) * np.exp(-(np.pi**2)*(f**2)*(t**2))
    return y
 
 
def conv(workspace, wavelet):
        return np.apply_along_axis(lambda m: fftconvolve(m, wavelet, mode='same'), axis=-1, arr=workspace)

#==================================================
#                                finite difference modelling tools
#==================================================

                
def evolve(p, nz, nx, k, t):
    '''brute force iterator'''
    for z in range(1,nz-1):
        for x in range(1,nx-1):
            p[xs,zs,t] = s[t]
            k = kk[x, z]  
            p[x,z,t] = 2*p[x,z,t-1] - p[x,z,t-2] + k*(p[x+1,z,t-1]-4*p[x,z,t-1]+p[x-1,z,t-1]+p[x,z+1,t-1]+p[x,z-1,t-1])
    return p

def evolve1(grid, velocity, s, xs, xz, step=0, buf=20):
    '''pad and slice iterator'''
    assert buf > 1
    padded = np.pad(grid, buf, mode='symmetric')[:,:,buf:-buf]
    padded[0:20,:,:] *= -1
    padded[:,-20:-1,:] *= -1
    a = 2*padded[1:-1,1:-1,-1] - padded[1:-1,1:-1,-2] 
    b = padded[2:,1:-1,-1] -4*padded[1:-1,1:-1,-1]+ padded[:-2,1:-1,-1]+padded[1:-1,2:,-1]+padded[1:-1,:-2,-1]
    buf -= 1
    a = a[buf:-buf, buf:-buf]
    b = b[buf:-buf, buf:-buf]
    c = a + velocity*b
    c[xs, xz] += s
    return c

def evolve2(grid, C, s, xs, xz, step=0):  
    '''pad and roll iterator'''
    c = np.pad(grid, 1, mode='edge')[:,:,1:-1]
    vel = np.pad(C, 1, mode='edge')  
    d= 2.0*c[:,:,-1]  - c[:,:,-2] + vel*(np.roll(c[:,:,-1], 1, axis=1)  + \
                -4*c[:,:,-1]  + np.roll(c[:,:,-1], -1, axis=1) + np.roll(c[:,:,-1],-1, axis=0) + \
                np.roll(c[:,:,-1], 1, axis=0))
    d = d[1:-1,1:-1]
    d[xs, xz] += s
    return d


def ricker_roll(freq, length, dt):
        s = ricker(freq, length, dt)
        while np.abs(s[0]) < 1e-2:
                s = np.roll(s, -1)

        return s
        
        
def stability_check(vp, dt, dx):
        old_dt = dt
        C = (vp*dt/dx)**2 
        #stability check
        low = 1e-6
        high = 1e6
        threshold = 0.5
        while True:
                dt = (low + high)/2.
                C = (vp*dt/dx)**2
                if np.amax(np.abs(C)) <threshold: 
                        low = dt
                else: 
                        high = dt
                if  np.isclose(np.amax(np.abs(C)), threshold):
                        break
        return dt, C

