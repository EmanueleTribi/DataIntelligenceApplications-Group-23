
from Advertising.enviroment.advertising_environment import Advertising_envirorment
from Advertising.learners.GPTSLearner import GPTS_Learner
from Advertising.learners.GeneralLearner import GeneralLearner
import numpy as np 
from matplotlib import pyplot as plt 

class Auction_Manager():
    def __init__(self,bids,sigma=4):
        self.collected_reward=[]

        env=Advertising_envirorment(bids=bids,sigma=sigma)

        pass

    def auction(self, n_obs, Learner=GeneralLearner()):
        for o in n_obs:
            pulled_arm=Learner.pull_arm()
            reward=self.env.round(pulled_arm)
            Learner.update(pulled_arm=pulled_arm,reward=reward)
        self.collected_reward.append(reward)    
        pass

n_arms=20
min_bid=0.0
max_bid=1.0
bids=np.linspace(min_bid, max_bid, n_arms)
sigma=10
manager=Auction_Manager(bids,sigma)
learner=GPTS_Learner(n_arms,bids)

for e in range(0,100):
   manager.auction(100, learner)

opt=np.max(manager.env.means)
plt.figure(0)
plt.ylabel("Regret")
plt.xlabel("t")
plt.plot(np.cumsum(np.mean(opt-manager.collected_reward,axis=0)), 'g')
plt.show()