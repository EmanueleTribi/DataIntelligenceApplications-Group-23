from tqdm.notebook import trange
from SocialNetwork.social_network_environment import *
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from Advertising.learners.Greedy_algorithm import *


def create_adv_bids():
    
    adversary_bids = []
    for _ in range(0, 10): 
        adversary_i_bids = []
        for _ in range(0, 5):
            adversary_i_bids.append(random.randint(0, 4))
        adversary_bids.append(adversary_i_bids)
    return adversary_bids

def experiment(rounds, learner, all_bids, social_network, arms,first = False, qualities = False):

    vcg = VCG()

    moving_average = []
    moving_average.append(0)

    for t in range(0, rounds):

        index=learner.pull_arm()
        best_arm = arms[index]


        all_bids.insert(0, best_arm)
        ad_allocation_list = setup(bids=all_bids, n_bids=5)
        best_allocation = vcg.all_best_allocations(ad_allocation_list, social_network)

        if first:
            for j in range(0, len(best_allocation)):
                temp_allocation = []
                temp_allocation = best_allocation[j]
                for k in range(0, len(best_allocation[j])):
                    if temp_allocation[k].ad_id == 1 and k != 0:
                        temp_allocation[k].ad_id = None
                        best_allocation[j] = temp_allocation

        # Computing payments
        payments = vcg.payments(ad_allocation_list, best_allocation, social_network)

        if qualities:
            active_nodes, total_reward = active_nodes_click(social_network, best_allocation, deltas, learner_id=1)
        else:     
            active_nodes, total_reward = activate_cascade(social_network=social_network, ad_allocation_list=best_allocation, slot_prominence=deltas,learner_id=1)

        payments_tot = calculate_total_payment(payments, social_network.categories, active_nodes)


        reward = (total_reward-payments_tot)

        if qualities:
            learner.update(index, reward, np.where(active_nodes==1)[0])
        else:
            learner.update(index, reward)
        
        moving_average.append((moving_average[-1] * t + learner.collected_rewards[-1]) / (t+1))

        all_bids.pop(0)
        reset_nodes(social_network)
    
    return moving_average

def plot_clairvoyant(clairvoyant, moving_average):

    plt.figure()
    plt.axhline(y = clairvoyant, color = 'r', linestyle = '-')
    plt.plot(moving_average, color = 'b')
    plt.show()
