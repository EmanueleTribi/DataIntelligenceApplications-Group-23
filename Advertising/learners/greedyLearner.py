import numpy as np
 


class greedyLearner:
    def __init__(self, n_bids, bids):
        self.n_bids = n_bids
        self.bids = bids
## funtion that  returns the marginal increment in the bid of the category passed
## va fatto il controllo che non sia maggiore di 4
    def get_new_bids(self, category):
        return self.bids[category]+1
## function that returns the difference beteen the rewards
    def evaluate_marginal(self, previous_reward, actual_reward):
        return actual_reward - previous_reward
    
## function that creates a list of marginal increments and it returns it
    def level_exploration(self, bids):
        marginal_bids= []
        for i in range(0, 4):
            ## check that the value of bids is not over 4
            if self.bids[i]+1 < 5:
                marginal_bids.append(get_new_bids(i))
        return marginal_bids
    
    def update_bids(self, bids):
        self.bids = bids


    

            


