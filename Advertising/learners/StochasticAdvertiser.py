import numpy as np
import random
class StochasticLearner:
    def __init__(self, param_bid):
        self.param_bid = param_bid
        self.t = 0
    ## rewards shouldn't affect a stochstic learner, for which the only updated parameter should be the round number 
    ##    self.reward_per_arm = x = [[] for i in range(n_arms)]
    ##    self.collected_rewards = np.array([])

    ## funtion that updates the round
    def update(self):
        self.t += 1

    ## function that pull the arm, in this case it simply returns a random number 
    ## that is the random bid that the advertiser will make, it depends on a parameter that can be defined 
    ## once initialized the stochastic learner and on the time variable self.t
    def stoch_bid(self):
        num = random.random()
        if num > 0.5:
            bid_value = self.param_bid + self.t%3
        else:
            bid_value = self.param_bid - self.t%3
        return bid_value
    ## function random bid maybe considering a max bid
