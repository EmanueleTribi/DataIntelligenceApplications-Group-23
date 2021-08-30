import numpy as np


class TS_Learner:
    def __init__(self, n_arms, arms, n_categories, adv_id):
        self.adv_id = adv_id
        self.arms = arms
        self.n_categories = n_categories
        self.beta_parameters = np.ones((n_categories, n_arms, 2))
        self.n_arms = n_arms
        self.t = 0
        self.collected_rewards = []

    def update_observations(self, pulled_arm, reward):
        self.collected_rewards = np.append(self.collected_rewards, reward)

  # select the arm to pull
    def pull_arm(self):
        pulled_arm = np.array([])
        for i in range(self.n_categories):
            pulled_arm = np.append(np.argmax(np.random.beta(
                self.beta_parameters[i, :, 0], self.beta_parameters[i, :, 1])))
        return pulled_arm

    def update(self, pulled_arm, reward):
        self.t += 1
        self.update_observations(pulled_arm, reward)
        for i in range(self.n_categories):
            self.beta_parameters[i, pulled_arm[i], 0] += reward
            self.beta_parameters[i, pulled_arm[i], 1] += 1.0 - reward
