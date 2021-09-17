import numpy as np
import math
import time

class UCB_Learner:
    def __init__(self, arms, hyperpar):
        self.t = 0
        self.hyperpar=hyperpar
        self.arms = arms
        self.bounds = np.zeros(len(arms))
        self.n_pulls = np.ones(len(arms))
        self.n_arms = len(arms)
        self.exp_values = np.zeros(len(arms))
        self.collected_rewards = []
    
    def return_best_arm(self):
        return np.argmax(self.exp_values)

    def return_expected_values(self):
        return self.exp_values
        
    def pull_arm(self):
        if self.t < self.n_arms:
            return self.t
        
        arm_idx = np.argmax(np.add(self.bounds,self.exp_values))
        self.n_pulls[arm_idx] += 1
        return arm_idx

    def update(self, pulled_arm_idx, reward):
        self.t+=1
        pulls = self.n_pulls[pulled_arm_idx]

        for i in range(self.n_arms):
            self.bounds[i] = self.hyperpar*math.sqrt(np.log(self.t)/self.n_pulls[i])
        
        self.exp_values[pulled_arm_idx] = (self.exp_values[pulled_arm_idx] * (pulls-1) + reward)/pulls

        self.collected_rewards.append(reward)
