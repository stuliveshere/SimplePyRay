

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.cm as cm
from matplotlib.mlab import griddata
from numpy.random import uniform, seed
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


r = griddata(x,t,v,xi,yi, interp='linear')

#~ seed(0)
#~ npts = 200
#~ x = uniform(-2, 2, npts)
#~ y = uniform(-2, 2, npts)
#~ z = x*np.exp(-x**2 - y**2)
#~ # define grid.
#~ xi = np.linspace(-2.1, 2.1, 100)
#~ yi = np.linspace(-2.1, 2.1, 200)
#~ # grid the data.
#~ zi = griddata(x, y, z, xi, yi, interp='linear')

r = rescaled_interp(x,t,v,xx,yy)

plt.imshow(r.T)
plt.colorbar()
plt.show()