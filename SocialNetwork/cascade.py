from networkx.generators import social
import numpy as np  
from SocialNetwork.influence_estimation import *
monetary_value_click = [0.3, 0.4, 0.35, 0.7, 0.45]
monetary_value_influence = [0.3, 0.4, 0.35, 0.7, 0.45]

def max_reward(social_network=None):
    reward = 0
    for category in social_network.categories:
        reward += monetary_value_click[category-1]

    return reward
def reset_nodes(social_network=None):
    for i in range(0, len(social_network.active_nodes)):
        social_network.active_nodes[i] = 0

def active_nodes_click(active_nodes, categories, qualities, ad_allocation_list, slot_prominence, learner_id):
    for i in range(0, len(active_nodes)):
        category = categories[i]
        node_number = i
        found = False
        for j in range(0, len(ad_allocation_list[int(category)-1])):
            if ad_allocation_list[category-1][j].ad_id == learner_id:
                found = True
                slot = j
                break
        if found:
            active_probability = ((slot_prominence[slot]*slot_prominence[slot])/slot_prominence[0])*(qualities[node_number])
            active_nodes[node_number] = np.random.binomial(n=1, p=active_probability)
    return active_nodes


def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    social_network.active_nodes = active_nodes_click(social_network.active_nodes, social_network.categories, 
                        social_network.weights_fictitious_nodes, ad_allocation_list, slot_prominence, learner_id)
    
    active_by_click_reward = 0
    for i in range (0, len(social_network.active_nodes)):
        if social_network.active_nodes[i] == 1:
            active_by_click_reward += monetary_value_click[int(social_network.categories[i])-1]
    active_by_click_array = np.copy(social_network.active_nodes)

    social_network.active_nodes = leg_sample(social_network.adj_matrix, social_network.active_nodes)

    active_by_influence_reward = 0
    temporary_array = social_network.active_nodes - active_by_click_array
    for i in range (0, len(temporary_array)):
        if temporary_array[i] == 1:
            active_by_influence_reward += monetary_value_influence[int(social_network.categories[i])-1]
    
    return active_by_influence_reward + active_by_click_reward, active_by_click_array
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

            
        

    
