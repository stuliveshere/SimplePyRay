# in prac 1 we will build a synthetic shot record. 
# it will compose of 3 separate components
#	direct wave
#	refracted wave
#	reflected wave
# based up on a predefined model.

from toolbox import io
import toolbox
import numpy as np
import matplotlib.pyplot as pylab
from exersize1 import initialise
from exersize2 import diverge


#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

def reflection_coefficient(z0, z1):
    z = ((z1 - z0))/(z1+z0)
    return z

def transmission_coefficient(z0, z1):
    r = (2.0*z0)/((z1+z0))
    return r

#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

@io
def build_reflector(dataset, **kwargs):
        '''
        builds reflector
        '''
        
        #some shortcuts
        vp = kwargs['model']['vp']
        rho = kwargs['model']['rho']
        R = kwargs['model']['R']
        sz = kwargs['sz']
        gz = kwargs['gz']
        sx = kwargs['sx']
        gx = kwargs['gx']
        
        numpoints = 100 #used for interpolating through the model
        for x in  gx:
                cmpx = np.floor((gx + sx)/2.).astype(np.int) # nearest midpoint
                h = cmpx - sx #half offset
                #the next line extracts the non-zero reflection points at this midpoint
                rp = np.nonzero(R[cmpx,:])[1][:40]
                print rp
                #and iterates over them
                             
                #~ for cmpz in ():
                        #~ ds = np.sqrt(cmpz**2 + (h)**2)/float(numpoints) # line step distance
                        #~ #predefine outputs
                        #~ amp = 1.0
                        #~ time = 0.0

                        #~ #traveltime from source to cdp
                        #~ vp_down = toolbox.find_points(sx, sz, cmpx, cmpz, numpoints, vp)
                        #~ time += np.sum(ds/vp_down)

                        #~ #traveltime from cdp to geophone
                        #~ vp_up = toolbox.find_points(cmpx, cmpz, gx-1, gz, numpoints, vp)
                        #~ time += np.sum(ds/vp_up)

                        #~ #loss due to spherical divergence
                        #~ amp *= diverge(ds*numpoints, 3)#two way

                        #transmission losses from source to cdp
                        #~ rho_down = toolbox.find_points(sx, sz, cmpx, cmpz, numpoints, rho)
                        #~ z0s = rho_down * vp_down
                        #~ z1s = toolbox.roll(z0s, 1)
                        #~ correction = np.cumprod(transmission_coefficient(z0s, z1s) )[-1] 
                        #~ amp *= correction

                        #~ #amplitude loss at reflection point
                        #~ correction = R[cmpx,cmpz]
                        #~ amp *= correction
                        #~ #transmission loss from cdp to source
                        #~ rho_up = toolbox.find_points(cmpx, cmpz, gx-1, gz, numpoints, rho)
                        #~ z0s = rho_up * vp_up
                        #~ z1s = toolbox.roll(z0s, 1)
                        #~ correction = np.cumprod(transmission_coefficient(z0s, z1s))[-1]
                        #~ amp *= correction

                        #~ x = np.floor(gx).astype(np.int) -1
                        #~ t = np.floor(time*1000).astype(np.int)

                        #~ dataset['trace'][x, t] += amp
        #~ return dataset


        
if __name__ == '__main__':
        workspace, params = initialise()
        
        build_reflector(workspace, 'reflector.su', **params)
        #~ tmp = toolbox.agc('reflector.su', None, **param)
        #~ toolbox.display(tmp, None, **param)

                

                
                
        
        
        

        
        
        