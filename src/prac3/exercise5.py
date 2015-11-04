#pick around 10 cdp locations and do a velocity analysis

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
        workspace, params = toolbox.initialise('al_dynamite.su')
        
        #lets see how many cdps there are
        #~ print  np.unique(workspace['cdp'])[25::45].tolist()
        
        #store the cdps for reference
        cdps =[225, 270, 315, 360, 405, 450, 495, 540, 585]   
        
        #define velocities
        params['velocities'] = np.arange(1000,6000,50)
        params['smoother'] = 5
        
        #iterate over list of cdps
        #~ for cdp in cdps:
                #~ params['smute'] = 30
                #~ inds = (workspace['cdp'] > cdp -2) * (workspace['cdp'] < cdp +2)
                #~ gather = workspace[inds]
                #~ toolbox.agc(gather, None, **params)
                #~ params['highcut'] = 120
                #~ params['lowcut'] = 30
                #~ toolbox.bandpass(gather, None, **params)
                #~ toolbox.semb(gather, **params)
                
        #set up vel dictionary for storing values
        vels = {}
        vels[225] =  (0.06, 1537.38) , (0.28, 2876.21) , (0.87, 4608.10)
        vels[270] =  (0.05, 1525.09) , (0.18, 2483.16) , (0.36, 3171.00) , (0.66, 4079.93) , (0.98, 4816.90)
        vels[315] =  (0.04, 1365.42) , (0.14, 2728.82) , (0.22, 3134.15) , (0.57, 4116.78) , (0.74, 4571.25) , (0.97, 5013.43)
        vels[360] =  (0.04, 1697.05) , (0.10, 2520.01) , (0.21, 2937.62) , (0.43, 3244.70) , (0.64, 3981.67) , (0.98, 4239.61)
        vels[405] =  (0.06, 1439.11) , (0.27, 2753.38) , (0.49, 3957.10) , (0.97, 5381.92)
        vels[450] =  (0.06, 1340.85) , (0.41, 2741.10) , (0.52, 3625.47) , (0.02, 1144.32) , (0.29, 3060.45) , (0.54, 3711.45) , (0.97, 4313.31)
        vels[495] =  (0.04, 1611.07) , (0.11, 3072.74) , (0.23, 3318.39) , (0.35, 3772.86) , (0.48, 3981.67) , (0.94, 5099.41)
        vels[539] =  (0.04, 2028.69) , (0.11, 3072.74) , (0.32, 3883.41) , (0.51, 4485.27) , (0.96, 5222.24)
        vels[584] =  (0.06, 1623.36) , (0.20, 2495.44) , (0.32, 3121.87) , (0.95, 4411.57)
        
        #build vels
        vels = toolbox.build_vels(vels, **params)
        
        #display vels
        pylab.imshow(vels.T, aspect='auto')
        pylab.colorbar()
        pylab.show()


