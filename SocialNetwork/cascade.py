import numpy as np  
from SocialNetwork.influence_estimation import *
monetary_value_click = [0.3, 0.4, 0.35, 0.7, 0.45]
monetary_value_influence = [0.3, 0.4, 0.35, 0.7, 0.45]

def compute_array_estimated_influence(social_network, rounds):
    array_estimated_influence= np.zeros(len(social_network.adj_matrix[0]))
    fake_array_active = np.zeros(len(social_network.adj_matrix[0]))
    for i in range(0, len(social_network.active_nodes)):
        fake_array_active[i] = 1
        influence_reward = 0
        for _ in range(rounds):
            _, reward = active_nodes_influence(fake_array_active, social_network.adj_matrix, fake_array_active, social_network.categories)
            influence_reward += reward
        influence_reward = influence_reward/rounds
        array_estimated_influence[i] = influence_reward
        fake_array_active[i] = 0
    return array_estimated_influence


def max_reward(social_network=None):
    reward = 0
    for category in social_network.categories:
        reward += monetary_value_click[category-1]
    return reward

def reset_nodes(social_network=None):
    for i in range(0, len(social_network.active_nodes)):
        social_network.active_nodes[i] = 0

#in input, mandare active_nodes=temp, dove temp=np.copy(active_nodes)
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

    
    active_by_click_reward = 0
    for i in range (0, len(active_nodes)):
        if active_nodes[i] == 1:
            active_by_click_reward += monetary_value_click[int(categories[i])-1]
    return active_nodes, active_by_click_reward

def active_nodes_influence(active_nodes, adj_matrix, active_by_click_array, categories):
    active_nodes = leg_sample(adj_matrix, active_nodes)

    active_by_influence_reward = 0
    temporary_array = active_nodes - active_by_click_array
    for i in range (0, len(temporary_array)):
        if temporary_array[i] == 1:
            active_by_influence_reward += monetary_value_influence[int(categories[i])-1]

    return active_nodes, active_by_influence_reward

def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    social_network.active_nodes, active_by_click_reward = active_nodes_click(social_network.active_nodes, social_network.categories, 
                        social_network.weights_fictitious_nodes, ad_allocation_list, slot_prominence, learner_id)
    
    active_by_click_array = np.copy(social_network.active_nodes)

    social_network.active_nodes, active_by_influence_reward = active_nodes_influence(social_network.active_nodes, social_network.adj_matrix, 
                            active_by_click_array, social_network.categories)
    
    return active_by_influence_reward + active_by_click_reward, active_by_click_array


#
#
#
#
#
#
#PSEUDO CODICE PER IL REWARD DEL PUNTO 4
#
#
#
#bid_allocation 
#active_nodes, active_by_click_reward = active_nodes_click(..., bid_allocation, ...)
#total_payments = calculate_total_payment(..., active_nodes)
#reward_influence = 0
#for i in range(0, len(array_estimation)):
#   reward_influence += array_estimation[i] solamente per i nodi attivi
#reward_influence = reward_influence/(numero di nodi attivi)
#
#
#total_reward = active_by_click_reward + reward_influence - total_payments
#