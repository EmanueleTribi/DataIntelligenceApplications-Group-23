import numpy as np
from Advertising.enviroment.bid import Bid


class TS_Learner:
    def __init__(self, n_arms, arms, n_categories, ad_id):
        self.ad_id = ad_id
        self.arms = arms
        self.n_categories = n_categories
        self.beta_parameters = np.ones((n_categories, n_arms, 2))
        self.n_arms = n_arms
        self.t = 0
        self.collected_rewards = []
        self.prev_reward = np.zeros(n_categories)

    def update_observations(self, pulled_arm, reward):
        self.collected_rewards.append(reward)


    def pull_arm(self):
        bid=[]
        values = np.random.beta(self.beta_parameters[:, :, 0], self.beta_parameters[:, :, 1])
        value_bid = np.argmax(values,axis=-1)
        for i in range(len(value_bid)):
            bid.append(Bid(value_bid[i], self.ad_id))
        return bid

  # select the arm to pull
    # def pull_arm(self):
    #   pulled_arm = []
    # for i in range(self.n_categories):
    #     values = np.random.beta(self.beta_parameters[i, :, 0], self.beta_parameters[i, :, 1])
    #     value_bid = np.argmax(values)
    #    bid = Bid(value_bid, self.ad_id)
    #   pulled_arm.append(bid)
    # return pulled_arm

    def update(self, pulled_arm, reward):
        self.t += 1
        self.update_observations(pulled_arm, reward)
        new=[]
        for i in range(self.n_categories):
            rew=reward[i]/36
            
            self.beta_parameters[i, pulled_arm[i].bid, 0] += rew
            self.beta_parameters[i, pulled_arm[i].bid, 1] += 1.0 - rew
            self.prev_reward[i] = reward[i]

#define a thompson sampling algorithm