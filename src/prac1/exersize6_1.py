import toolbox
import numpy as np
np.seterr(invalid='raise')
import pylab
import multiprocessing as mp
import time
from exersize1 import initialise



def format_coord(x, y):
    col = int(x+0.5)
    row = int(y+0.5)
    if col>=0 and col<numcols and row>=0 and row<numrows:
        z = upwardNormals.T[row,col]
        return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f'%(x, y)


todo = '''
need to re-do angle calculation so it's always to the normal.

normal is easy if we assume every reflection interface is horizontal.
the angle of incidence will then always be %90. save the 
'''
                

import numpy as np
np.seterr(invalid="raise")

def worker(*args):
        parms = args[0]
        
        vmodel = np.frombuffer(vArray.get_obj(), dtype=np.float32)
        vmodel = vmodel.reshape(parms['nx'], parms['nz'])
        pmodel = np.frombuffer(pArray.get_obj(), dtype=np.float32)
        pmodel = pmodel.reshape(parms['nx'], parms['nz'])

        ups = np.frombuffer(upNormals.get_obj(), dtype=np.float32)
        ups = ups.reshape(parms['nx'], parms['nz'])
        downs = np.frombuffer(downNormals.get_obj(), dtype=np.float32)
        downs = downs.reshape(parms['nx'], parms['nz'])

        cell_list = np.array([0, 45, 90, 135, 180, 225, 270, 360])
        cell_lookup={	0:[0,-1],
                45:[1,-1],
                90:[1,0],
                135:[1,1],
                180:[0,1],
                225:[-1,1],
                270:[-1,0],
                315:[-1,-1],
                360:[0,-1],
                }#angle to array index adjustment
        
        alive=1
        
   
        arr = args[1]
        output = []
        
        '''the actual iterator'''
        remainder = 0
        while alive:
                angle = parms['angle']%360
        
                step = cell_list[np.abs(cell_list-angle).argmin()]
                
                remainder += angle - step
                if remainder > 45:
                        step += 45
                        remainder -= 45
                if remainder < -45:
                        step -= 45
                        remainder += 45

                try:
                        new_cell = cell_lookup[step]
                except KeyError:
                        print 'cell key error!'
                        break
                
                tx, tz = parms['x'],parms['z']
                
                try:
                        p1 = pmodel[parms['x'],parms['z']]
                        v1 = vmodel[parms['x'],parms['z']]
                        
                        parms['x']+=new_cell[0]
                        parms['z']+=new_cell[1]
                        
                        if (parms['x'] < 0) or(parms['z'] < 0): break
                        
                        p2 = pmodel[parms['x'],parms['z']]
                        v2 = vmodel[parms['x'],parms['z']]
                except IndexError:
                        #~ print 'step error!', parms['x'], parms['z']
                        break
                
                
                if ((p1 != p2) or (v1 != v2)):
                        if 90 <= angle < 270:
                                normal = downs[tx, tz]
                                incidence = normal - angle #rotated
                                reflection = normal - 180 + incidence #compass
                                try:
                                        ic = np.degrees(np.arcsin(v1/v2))
                                except FloatingPointError:
                                        ic = 180
                                
                                #transmissions
                                if np.abs(incidence) < ic:	
                                        transmission = np.degrees(np.arcsin(v2*np.sin(np.radians(incidence))/v1))
                                        #~ 
                                        #~ print ''
                                        parms['angle'] =  normal - transmission
                                else:
                                        #~ print angle, normal, incidence, v1, v2, reflection, ic, transmission, tx, tz	
                                        break
                                        
                        else:
                                normal = ups[tx, tz]
                                incidence = normal - angle #rotated
                                reflection = normal - 180 + incidence #compass
                                try:
                                        ic = np.degrees(np.arcsin(v1/v2))
                                except FloatingPointError:
                                        ic = 999
                                
                                #transmissions
                                if np.abs(incidence) < ic:	
                                        transmission = np.degrees(np.arcsin(v2*np.sin(np.radians(incidence))/v1))
                                        #~ 
                                        #~ print ''
                                        parms['angle'] =  normal - transmission
                                else:
                                        #~ print angle, normal, incidence, v1, v2, reflection, ic, transmission, tx, tz	
                                        break
                                
                                #~ print normal, angle
                                #~ break
                                
                        new_kwargs = parms.copy()
                        new_kwargs['angle'] = reflection
                        new_kwargs['z'] -= new_cell[1]
                        new_kwargs['x'] -= new_cell[0]
                        new_kwargs['gen'] += 1
                        if new_kwargs['gen'] < new_kwargs['maxgen']: newworkers.put(new_kwargs)


                output.append([parms['x'],parms['z']])
                alive += 1
                if alive > 4000:break

                        
        arr.append(output)
        return 

if __name__ == "__main__":

        workspace, parameters = initialise(filename='model2.png')
        #holding array
        manager = mp.Manager()
        arr = manager.list()
        

        cross = parameters['model']['vp']

    
        nz = cross.shape[-1]
        nx = cross.shape[-2]
        
        dz = np.zeros_like(cross)
        dx = np.zeros_like(cross)
        
        dz[:,1:] = np.diff(cross, axis=-1)
        dx[1:,:] = np.diff(cross, axis=-2)
        
        im = np.hypot(dx, dz)
        im[im != 0.0] = 1
        

        inds = zip(*np.nonzero(im))
        
        downwardNormals = np.zeros_like(cross)
        upwardNormals = np.zeros_like(cross)
        
        for x, z in inds:
                stamp = im[x-3:x+3,z-3:z+3]
                if stamp.shape == (6,6):
                        locs = np.nonzero(stamp)
                        xi = locs[0]
                        A = np.array([xi, np.ones_like(xi)])
                        # linearly generated sequence
                        yi = locs[1]
                        w = np.linalg.lstsq(A.T,yi)[0][0]
                        #~ if 520 < x < 600 and 1200 < z < 1300: 
                                #~ print x, z, np.degrees(np.arctan2(w, -1) ) %360
                                #~ pylab.pcolor(stamp.T)
                                #~ pylab.show()
                        downwardNormals[x-1:x+1,z-1:z+1] = np.degrees(np.arctan2(w, 1) + np.pi) %360
                        upwardNormals[x-1:x+1,z-1:z+1] =  np.degrees(np.arctan2(w, 1) ) %360


        vArray = mp.Array('f', cross.flatten())
        pArray = mp.Array('f', cross.flatten())
        upNormals = mp.Array('f', upwardNormals.flatten())
        downNormals = mp.Array('f', downwardNormals.flatten())


        workers = mp.Queue()
        newworkers = mp.Queue()
        nprocesses = 4
        jobs = []

        print "gonna spawn some rays!"
        angles = np.arange(135,226,3)
        jobs = []
        tmp = []
        for angle in angles:
                kwargs={'x':int(nx/2.),
                                'z':1,
                                't':0,
                                'angle':angle,
                                'amplitude':1,
                                'nx':nx,
                                'nz':nz,
                                'gen':0,
                                'maxgen':1,
                                }
                workers.put(kwargs)
        print "starting queue built!"
        time.sleep(0.1)
        #~ print workers.qsize()
        

        while True:
                for _ in range(min(nprocesses, workers.qsize())):
                        args = workers.get()
                        p = mp.Process(target=worker, args=(args,arr))
                        jobs.append(p)
                        tmp.append(args)
                        p.start()
                        time.sleep(0.1)

                while newworkers.qsize(): workers.put(newworkers.get())	
                
                for i, j in enumerate(jobs):
                        j.join()
                jobs = []
                tmp = []
                print workers.qsize()
                if workers.qsize() ==0: break

        
        print 'plotting!'
        for item in arr:
                try:
                        x,y = zip(*item)
                        pylab.plot(x, y, 'k')
                        pylab.xlim([0,nx])
                        pylab.ylim([nz,0])	
                except ValueError:
                        pass


        
        
        pylab.imshow(cross.T)
        pylab.plot(parameters['gx'][::40], np.ones_like(parameters['gx'][::40]), 'gD')
        pylab.show()
                


                
                

        