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
        
        # Here estimating the reward using the pre-computed influences
        reward_influence = 0
        if len(seeds) != 0:
            for i in range(0, len(seeds)):
                reward_influence += self.nodes_estimation[seeds[i]]
            reward_influence = reward_influence/len(seeds)# + reward_influence)/2
            estimated_reward = reward + reward_influence
        else:
            estimated_reward = 0
        
        super().update(pulled_arm_idx, estimated_reward)