from Advertising.learners.Greedy_algorithm import *
import numpy as np
import itertools
import random
import math
import time
from SocialNetwork.cascade import *
from Advertising.enviroment.VCG import *


exploration_hyperparameter = 4.2

def arms_creation(seed=None, number_of_arms=-1):
    arms=[]
    if number_of_arms < 0:
        for i in itertools.product([0, 1, 2, 3, 4], repeat = 5):
            arms.append(list(i))
    else: 
        arms=[]
        random.seed(seed)
        for i in range(0, number_of_arms):
            arm = []
            if i == 0:
                arm=[0,0,0,0,0]
            else:
                for i in range(0, 5):
                    arm.append(random.randint(0, 4))
            arms.append(arm)
            
    return arms





def play_once(vcg, arms, adversary_bids, social_network, deltas, learner_id, only_first=False):
    bounds = []
    expected_values = []
    for i in range(0, len(arms)):
        all_bids = []
        all_bids.append(arms[i])
        for element in adversary_bids:
            all_bids.append(element)
        ad_allocation_list = setup(bids=all_bids)
        
        best_allocation = vcg.all_best_allocations(ad_allocation_list, social_network)
        
        if only_first:
            for j in range(0, len(best_allocation)):
                temp_allocation = []
                temp_allocation = best_allocation[j]
                for k in range(0, len(best_allocation[j])):
                    if temp_allocation[k].ad_id == 1 and k != 0:
                        temp_allocation[k].ad_id = None
                        best_allocation[j] = temp_allocation


        payments = vcg.payments(ad_allocation_list, best_allocation, social_network)
        total_reward, active_nodes = activate_cascade(social_network=social_network, ad_allocation_list=best_allocation, slot_prominence=deltas,learner_id=learner_id)

        payments_tot = calculate_total_payment(payments, social_network.categories, active_nodes)

        reward = (total_reward-payments_tot)
        
        bounds.append(0)
        
        expected_values.append(reward)
        reset_nodes(social_network=social_network)

        

        
    return bounds, expected_values






def ucb(arms, n_rounds, adversary_bids, social_network, deltas, learner_id, only_first=False):
    vcg = VCG(deltas=deltas)
    bounds, expected_values = play_once(vcg, arms, adversary_bids, social_network, deltas, learner_id, only_first)
    number_of_pulls = [1]*len(arms)
    sum_expected_values = expected_values.copy()
    thing_to_plot=[]
    thing_to_plot.append(0)
    all_bounds_escalation = [[]for _ in range(0, len(arms))]
    for t in range(1, n_rounds):
        
        best_arm_index = np.argmax(np.add(expected_values, bounds))
        


        all_bids = []
        all_bids.append(arms[best_arm_index])
        for element in adversary_bids:
            all_bids.append(element)
        ad_allocation_list = setup(bids=all_bids, n_bids=5)
        best_allocation = vcg.all_best_allocations(ad_allocation_list, social_network)

        if only_first:
            for j in range(0, len(best_allocation)):
                temp_allocation = []
                temp_allocation = best_allocation[j]
                for k in range(0, len(best_allocation[j])):
                    if temp_allocation[k].ad_id == 1 and k != 0:
                        temp_allocation[k].ad_id = None
                        best_allocation[j] = temp_allocation
                        
        payments = vcg.payments(ad_allocation_list, best_allocation, social_network)



        total_reward, active_nodes = activate_cascade(social_network=social_network, ad_allocation_list=best_allocation, slot_prominence=deltas)
        payments_tot = calculate_total_payment(payments, social_network.categories, active_nodes)
        
        reward = total_reward - payments_tot
        
        thing_to_plot.append((reward+thing_to_plot[-1]*(t-1))/t)
        sum_expected_values[best_arm_index] += reward
        number_of_pulls[best_arm_index] += 1
        expected_values[best_arm_index] = sum_expected_values[best_arm_index]/number_of_pulls[best_arm_index]

        for i in range(0, len(bounds)):
            bounds[i] = exploration_hyperparameter*math.sqrt(np.log(t+1)/number_of_pulls[i])
            all_bounds_escalation[i].append(bounds[i])

        reset_nodes(social_network=social_network)
        
    best_arm_index = np.argmax(expected_values)

    
    return arms[best_arm_index], expected_values, number_of_pulls, best_arm_index, bounds, thing_to_plot, all_bounds_escalation

