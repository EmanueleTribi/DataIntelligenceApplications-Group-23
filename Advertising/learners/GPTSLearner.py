from GeneralLearner import*
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

class GPTS_Learner(GeneralLearner):
    def __init__(self, n_arms, arms, adv_id):
        super().__init__(n_arms)
        self.adv_id = adv_id
        self.arms = arms
        self.means = np.zeros(self.n_arms)
        self.sigmas = np.ones(self.n_arms)*10
        self.pulled_arms = []
    ## parameters of the GPTS       
        alpha = 10.0
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-3, 1e3))
        self.gp = GaussianProcessRegressor(kernel=kernel, alpha = alpha**2, normalize_y=True, n_restarts_optimizer = 9)

## extend the funtion update_observations of the superclass because we want to 
## update also the list of the pulled arms (together with the rewards and the reward per arm)
    def update_observations(self, arm_idx, reward):
        super().update_observations(arm_idx, reward)
        self.pulled_arms.append(self.arms[arm_idx])

## funtion that updates the model(means, sigmas) looking at the new rewards obtained from the enviroment
    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards
        self.gp.fit(x,y)
        self.means, self.sigmas = self.gp.predict(np.atleast_2d(self.arms).T, return_std = True)
        self.sigmas = np.maximum(self.sigmas, 1e-2)
    
## update the value of the current round and update observation and model    
    def update(self, pulled_arms, reward):
        self.t += 1
        self.update_observations(pulled_arms, reward)
        self.update_model()
    
## funtion that pulls the arm, it returns the argmax of the distribution given the means and the sigmas
    def pull_arm(self):
        sampled_values = np.random.normal(self.means, self.sigmas)
        return np.argmax(sampled_values)


    


