from Advertising.learners.greedyLearner import *
import numpy as np
from SocialNetwork.social_network_environment import *
from SocialNetwork.cascade import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *


class GTS_SW_Learner():
    def __init__(self, n_arms, arms, variance=20,size_SW=1000 ,ad_id=1):
        self.n_arms = n_arms
        self.arms = arms
        self.tau = 1/variance  # precision of the Gaussian
        self.tau0 = np.ones(n_arms)*0.001
        self.u0 = np.zeros(n_arms)
        self.rewards_per_arm = [[] for i in range(self.n_arms)]
        self.t = 0
        self.ad_id = ad_id
        self.collected_rewards = []
        self.pulled_arms=[]
        self.size_SW=size_SW
        self.collected_tau0=[ []  for i in range(n_arms) ]

    def pull_arm(self):
        values = np.random.normal(self.u0, 1/self.tau0)
        pulled_arm = np.argmax(values)
        self.pulled_arms.append(pulled_arm)
        arm = self.arms[pulled_arm]
        return arm, pulled_arm

#per risparmiare tempo passo l'indice dell'arm, e viene pullato insieme alle bid
    def update(self, pulled_arm, reward, number_of_pulls):
        self.t += 1
        # aggiungo la reward a quelle ottenute
        self.rewards_per_arm[pulled_arm].append(reward)


        self.collected_rewards.append(reward)
        # aggiorno i parametri della normale

        count=len(np.where(np.array(self.pulled_arms[-self.size_SW:])==pulled_arm))
        self.tau0[pulled_arm] =  np.sum(self.collected_tau0[-count:])+ count*self.tau
        self.collected_tau0[pulled_arm].append(self.tau0[pulled_arm])

        rews = np.sum(self.rewards_per_arm[pulled_arm][-count:])

        self.u0[pulled_arm] = (self.tau0[pulled_arm]*self.u0[pulled_arm] +
                               self.tau*rews)/(self.tau0[pulled_arm]+(count*self.tau))
