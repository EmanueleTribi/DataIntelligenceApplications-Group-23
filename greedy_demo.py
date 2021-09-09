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
deltas=[0.5,0.42,0.38,0.30,0.2,0.05]
rounds = 5000
seed = 1234

def keep_going_on(marginal_gain, bids): 
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

    adversary_bids = []
    for _ in range(0, n_adversaries): 
        adversary_i_bids = []
        for _ in range(0, n_bids):
            adversary_i_bids.append(random.randint(0, 4))
        adversary_bids.append(adversary_i_bids)

    for elem in adversary_bids:
        all_bids.append(elem)

    ad_allocation_list = setup(bids=all_bids, n_bids=n_bids)
    vcg = VCG()
    allocation = vcg.all_best_allocations(list_camp_bids=ad_allocation_list, social_network=social_network)
    payments = vcg.payments(bids=ad_allocation_list, best_allocation=allocation, social_network=social_network)

    return allocation, payments

def setup(bids, n_bids=5):
    bid_objects = []
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
def evaluate(n_bids, n_adversaries, social_network_environment):
    learner_bids=np.zeros(n_bids)
    random.seed(seed)
    previous_reward = 0
    marginal_gain = np.zeros(n_bids)
    bids = learner_bids
    while keep_going_on(marginal_gain, bids=bids):
        new_bid = bids.copy()
        marginal_gain = np.zeros(n_bids)
        for i in range(0, n_bids):
            if new_bid[i] != 4:
                new_bid[i] += 1
                array_rewards=[]
                
                for _ in range(rounds):
                    allocation, payments = bids_simulation(new_bid, n_adversaries=n_adversaries, 
                            n_bids=n_bids, social_network=social_network_environment)
                    reward_temp, active_by_click_array = activate_cascade(social_network=social_network, ad_allocation_list=allocation, 
                            slot_prominence=deltas)
                    reset_nodes(social_network=social_network)
                    payments_tot = calculate_total_payment(payments, social_network.categories, active_by_click_array)
                    reward = reward_temp - payments_tot
                    array_rewards.append(reward)
                
                expected_reward = sum(array_rewards)/len(array_rewards)
            
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
        if marginal_gain[max_gain] >= 0:
            bids[max_gain] += 1
        previous_reward += marginal_gain[max_gain]
        if marginal_gain[max_gain] >= 0:
            to_print = str(marginal_gain[max_gain])
        else:
            to_print = "negative"
        print("The max gain from the previous iteration was " + to_print + " and the new bids are " + str(bids))

    return bids

def calculate_total_payment(payments, categories, active_by_click_array):
    payments_tot = 0
    for i in range(0, len(categories)):
        if active_by_click_array[i] == 1:
            payments_tot += payments[int(categories[i])-1]
    return payments_tot

if __name__ == "__main__":
    
    social_network = social_network_environment()
    social_network.init_from_json(json_path_network='Config/network.json', json_path_features='Config/features.json')
    all_best_greedy = []
    for _ in range(0, 30):
        final = evaluate(n_bids=5, n_adversaries=10, social_network_environment=social_network)
        all_best_greedy.append(final) 

    print(all_best_greedy)






    

            


