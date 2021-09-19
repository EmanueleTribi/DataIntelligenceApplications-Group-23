from Advertising.learners.Greedy_algorithm import *
import numpy as np
from SocialNetwork.social_network_environment import *
from SocialNetwork.cascade import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *

class GTS_Learner():
    def __init__(self, arms, variance=20, ad_id=1):
        self.n_arms = len(arms)
        self.arms = arms
        self.tau = 1/variance  # precision of the Gaussian
        self.tau0 = np.ones(self.n_arms)*0.001
        self.u0 = np.zeros(self.n_arms)
        self.rewards_per_arm = [[] for _ in range(self.n_arms)]
        self.t = 0
        self.ad_id = ad_id
        self.collected_rewards=[]
        self.number_of_pulls = np.zeros(self.n_arms)

    def pull_arm(self):
        values = np.random.normal(self.u0, 1/self.tau0)
        pulled_arm = np.argmax(values)
        self.number_of_pulls[pulled_arm] += 1
        arm = self.arms[pulled_arm]
        return pulled_arm

#per risparmiare tempo passo l'indice dell'arm, e viene pullato insieme alle bid
    def update(self, pulled_arm, reward):
        self.t += 1
        # aggiungo la reward a quelle ottenute
        self.rewards_per_arm[pulled_arm].append(reward)

        self.collected_rewards.append(reward)
        # aggiorno i parametri della normale
        self.tau0[pulled_arm] += self.number_of_pulls[pulled_arm]*self.tau
        rews = np.sum(self.rewards_per_arm[pulled_arm])

        self.u0[pulled_arm] = (self.tau0[pulled_arm]*self.u0[pulled_arm] +
                          self.tau*rews)/(self.tau0[pulled_arm]+(self.number_of_pulls[pulled_arm]*self.tau))
