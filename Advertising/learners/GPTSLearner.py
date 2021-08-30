from Advertising.learners.GeneralLearner import *
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C


class GPTS_Learner(GeneralLearner):
    def __init__(self, n_arms, arms, adv_id, n_categories):
        super().__init__(n_arms)
        self.arms = arms
        self.n_categories = n_categories
        self.means = np.zeros((self.n_categories, self.n_arms))
        self.sigmas = np.ones((self.n_categories, self.n_arms)) * 10
        self.adv_id = adv_id
        self.pulled_arms = np.array([])
        self.prew_reward=np.zeros(n_categories)
        # parameters of the GPTS
        alpha = 10.0
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        self.gp = GaussianProcessRegressor(
            kernel=kernel, alpha=alpha ** 2, normalize_y=True, n_restarts_optimizer=9)

    # extend the funtion update_observations of the superclass because we want to
    # update also the list of the pulled arms (together with the rewards and the reward per arm)
    def update_observations(self, pulled_arm, reward):
        super().update_observations(pulled_arm, reward)
        self.pulled_arms = np.append(self.pulled_arms, pulled_arm)

    # function that updates the model(means, sigmas) looking at the new rewards obtained from the enviroment
    def update_model(self):
        for i in range(self.n_categories):
            x = np.atleast_2d([self.pulled_arms[k][i]
                              for k in range(self.t)]).T
            y = np.array([self.collected_rewards[k][i] for k in range(self.t)])
            if len(self.t) > 1:
                self.gp.fit(x, y)
                self.means, self.sigmas = self.gp.predict(
                    np.atleast_2d(self.arms).T, return_std=True)
                self.sigmas = np.maximum(self.sigmas, 1e-2)

    # update the value of the current round and update observation and model
    def update(self, pulled_arms, reward):
        self.t += 1
        self.update_observations(pulled_arms, reward)
        self.update_model()

    # funtion that pulls the arm, it returns the argmax of the distribution given the means and the sigmas
    # pulls a set of arms, one for each category
    def pull_arm(self):
        pulled_arms = np.array([])
        for i in range(self.n_categories):
            sampled_values = np.random.normal(self.means[i], self.sigmas[i])
            pulled_arms = np.append(pulled_arms, np.argmax(sampled_values))
        return pulled_arms
