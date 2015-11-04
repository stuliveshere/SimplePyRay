#last time we did a very simplistic velocity analysis. 
#this time we want to do a few more locations

import toolbox
import numpy as np
import pylab

#--------------------------------------------------
#       useful functions
#-------------------------------------------------

None

if __name__ == "__main__":
        #initialise dataset
        print "initialising dataset"
        workspace, params = toolbox.initialise('foybrook.su')
        
        #apply TAR
        print "applying true amplitude recovery"
        params['gamma'] = 3
        toolbox.tar(workspace, None, **params)
        
        #lets see how many cdps there are
        print  np.unique(workspace['cdp'])[25::45].tolist()
        params['smoother'] = 5
        
        #copy your list of cdps here... it will make it easier later
        cdps = [219, 264, 309, 354, 399, 444, 489, 534, 579]
        
        #~ params['velocities'] = np.arange(2000,6000,50)
        
        #~ for cdp in cdps:
                #~ gather = workspace[workspace['cdp'] == cdp]
                #~ toolbox.agc(gather, None, **params)
                #~ toolbox.semb(gather, **params)
                
        vels = {}
        vels[219] =  (0.03, 2350.40) , (0.13, 2615.04) , (0.46, 3232.54) , (1.13, 4202.88) , (1.54, 4545.94)
        vels[264] =  (0.05, 2840.48) , (0.10, 3203.13) , (0.15, 3918.64) , (0.56, 4398.91) , (1.14, 4888.99)
        vels[309] =  (0.07, 2918.89) , (0.28, 3634.40) , (0.76, 4085.27) , (1.47, 4565.54)
        vels[354] =  (0.09, 2997.30) , (0.54, 3820.63) , (0.65, 3987.25) , (0.88, 4330.30) , (1.32, 4692.96)
        vels[399] =  (0.07, 2938.49) , (0.31, 3516.78) , (0.71, 4389.11) , (1.38, 5055.61) 
        vels[444] =  (0.07, 2869.88) , (0.26, 3242.34) , (0.45, 3712.81) , (0.75, 4006.85) , (1.11, 5222.24) 
        vels[489] =  (0.05, 2781.67) , (0.23, 3585.39) , (0.47, 4379.31) , (0.90, 4938.00) , (1.47, 5437.87) 
        vels[534] =  (0.05, 2673.85) , (0.14, 3212.93) , (0.24, 4193.08) , (0.76, 4741.97) , (1.22, 5134.03)
        vels[579] =  (0.08, 2673.85) , (0.19, 3320.75) , (0.40, 4036.26) , (1.06, 4781.17) 
        
        #build our 2D  velocity map
        print "building velocities"
        params['vels'] = toolbox.build_vels(vels, **params)
        
        #~ #view it
        pylab.imshow(params['vels'].T, aspect='auto')
        pylab.colorbar()
        pylab.show()
        
        #~ #Now we have a better velocity profile, we can use a better nmo to move it out
        #~ print "applying nmo correction"
        #~ workspace = toolbox.co_nmo(workspace, None, **params)
        
        #~ #apply AGC
        #~ print "applying AGC"
        #~ toolbox.agc(workspace, None, **params)
        
        #~ #trace mix
        #~ print "applying trace mix"
        #~ params['mix'] = 5
        #~ toolbox.trace_mix(workspace, None, **params)
        
        #~ #stack
        #~ print "stacking"
        #~ section = toolbox.stack(workspace, None, **params)
        
        #~ #display
        #~ #turn off gather sort
        #~ params['primary'] = None
        #~ print "displaying"
        #~ toolbox.display(section, None, **params)
        #~ toolbox.cp(section, 'stack.su', **params)
        #~ pylab.show()
        
        
        
        














        