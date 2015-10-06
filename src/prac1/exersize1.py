from toolbox import io
import toolbox
import numpy as np

#-----------------------------------------------------------------------
#              useful functions
#-----------------------------------------------------------------------

@io
def spike(dataset, **kwargs):
        '''add spike to dataset'''
        dataset[:,500] = 1


#-----------------------------------------------------------------------
#              main functions
#-----------------------------------------------------------------------

def initialise(filename='model.png'):
        #initialise parameter dictionary
        parameters = {}
        #build our model, which is pre-defined in the toolbox
        parameters['model'] = toolbox.build_model(filename=filename)

        #add some useful stuff
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
        parameters['offset'] = parameters['gx'] - parameters['sx']
        parameters['aoffsets'] = np.abs(parameters['offset'])
        
        #return workspace and parameters
        return workspace, parameters
        
if __name__ == '__main__':
        #initialise
        workspace, params = initialise()
        #check dictionary contents
        print params['model'].keys()
        #have a look at it - it has a build in display routine
        params['model'].display()
        #add spikes
        spike(workspace, None, **params)
        #display
        toolbox.display(workspace, None, **params)


                


                
                
        
        
        

        
        
        