import numpy as np  
from SocialNetwork.influence_estimation import *
monetary_value_click = [0.32, 0.48, 0.8, 1.6, 0.4]
monetary_value_influence = [0.32, 0.48, 0.8, 1.6, 0.4]

def reset_nodes(social_network=None):
    for i in range(0, len(social_network.active_nodes)):
        social_network.active_nodes[i] = 0



def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    node_number = -1
    for element in social_network.active_nodes:
        node_number += 1
        category = social_network.categories[node_number]
        slot = -1
        found = False
        for element in ad_allocation_list[category-1]:
            slot += 1
            if element.ad_id == learner_id:
                found = True
                break
        if found:
            click_probability = (slot_prominence[slot])*(social_network.weights_fictitious_nodes[node_number])
            social_network.active_nodes[node_number] = np.random.binomial(n=1, p=click_probability)
    
    active_by_click_reward = 0
    for i in range (0, len(social_network.active_nodes)):
        if social_network.active_nodes[i] == 1:
            active_by_click_reward += monetary_value_click[social_network.categories[i]-1]
    temporary_array = np.copy(social_network.active_nodes)

    social_network.active_nodes = leg_sample(social_network.adj_matrix, social_network.active_nodes)

    active_by_influence_reward = 0
    temporary_array = social_network.active_nodes - temporary_array
    for i in range (0, len(temporary_array)):
        if temporary_array[i] == 1:
            active_by_influence_reward += monetary_value_influence[social_network.categories[i]-1]

    return active_by_influence_reward + active_by_click_reward


            
        

    
