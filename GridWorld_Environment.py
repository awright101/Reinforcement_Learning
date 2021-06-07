import numpy as np
class AstroidGrid():
    
    def __init__(self,length,width,ndeposits,nsinkholes,rand_locs,fuel):
        self.randomseed1 = np.random.randint(1000)
        self.randomseed2 = np.random.randint(1000)
        #Setting up instance variables
        self.length    = int(length)
        self.width     = int(width)
        self.ndeposits = int(ndeposits)
        self.nsinkholes= int(nsinkholes)
        self.rand_locs = rand_locs
        
        
        #Position Vectors for exit and agent 
         
        
        self.exit_pos    = np.array([length-2,width-2])
        
        self.init_fuel   = fuel
        #Inital Fuel
        self.fuel_left   = fuel
        #Cumulative Reward
        self.reward_cum  = int(0)
        
        #Initalizing Environment 
        self.environment = None
        self.samar_pos  = None
        self.next_pos   = None
        
        self.done = False
        
        self.action_list = ['up','down','left','right','retrive']
        
        
    def reset_env(self):
        
        #Initalizing Grid Array
        
        environment = np.zeros([self.length,self.width])
        
        #Setting Boundary Conditions
        
        environment[:,-1] = -1
        environment[:,0]  = -1
        environment[0,:]  = -1 
        environment[-1,:] = -1
        
        #Setting Exit Position
        
        
        
   
        
        
        if self.rand_locs == False: 
            np.random.seed(self.randomseed1)
            
        for _ in range(self.ndeposits):
            deposit_y,deposit_x = np.random.randint(1,self.length-1),np.random.randint(1,self.width-1)
            environment[deposit_y,deposit_x] = 2
        np.random.seed(seed=None)
        
        
        
        if self.rand_locs == False: 
            np.random.seed(self.randomseed2)
            
        for _ in range(self.nsinkholes):
            sinkhole_y,sinkhole_x = np.random.randint(1,self.length-1),np.random.randint(1,self.width-1)
            environment[sinkhole_y,sinkhole_x] = 3
        np.random.seed(seed=None)
                

            
            
        self.samar_pos = np.array([1,1])
        environment[self.samar_pos[0],self.samar_pos[1]]=0
        environment[self.exit_pos[0],self.exit_pos[1]]  = 5
        self.next_pos  = self.samar_pos
        self.environment =environment
        self.done = False
        self.reward_cum  = int(0)
        self.fuel_left   = self.init_fuel
       
    
    def take_action(self,action):
        
        if action in ['up','down','left','right']:
            
            random_action = np.random.choice([0,1],p = [0.9,0.1])
            
            if random_action:
                
                action = np.random.choice(['up','down','left','right'])
            
      
        if action == 'left':
            self.next_pos = np.array([self.samar_pos[0],self.samar_pos[1] -1])
        if action == 'right':
            self.next_pos = np.array([self.samar_pos[0],self.samar_pos[1]  +1])
        if action == 'down':
            self.next_pos = np.array([self.samar_pos[0] +1,self.samar_pos[1]])
        if action == 'up':  
            self.next_pos = np.array([self.samar_pos[0] -1,self.samar_pos[1]])
        if action == 'retrive':
            self.next_pos = self.samar_pos
            
                                                            
        #Reward responses for position resulting from  action
            
            #Next pos is a boundary
        if self.environment[self.next_pos[0],self.next_pos[1]] == -1: 
            self.samar_pos = self.samar_pos #position doesnt changed as agent is at boundary
            reward = -2
            self.fuel_left += -1
                
            #Next pos is a free space    
        if self.environment[self.next_pos[0],self.next_pos[1]] == 0: 
            self.samar_pos = self.next_pos
            reward = -1
            self.fuel_left += -1
                
            #Next pos is a PMD
        if self.environment[self.next_pos[0],self.next_pos[1]] == 2:
            self.samar_pos = self.next_pos
            reward = 20
            self.fuel_left += -1
            
            #Curr pos is a metal deposit 
        if self.environment[self.samar_pos[0],self.samar_pos[1]] == 2 and action=='retrive':
            reward = 100
            self.fuel_left += -1
                
                #Setting current location back to 0 as deposit has been collect
            self.environment[self.samar_pos[0],self.samar_pos[1]] = 0
            
                  
        if self.environment[self.samar_pos[0],self.samar_pos[1]] != 2 and action=='retrive':
            reward = -10
            self.fuel_left += -1
                
                
        if self.environment[self.next_pos[0],self.next_pos[1]] == 3:
            self.samar_pos = self.next_pos
            reward = -1*np.random.randint(1,100)
            self.fuel_left += -1
                
                
            
        if self.environment[self.next_pos[0],self.next_pos[1]] == 5:
            reward = 20
            self.done = True #Termination condition reached 
            #print('Extraction Point Reached')
        if self.fuel_left <1:
            self.done = True
            reward = -10
            #print('Ran out of fuel')
            
        self.reward_cum += reward 
            
        return reward,self.reward_cum,self.samar_pos,self.fuel_left,self.done
            
        
        
    def calc_obs(self):
        
        obs = self.environment[self.samar_pos[0]-1:self.samar_pos[0]+2,self.samar_pos[1]-1:self.samar_pos[1]+2]
        
        return obs
        
