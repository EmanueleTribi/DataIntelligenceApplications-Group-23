import numpy as np  
from SocialNetwork.influence_estimation import *
monetary_value = [0.1, 0.1, 0.1, 0.1, 0.1]

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
    
    social_network.active_nodes = leg_sample(social_network.adj_matrix, social_network.active_nodes)
    reward = 0
    count = 0
    for i in range (0, len(social_network.active_nodes)):
        if social_network.active_nodes[i] == 1:
            count+=1
            reward += monetary_value[social_network.categories[i]-1]

    return reward, count


            
        

    
