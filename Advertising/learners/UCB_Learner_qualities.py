import numpy as np
import math
from Advertising.learners.UCB_Learner import *
from SocialNetwork.cascade import *

class UCB_Learner_qualities(UCB_Learner):

    def __init__(self, arms, hyperpar, social_network,estimation_rounds = 2000):
        super().__init__(arms, hyperpar)
        self.nodes_estimation = compute_array_estimated_influence(social_network=social_network, rounds=estimation_rounds)
    

    # seeds it's supposed to be an array of indexes denoting the active nodes (the ones who clicked)
    def update(self, pulled_arm_idx, reward, seeds):
        self.t+=1
        pulls = self.n_pulls[pulled_arm_idx]

        for i in range(self.n_arms):
            self.bounds[i] = self.hyperpar*math.sqrt(np.log(self.t)/self.n_pulls[i])
        
        # Here estimating the reward using the pre-computed influences
        reward_influence = 0
        if len(seeds) != 0:
            for i in range(0, len(seeds)):
                reward_influence += self.nodes_estimation[seeds[i]]
            reward_influence = reward_influence/len(seeds)# + reward_influence)/2
            estimated_reward = reward + reward_influence
        else:
            estimated_reward = 0
        
        self.exp_values[pulled_arm_idx] = (self.exp_values[pulled_arm_idx] * (pulls-1) + estimated_reward)/pulls
        self.collected_rewards.append(reward_influence)