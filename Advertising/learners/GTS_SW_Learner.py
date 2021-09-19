from Advertising.learners.Greedy_algorithm import *
import numpy as np
from SocialNetwork.social_network_environment import *
from SocialNetwork.cascade import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *

class GTS_SW_Learner():
    def __init__(self, arms, variance=20,size_SW=1000 ,ad_id=1):
        self.n_arms = len(arms)
        self.arms = arms
        self.tau = 1/variance  # precision of the Gaussian
        self.tau0 = np.ones(self.n_arms)*0.0001 #prior precision
        self.u0 = np.zeros(self.n_arms) #expected means
        self.rewards_per_arm = [[] for i in range(self.n_arms)] # collection of rewards for each arm
        self.t = 0
        self.ad_id = ad_id #identity of the learner
        self.collected_rewards = []
        self.pulled_arms=np.array([]) #saves which reward is pulled at each round
        self.size_SW=size_SW # window size
        self.collected_tau0=[ []  for i in range(self.n_arms) ]# we collect the precision at each time
        self.number_of_pulls = np.zeros(self.n_arms)
        #to update it while the window moves over time

#sample the new arm from a gaussian distribution
    def pull_arm(self):
        values = np.random.normal(self.u0, 1/self.tau0)
        pulled_arm = np.argmax(values)
        self.pulled_arms=np.append(self.pulled_arms, pulled_arm)
        self.number_of_pulls[pulled_arm] += 1
        return pulled_arm

    def update(self, pulled_arm, reward):
        self.t += 1
        # aggiungo la reward a quele ottenute
        self.rewards_per_arm[pulled_arm].append(reward)
        self.collected_rewards.append(reward)

#to check to take exactly the precisions and rewards inside the window, we use the pulled_arms to check it 
#then we update the parameters
        count=len(np.where(self.pulled_arms[-self.size_SW:]==pulled_arm)[0])
        # self.tau0[pulled_arm] =  np.sum(self.collected_tau0[-count:])+ count*self.tau

        self.tau0[pulled_arm] += count*self.tau
        #self.collected_tau0[pulled_arm].append(self.tau0[pulled_arm])

        rews = np.sum(self.rewards_per_arm[pulled_arm][-count:])

        mean_rews = rews/len(self.rewards_per_arm[pulled_arm][-count:])

        self.u0[pulled_arm] = (self.tau0[pulled_arm]*self.u0[pulled_arm] +
                               self.tau*count*mean_rews)/(self.tau0[pulled_arm]+(count*self.tau))

        # self.u0[pulled_arm] = (self.tau0[pulled_arm]*self.u0[pulled_arm] +
        #                        self.tau*rews)/(self.tau0[pulled_arm]+(count*self.tau))