from Advertising.learners.GTS_Learner import *

class GTS_Learner_qualities(GTS_Learner):

    def __init__(self, arms, variance, ad_id, nodes_estimation):
        super().__init__(arms, variance=variance, ad_id=ad_id)
        self.nodes_estimation = nodes_estimation
    
    def update(self, pulled_arm, reward, seeds):
        # Here estimating the reward using the pre-computed influences
        reward_influence = 0
        if len(seeds) != 0:
            for i in range(0, len(seeds)):
                reward_influence += self.nodes_estimation[seeds[i]]
            reward_influence = reward_influence/len(seeds)# + reward_influence)/2
            estimated_reward = reward + reward_influence
        else:
            estimated_reward = 0

        return super().update(pulled_arm, estimated_reward)