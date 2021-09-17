from Advertising.enviroment.VCG import *
from SocialNetwork.cascade import *
from Advertising.learners.Greedy_algorithm import *

import random

def test_sw(learner, arms, list_adv_bids, only_first,  n_rounds, lambdas, social_network, interval):
    vcg = VCG(lambdas)
    number_of_pulls = np.zeros(len(arms))
    sum_expected_values = np.zeros(len(arms))
    expected_values = np.zeros(len(arms))
    thing_to_plot = []
    thing_to_plot.append(0)
    adversary_bids = []
    times_change = 0
    for i in range(0, n_rounds):
        if i %interval == 0: 
            adversary_bids = list_adv_bids[times_change]
            times_change += 1
            thing_to_plot.append(0)

        arm_learner, pulled_arm = learner.pull_arm()


        all_bids = []
        all_bids.append(arm_learner)
        for element in adversary_bids:
            all_bids.append(element)
        ad_allocation_list = setup(bids=all_bids, n_bids=5)

        best_allocation = vcg.all_best_allocations(
            list_camp_bids=ad_allocation_list, social_network=social_network)

        if only_first:
            for j in range(0, len(best_allocation)):
                temp_allocation = []
                temp_allocation = best_allocation[j]
                for k in range(0, len(best_allocation[j])):
                    if temp_allocation[k].ad_id == 1 and k != 0:
                        temp_allocation[k].ad_id = None
                        best_allocation[j] = temp_allocation

        total_reward, active_nodes = activate_cascade(
            social_network=social_network, ad_allocation_list=best_allocation, slot_prominence=deltas)

        payments = vcg.payments(
            ad_allocation_list, best_allocation, social_network=social_network)
    # with this part of code i set that if the learner is present in the allocation list then get the normal allocation
    # reward, if it's not present and it bids 0 then the reward is 0.

        payments_tot = calculate_total_payment(
            payments, social_network.categories, active_nodes)

        reward = total_reward - payments_tot

        if i > 0:
            thing_to_plot.append((reward+thing_to_plot[-1]*(i-1))/i)

        number_of_pulls[pulled_arm] += 1
        sum_expected_values[pulled_arm] += reward
        expected_values[pulled_arm] = sum_expected_values[pulled_arm]/ number_of_pulls[pulled_arm]

    # updating of the learners
        learner.update(pulled_arm, reward, number_of_pulls)
        reset_nodes(social_network=social_network)

    best_arm_index = np.argmax(expected_values)


    return arms[best_arm_index], best_arm_index, number_of_pulls, expected_values, thing_to_plot
