#create final stack
#test stretch mute
#test trace mix
#email final stack to mail@stuliveshere.com

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
        params['primary'] = None
        
        #apply tar
        params['gamma'] = 5
        toolbox.tar(workspace, None, **params)

      
        #copy vels from previous exercise
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
        
        #
        params['vels'] = vels
        params['smute'] = 30
        
        #normal moveout      
                
        v100 = toolbox.co_nmo(workspace, None, **params)
        
        #agc
        toolbox.agc(v100, None, **params)
        
        #trace mix
        params['mix'] = 5
        toolbox.trace_mix(workspace, None, **params)
        
        #stack
        section100 = toolbox.stack(v100, None, **params)
        
        #bandpass filter
        params['lowcut'] = 30
        params['highcut'] = 100
        toolbox.bandpass(section100, None, **params)
        toolbox.cp(section100, 'final_stack.su', **params)
        #display
        toolbox.display(section100, None, **params)
        
        pylab.show()
        