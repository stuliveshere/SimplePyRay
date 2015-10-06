from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
import matplotlib.animation as animation
from exersize1 import initialise

@io       
def run_model(dataset, **kwargs):
        #calculate courant's number, do stability check, adjust dt if neccessary
        kwargs['dt'], kwargs['C'] = toolbox.stability_check(kwargs['model']['vp'], kwargs['dt'], min(kwargs['dx'], kwargs['dz']))
        #calculate source wavelet
        kwargs['source'] = toolbox.ricker_roll(200, params['nsteps']*kwargs['dt'], kwargs['dt'] )  
        
        #plotting stuff
        fig, ax = pylab.subplots(1,1,figsize=(8,8))
        frames = []
        #holding arrays
        p=np.zeros([kwargs['nx'],kwargs['nz'],3], dtype=np.float64)  
        shot = np.zeros((kwargs['nx'], kwargs['nsteps']), dtype=np.float32)
        
        #inject first source point
        p[kwargs['sx'], kwargs['sz'],1] += kwargs['source'][1]
        for t in range(2, kwargs['nsteps']-1):
                print t
                #do the thing
                panel = toolbox.evolve1(p, kwargs['C'], kwargs['source'][t], kwargs['sx'], kwargs['sz'])
                #manually roll the array forward
                p[:,:,:-1] = p[:,:,1:] 
                p[:,:,2] = panel
                
                #plotting stuff
                shot[:,t] = p[:,0,1]        
                if t %5 == 0:
                        localmax = np.amax(np.abs(panel))

                        ax.imshow(kwargs['model']['vp'].T, aspect=1, cmap='binary')
                        ax.set_title("%d" %t)
                        frame = ax.imshow(panel.T, aspect=1, vmin=-1*localmax, vmax=localmax, alpha=0.8, cmap='RdBu')
                        frames.append([frame])
                
        ani = animation.ArtistAnimation(fig,frames,interval=10, blit=True,repeat_delay=1000)
        pylab.show()
        return shot


if __name__ == "__main__":
        workspace, params = initialise(filename="model2.png")
        params['sz'] = 100
        #setup some modelling parameters
        params['dt'] = 1e-4
        params['nsteps'] = 1000
        params['dx'] = 1
        params['dz'] = 1
        
  
        panel = run_model(workspace, None, **params)
        #~ panel = toolbox.agc(panel, None, **params)
        pylab.imshow(panel.T)
        pylab.show()