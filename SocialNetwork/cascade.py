from networkx.generators import social
import numpy as np  
from SocialNetwork.influence_estimation import *
monetary_value_click = [4.4, 5, 3.8, 8, 5.2]
monetary_value_influence = [4.4, 5, 3.8, 8, 5.2]

def max_reward(social_network=None):
    reward = 0
    for category in social_network.categories:
        reward += monetary_value_click[category-1]

    return reward
def reset_nodes(social_network=None):
    for i in range(0, len(social_network.active_nodes)):
        social_network.active_nodes[i] = 0

def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    for i in range(0, len(social_network.active_nodes)):
        category = social_network.categories[i]
        node_number = i
        found = False
        for j in range(0, len(ad_allocation_list[category-1])):
            if ad_allocation_list[category-1][j].ad_id == learner_id:
                found = True
                slot = j
                break
        if found:
            active_probability = (slot_prominence[slot])*(social_network.weights_fictitious_nodes[node_number])
            social_network.active_nodes[node_number] = np.random.binomial(n=1, p=active_probability)
    
    active_by_click_reward = 0
    for i in range (0, len(social_network.active_nodes)):
        if social_network.active_nodes[i] == 1:
            active_by_click_reward += monetary_value_click[int(social_network.categories[i])-1]
    temporary_array = np.copy(social_network.active_nodes)

    social_network.active_nodes = leg_sample(social_network.adj_matrix, social_network.active_nodes)

    active_by_influence_reward = 0
    temporary_array = social_network.active_nodes - temporary_array
    for i in range (0, len(temporary_array)):
        if temporary_array[i] == 1:
            active_by_influence_reward += monetary_value_influence[int(social_network.categories[i])-1]
    
    return active_by_influence_reward + active_by_click_reward
""" def cascade(social_network=None):
    new_active = True
    while new_active:
        temporary_array = np.copy(social_network.active_nodes)
        for i in range(0, len(social_network.active_nodes)):
            if social_network.active_nodes[i] == 1:
                for j in range(0, len(social_network.active_nodes)):
                    if social_network.active_nodes[j] == 0:
                        social_network.active_nodes[j] = np.random.binomial(n=1, p=social_network.adj_matrix[i][j])
        temporary_array = social_network.active_nodes - temporary_array
        new_active = False
        for element in temporary_array:
            if element == 1:
                new_active = True
                break
    return social_network.active_nodes """

            
        

    
