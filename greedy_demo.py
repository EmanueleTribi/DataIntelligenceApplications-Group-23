from SocialNetwork.cascade import *
import numpy as np
from random import randint
from pprint import pprint
from SocialNetwork.influence_estimation import *
from SocialNetwork.social_network_environment import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *
social_network = social_network_environment()
social_network.init_from_json(json_path_network='Config/network.json', json_path_features='Config/features.json')
deltas=[0.4,0.32,0.27,0.22,0.18,0.05]

## funtion that  returns the marginal increment in the bid of the category passed
## va fatto il controllo che non sia maggiore di 4
    #def get_new_bids(self, category):
       # return self.bids[category]+1
## function that returns the difference beteen the rewards
""" def evaluate_marginal(self, previous_reward, actual_reward):
    return actual_reward - previous_reward


def update_bids(self, bids):
    self.bids = bids """

def keep_going_on(marginal_gain, bids, done_random): 
    if done_random:
        return True
    for i in marginal_gain: 
        if i >= 0: 
            return True
    for i in range(0, len(bids)): 
        if bids[i] > 0: 
            break
    if i == len(bids):
        return True
    return False
        

def bids_simulation(bids, n_adversaries, n_bids, social_network):
    all_bids = []
    all_bids.append(bids)
    for _ in range(0, n_adversaries): 
        adversary_bids = []
        for _ in range(0, n_bids):
            adversary_bids.append(random.randint(0, 4))
        all_bids.append(adversary_bids)

    ad_allocation_list = setup(bids=all_bids, n_bids=n_bids)

    vcg = VCG()
    allocation = vcg.all_best_allocations(list_camp_bids=ad_allocation_list, social_network=social_network)
    payments = vcg.payments(bids=ad_allocation_list, best_allocation=allocation, social_network=social_network)

    return allocation, payments

def setup(bids, n_bids=5):
    bid_objects = []
    #print(bids)
    for i in range(0, n_bids):
        j = 1
        category = []
        for elem in bids: 
            bid = Bid(bid=elem[i], id = j)
            category.append(bid)
            j+=1
        bid_objects.append(category)
    return bid_objects 
    
#function that iterates over the possible bid 
#example: [0 0 0 0 0] -> [1 0 0 0 0], [0 1 0 0 0], [0 0 1 0 0], [0 0 0 1 0], [0 0 0 0 1]
#         [1 0 0 0 0] -> [2 0 0 0 0], [1 1 0 0 0], [1 0 1 0 0], [1 0 0 1 0], [1 0 0 0 1]
#todo: function to evaluate the marginal gain as it should be (for now it is just a random integer)
def evaluate(n_bids, n_adversaries, social_network_environment, learner_bids=[0, 0, 0, 0, 0]):
    previous_reward = 0
    done_random = False
    marginal_gain = np.zeros(n_bids)
    bids = learner_bids
    while keep_going_on(marginal_gain, bids=bids, done_random=done_random):
        new_bid = bids
        marginal_gain = np.zeros(n_bids)
        for i in range(0, n_bids):
            if new_bid[i] != 4:
                new_bid[i] += 1
                #marginal = evaluate_marginal(new_bid)
                array_rewards=[]
                node_counts=[]
                for _ in range(3000):
                    allocation, payments = bids_simulation(new_bid, n_adversaries=n_adversaries, n_bids=n_bids, social_network=social_network_environment)
                    
                    reward_temp, node_count = activate_cascade(social_network=social_network, ad_allocation_list=allocation, 
                            slot_prominence=deltas)
                    reset_nodes(social_network=social_network)
                    reward = reward_temp - payments[i]
                    array_rewards.append(reward)
                    node_counts.append(node_count)
                expected_reward = sum(array_rewards)/len(array_rewards)
                print("Expected activated nodes are " + str(sum(node_counts)/len(node_counts)))
                marginal = expected_reward - previous_reward
                print("Marginal Reward for " + str(new_bid) + " is " + str(marginal))
                if marginal < 0:
                    marginal = -1
                marginal_gain[i] = marginal
                new_bid[i] -= 1
            else: 
                marginal = -2
                marginal_gain[i] = marginal

        max_gain = np.argmax(a = marginal_gain)
        """ if max_gain == 0 and previous_reward == 0:
            random_increment = random.randint(0, 4)
            bids[random_increment] += 1
            done_random = True """
        if marginal_gain[max_gain] >= 0:
            bids[max_gain] += 1
        previous_reward += marginal_gain[max_gain]
        print("The max gain from the previous iteration was " + str(marginal_gain[max_gain]) + " and the new bids are " + str(bids))

            
                    

    return bids

social_network = social_network_environment()
social_network.init_from_json(json_path_network='Config/network.json', json_path_features='Config/features.json')
final = evaluate(n_bids=5, n_adversaries=10, social_network_environment=social_network)








    

            


