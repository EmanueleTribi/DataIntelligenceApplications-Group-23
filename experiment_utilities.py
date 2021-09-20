import itertools
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

def experiment(rounds, learner, all_bids, social_network, arms,first = False, qualities = False, sliding_window = False, interval = None):

    vcg = VCG()

    moving_average = []

    if sliding_window:
        assert isinstance(all_bids,list)
        assert len(all_bids) == (rounds/interval)
    
    step = 0
    bids = all_bids

    for t in trange(0, rounds):
        if sliding_window:
            if t %interval == 0:
                bids = all_bids[step]
                step += 1

        index=learner.pull_arm()
        best_arm = arms[index]


        bids.insert(0, best_arm)
        ad_allocation_list = setup(bids=bids, n_bids=5)
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
        if len(moving_average) == 0:
            moving_average.append(reward)
        else:
            moving_average.append((moving_average[-1] * t + learner.collected_rewards[-1]) / (t+1))

        bids.pop(0)
        reset_nodes(social_network)
    
    return moving_average

def plot_clairvoyant(clairvoyant, moving_average, label, moving_average2=np.array([None]), label2=None, title=None):

    plt.figure()
    plt.axhline(y = clairvoyant, color = 'r', linestyle = '-', label='Clairvoyant')
    plt.plot(moving_average, color = 'b', label=label)
    plt.title(title)
    if moving_average2.all() != None:
        plt.plot(moving_average2, color = 'g', label=label2)
    plt.legend()
    plt.show()


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