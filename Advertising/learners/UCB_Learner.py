from Advertising.enviroment.bid import Bid
import numpy as np

class UCB_Learner():
    def __init__(self, n_arms, arms, n_categories, ad_id):
        self. n_arms = n_arms
        self.n_categories = n_categories
        self.arms = arms
        self.ad_id = ad_id
        self.reward_per_arm = np.zeros((n_categories, n_arms)) # sum of reward of each arm in each category
        self.empirical_mean = np.ones((n_categories, n_arms))
        self.confidence = np.ones((n_categories, n_arms))*np.inf
        self.count = np.zeros((n_categories, n_arms)) # counting of how many time an arm in pulled in each category
        self.collected_rewards = []
        self.t = 0 #number of executions
        self.c = 2.0  # exploration factor

    def pull_arm(self):
        ucb = self.empirical_mean+self.confidence
        pulled_arm = np.argmax(ucb, axis=-1)
        pulled_arm = self.arms[pulled_arm]
        bids = [Bid(pulled_arm[i], self.ad_id) for i in range(5)]
        return bids

    def update(self, pulled_arm, reward):
        self.t += 1

        self.collected_rewards.append(reward)
        for i in range(self.n_categories):

            self.reward_per_arm[i][pulled_arm[i].bid] += reward
            self.count[i][pulled_arm[i].bid] += 1
            #computation empirical mean reward and confidence
            self.empirical_mean[i][pulled_arm[i].bid
                                   ] = self.reward_per_arm[i][pulled_arm[i].bid]/self.count[i][pulled_arm[i].bid]
            self.confidence[i][pulled_arm[i].bid] = self.c*np.sqrt(
                2*np.log(self.t)/(self.count[i][pulled_arm[i].bid]-1))
            #improvement to force the pulling of all arm    
        for i in range(self.n_categories):
            self.empirical_mean[i][self.count[i] == 0] = np.inf
            self.confidence[i][self.count[i] == 0] = np.inf
