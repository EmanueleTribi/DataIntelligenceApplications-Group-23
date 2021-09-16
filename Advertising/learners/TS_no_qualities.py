from Advertising.learners.greedyLearner import *
import matplotlib.pyplot as plt
import numpy as np
from SocialNetwork.social_network_environment import *
from SocialNetwork.cascade import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *
import itertools



def arms_creation(seed=None, number_of_arms=-1):
    arms = []
    if number_of_arms < 0:
        for i in itertools.product([0, 1, 2, 3, 4], repeat=5):
            arms.append(list(i))
    else:
        random.seed(seed)

        arms = []
        for i in range(0, number_of_arms):
            arm = []
            for i in range(0, 5):
                arm.append(random.randint(0, 4))
            arms.append(np.array(arm))
    return arms


def test(learner, arms, adversary_bids, only_first, active_by_influence_reward, n_rounds, lambdas, social_network):
    
    vcg = VCG(lambdas)
    number_of_pulls = [0]*len(arms)
    sum_expected_values = [0]*len(arms)
    expected_values = [0]*len(arms)
    thing_to_plot = []
    for i in range(0, n_rounds):

        
        arm_learner, pulled_arm = learner.pull_arm()

        all_bids=[]
        all_bids.append(arm_learner)
        for element in adversary_bids:
            all_bids.append(element)
        ad_allocation_list = setup(bids=all_bids, n_bids=5)
    
        best_allocation = vcg.all_best_allocations(list_camp_bids=ad_allocation_list, social_network=social_network)

        if only_first:
            for j in range(0, len(best_allocation)):
                temp_allocation = []
                temp_allocation = best_allocation[j]
                for k in range(0, len(best_allocation[j])):
                    if temp_allocation[k].ad_id == 1 and k != 0:
                        temp_allocation[k].ad_id = None
                        best_allocation[j] = temp_allocation


                       
        active_nodes, click_rewards = active_nodes_click( social_network, best_allocation, lambdas, 1)
        payments = vcg.payments(ad_allocation_list, best_allocation, social_network=social_network)
    # with this part of code i set that if the learner is present in the allocation list then get the normal allocation
    # reward, if it's not present and it bids 0 then the reward is 0.
        payments_tot = calculate_total_payment(payments, social_network.categories, active_nodes)

        
        reward = 0
        reward_influence = 0
        indexes = np.where(active_nodes == 1)[0]

        if len(indexes) != 0:
            for i in range(0, len(indexes)):
                reward_influence += active_by_influence_reward[i]
            reward_influence = (reward_influence/len(indexes) + reward_influence)/2                
            reward = (click_rewards + reward_influence - payments_tot)
        thing_to_plot=[]
        # if i==1:
        #     thing_to_plot.append(reward)
        # else:
        #     thing_to_plot.append((reward+thing_to_plot[-1]*(i-1))/i)    
        number_of_pulls[pulled_arm] += 1
        sum_expected_values[pulled_arm] += reward
        expected_values[pulled_arm] = sum_expected_values[pulled_arm]/number_of_pulls[pulled_arm]
        
        
        
        
        reset_nodes(social_network=social_network)

        #rew = reward-np.sum(payments_tot)

    # updating of the learners
        learner.update(pulled_arm, reward, number_of_pulls)
    
    best_arm_index = np.argmax(expected_values)

    print(expected_values)
    print(best_arm_index)

    return arms[best_arm_index], best_arm_index, number_of_pulls, expected_values, thing_to_plot


        

    # plt.figure(0)
    # plt.xlabel('round')
    # plt.ylabel('reward')
    # plt.plot(learner.collected_rewards)
    # plt.show()

    # print("THE BEST ARM IS:",
    #       arms[learner.pull_arm()[1]], "INDEX",learner.pull_arm()[1])
    # array = [i+1 for i in range(0, 20)]

    # plt.figure(1)
    # plt.errorbar(array, ts_learner.u0, yerr=(1/ts_learner.tau0)*5, fmt='o')
    # plt.show()
    


