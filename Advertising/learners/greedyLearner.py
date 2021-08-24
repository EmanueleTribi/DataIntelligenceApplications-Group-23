import numpy as np
from random import randint

class greedyLearner:
    def __init__(self, n_bids=5, bids=np.zeros(5)):
        self.n_bids = n_bids
        self.bids = bids
## funtion that  returns the marginal increment in the bid of the category passed
## va fatto il controllo che non sia maggiore di 4
    #def get_new_bids(self, category):
       # return self.bids[category]+1
## function that returns the difference beteen the rewards
    def evaluate_marginal(self, previous_reward, actual_reward):
        return actual_reward - previous_reward
    
## function that creates a list of marginal increments and it returns it
    def level_exploration(self):
        for i in range(0, 5):
            print(str(i) + ": this is the value of i")
            print(str(self.bids[i]) + ": this is the value of the bid at the position i")
            ## check that the value of bids is not over 4
            if self.bids[i]+1 < 5:
                marginal_bids.append(self.bids[i]+1)
        return marginal_bids
    
    def update_bids(self, bids):
        self.bids = bids

    def keep_going_on(self, marginal_gain): 
        for i in marginal_gain: 
            if i >= 0: 
                return True 
        return False


    #function that iterates over the possible bid 
    #example: [0 0 0 0 0] -> [1 0 0 0 0], [0 1 0 0 0], [0 0 1 0 0], [0 0 0 1 0], [0 0 0 0 1]
    #         [1 0 0 0 0] -> [2 0 0 0 0], [1 1 0 0 0], [1 0 1 0 0], [1 0 0 1 0], [1 0 0 0 1]
    #todo: function to evaluate the marginal gain as it should be (for now it is just a random integer)
    def evaluate(self):
        marginal_gain = np.zeros(self.n_bids)
        bids = self.bids
        while self.keep_going_on(marginal_gain):
            new_bid = bids
            marginal_gain = np.zeros(self.n_bids)
            for i in range(0, self.n_bids):
                if new_bid[i] != 4:
                    new_bid[i] += 1
                    #marginal = evaluate_marginal(new_bid)
                    marginal = randint(-75, 50)
                    if marginal < 0:
                        marginal = -1
                    marginal_gain[i] = marginal
                    new_bid[i] -= 1
                else: 
                    marginal = -2
                    marginal_gain[i] = marginal

            max_gain = np.argmax(a = marginal_gain)
            if marginal_gain[max_gain] >= 0:
                bids[max_gain] += 1

        return bids

    



    

            


