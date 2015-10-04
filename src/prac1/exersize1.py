from toolbox import io
import toolbox
import numpy as np

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def spike(dataset, **kwargs):
        dataset[:,500] = 1


#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

def initialise():
        parameters = {}
        #build our model, which is pre-defined in the toolbox
        parameters['model'] = toolbox.build_model()
       
        nx = parameters['nx'] = parameters['model']['nx']
        nz = parameters['nz'] = parameters['model']['nz']
        
        #initialise data workspace
        workspace = np.zeros((nx, nz), dtype=np.float32)	
        
        #define survey geometry, ie shot and reciever points
        parameters['sx'] = 250
        parameters['gx'] = np.arange(500.0)
        
        #add some more useful stuff
        parameters['dt'] = 1e-3	
        parameters['sz'] = 0
        parameters['gz'] = 0
        return workspace, parameters
        
if __name__ == '__main__':
        workspace, params = initialise()
        #check dictionary contents
        print params['model'].keys()
        #have a look at it - it has a build in display routine
        params['model'].display()
        spike(workspace, None, **params)
        toolbox.display(workspace, None, **params)


                


                
                
        
        
        

        
        
        