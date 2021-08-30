import numpy as np  
from SocialNetwork.influence_estimation import *

def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    node_number = -1
    for element in social_network.active_nodes:
        node_number += 1
        category = social_network.categories[node_number]
        slot = -1
        for element in ad_allocation_list[category-1]:
            slot += 1
            if element.ad_id == learner_id:
                break
        if slot < 6:
            click_probability = (slot_prominence[slot])*(social_network.weights_fictitious_nodes[node_number])
            social_network.active_nodes[node_number] = np.random.binomial(n=1, p=click_probability)
    
    social_network.active_nodes = leg_sample(social_network.adj_matrix, social_network.active_nodes)
    
    total_active=0
    for elem in social_network.active_nodes:
        if elem == 1:
            total_active += 1

    return total_active/len(social_network.active_nodes)


            
        

    
