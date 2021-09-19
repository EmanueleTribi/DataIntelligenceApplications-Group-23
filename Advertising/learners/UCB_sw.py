import numpy as np
import math
from Advertising.learners.UCB_Learner import *

class UCB_sw(UCB_Learner):
    def __init__(self, arms, hyperpar, window_size):
        super().__init__(arms, hyperpar)
        self.window_size = window_size
        self.rewards_per_arm = [[] for _ in range(self.n_arms)]
        self.pulled_arms = np.array([]) # stores the indexes of the pulled arms
    
    def pull_arm(self):
        not_pulled = [i for i in range(self.n_arms) if i not in self.pulled_arms[-self.window_size:] ]
        # not_pulled = np.where(self.pulled_arms[-self.window_size:] == 0)[0]

        if len(not_pulled) != 0:

            self.pulled_arms=np.append(self.pulled_arms, not_pulled[0])
            return not_pulled[0]
        
        arm_idx = np.argmax(np.add(self.bounds,self.exp_values))
        self.pulled_arms=np.append(self.pulled_arms, arm_idx)

        return arm_idx
    
    def update(self, pulled_arm_idx, reward):
        self.t += 1

        self.rewards_per_arm[pulled_arm_idx].append(reward)
        self.collected_rewards.append(reward)
        num_pulled_arm_window=len(np.where(self.pulled_arms[-self.window_size:] == pulled_arm_idx)[0])
        self.exp_values[pulled_arm_idx] = np.mean(self.rewards_per_arm[pulled_arm_idx][-num_pulled_arm_window:])

        for arm in range(self.n_arms):
            num_pulled_arm_window=len(np.where(self.pulled_arms[-self.window_size:] == arm)[0])

            if num_pulled_arm_window == 0:
                self.bounds[arm] = 0
            else:
                self.bounds[arm] = self.hyperpar*math.sqrt(np.log(min(self.t, self.window_size))/num_pulled_arm_window)
        
    
    

