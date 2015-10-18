import numpy as np
from toolbox import io

def initialise(file):
        #intialise empty parameter dictionary
        #kwargs stands for keyword arguments
        kwargs = {}
        #load file
        dataset = toolbox.read(file)
        
        #allocate stuff
        #~ 
        ns = kwargs['ns'] = dataset['ns'][0]
        dt = kwargs['dt'] = dataset['dt'][0]/1e6
                       
        #also add the time vector - it's useful later
        kwargs['times'] = np.arange(0, dt*ns, dt)
        
        dataset['trace'] /= np.amax(dataset['trace'])
        kwargs['primary'] = 'sx'
        kwargs['secondary'] = 'gx'
        kwargs['step'] = 1
        
        toolbox.scan(dataset)
        return dataset, kwargs
        
@io
def tar(data, **kwargs):
        #pull some values out of the
        #paramter dictionary
        gamma = kwargs['gamma']
        t = kwargs['times']
        
        #calculate the correction coeffieicnt
        r  = np.exp(gamma * t)
        
        #applyt the correction to the data
        data['trace'] *= r
        return data

def interp_vels(vels, **kwargs):
        import scipy.interpolate
        
        def normal_interp(x, y, a, xi, yi):
            rbf = scipy.interpolate.Rbf(x, y, a)
            ai = rbf(xi, yi)
            return ai

        def rescaled_interp(x, y, a, xi, yi):
            a_rescaled = (a - a.min()) / a.ptp()
            ai = normal_interp(x, y, a_rescaled, xi, yi)
            ai = a.ptp() * ai + a.min()
            return ai
        x = np.array([10, 20, 30, 40])
        t = np.array([0.0, .2, .40, .62])
        v = np.array([2000.4, 2300.7, 2400.4, 2900.7])
        xi, yi = np.linspace(0, 50, 500), np.linspace(0, 1, 500)
        xx,yy = np.meshgrid(xi, yi)
        r = rescaled_interp(x,t,v,xx,yy)           
        
def _nmo_calc(tx, vels, offset):
        '''calculates the zero offset time'''
        t0 = np.sqrt(tx*tx - (offset*offset)/(vels*vels))
        return t0
        
@io
def nmo(dataset, **kwargs):
        offsets = np.unique(dataset['offset'])
        if 'smute' not in kwargs.keys(): kwargs['smute'] = 10000.
        ns = kwargs['ns']
        dt = kwargs['dt'] 
        tx = kwargs['times']
        
        for offset in offsets:
                aoffset = np.abs(offset.astype(np.float))
                #calculate time shift for each sample in trac
                t0 = _nmo_calc(tx, kwargs['vels'], aoffset)
                t0 = np.nan_to_num(t0)
                #calculate stretch between each sample
                stretch = 100.0*(np.pad(np.diff(t0),(0,1), 'reflect')-dt)/dt
                filter = [(stretch >0.0) & ( stretch < kwargs['smute'])]
                
                inds = [dataset['offset'] == offset]
                subset = np.apply_along_axis(lambda m: np.interp(tx, t0[filter], m[filter]), axis=-1, arr=dataset['trace'][inds])
                subset[:,tx < np.amin(t0[filter])]  = 0.0
                subset[:,tx > np.amax(t0[filter])] = 0.0
                dataset['trace'][inds] = subset

        return dataset


def _stack_gather(gather):
        '''stacks a single gather into a trace.
        uses header of first trace. normalises
        by the number of traces'''
        gather['trace'][0] = np.mean(gather['trace'], axis=-2)
        return gather[0]

@io	
def stack(dataset, **kwargs):
        cdps = np.unique(dataset['cdp'])
        sutype = np.result_type(dataset)
        result = np.zeros(cdps.size, dtype=sutype)
        for index, cdp in enumerate(cdps):
                gather = dataset[dataset['cdp'] == cdp]
                trace = _stack_gather(gather)
                result[index] = trace
        return result


def semb(workspace,**kwargs):
        vels = kwargs['velocities']
        nvels = vels.size
        ns = kwargs['ns']
        result = np.zeros((nvels,ns),'f')
        for v in range(nvels):
                panel = workspace.copy()
                kwargs['vels'] = np.ones(kwargs['ns'], 'f') * vels[v]
                nmo(panel, None, **kwargs)
                result[v,:] += np.abs(_stack_gather(panel)['trace'])
                
                
        pylab.imshow(result.T, aspect='auto', extent=(min(vels), max(vels),kwargs['ns']*kwargs['dt'],0.), cmap='gist_heat')
        pylab.xlabel('velocity')
        pylab.ylabel('time')
        pylab.colorbar()
        pylab.show()


def _lmo_calc(aoffset, velocity):
        t0 = -1.0*aoffset/velocity
        return t0
        
@io
def lmo(dataset, **kwargs):
        offsets = np.unique(dataset['offset'])
        for offset in offsets:
                aoffset = np.abs(offset)
                shift = _lmo_calc(aoffset, kwargs['lmo'])
                shift  = (shift*1000).astype(np.int)
                inds= [dataset['offset'] == offset]
                dataset['trace'][inds] =  np.roll(dataset['trace'][inds], shift, axis=-1) #results[inds]
        return dataset


@io
def trace_mix(dataset, **kwargs):
        ns = kwargs['ns']
        window = np.ones(kwargs['mix'], 'f')/kwargs['mix']
        for i in range(ns):
                dataset['trace'][:,i] = np.convolve(dataset['trace'][:,i], window, mode='same')
        return dataset


def bandpass(dataset, **kwsargs):
        from scipy.signal import butter, lfilter

        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a

        def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
            b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            y = lfilter(b, a, data)
            return y


        # Sample rate and desired cutoff frequencies (in Hz).
        fs = 5000.0
        lowcut = 500.0
        highcut = 1250.0
            
        y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
        plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)