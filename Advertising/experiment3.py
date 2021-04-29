import numpy as np
from Advertising.enviroment.Advertising_envirorment import*
from Advertising.learners.greedyLearner import*

## initialize enviroment and bids
n_bids = 5
bids_t = np.zeros(n_bids)
bids = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
env = Advertising_envirorment(bids=bids, sigma=sigma)

gr_learner = greedyLearner(n_bids=n_bids, bids=bids_t)

reward_t = 0
rewards = []
## repeate until there is no positive gain
## explore possible increments, evaluate the rewards, if the argmax of the rewards is <0 or 
## the list of the next level of exploration is empty exit, otherwise keep going
while True:
    bids_next = level_exploration(bids_t)
    
    ##calculate all rewards
    for possible_bids in bids_next
        rewards.append(env.round(pulled_arms=possible_bids))
    
    ##best reward
    ind_max = np.argmax(rewards)
    reward_next = rewards[ind_max]
    
    ## control to exit the while
    if (gr_learner.evaluate_marginal(reward_t, reward_next) < 0) | !bids_next:
    break
    
    
    ## keep the bids that gave the best reward as next bids list to explore
    ## and the best reward found for the next cycle
    bids_t = bids_next[ind_max]
    gr_learner.update_bids(bids_t)
    reward_t = reward_next



best_bids = bids_t
final_reward = reward_t

## maybe do a plot with the progress of the reward
