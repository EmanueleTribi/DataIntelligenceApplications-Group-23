from social_network_environment import social_network_environment
import numpy as np  

def activate_cascade(social_network=None, ad_allocation_list=None, learner_id=1, slot_prominence=None):
    
    node_number = -1
    for element in social_network.active_nodes:
        node_number += 1
        category = social_network.categories[node_number]
        slot = -1
        for element in ad_allocation_list[category]:
            slot += 1
            if element.ad_id == learner_id:
                break
        if slot < 6:
            click_probability = (slot_prominence[slot])*(social_network.weights_fictitious_nodes[node_number])
            social_network.active_nodes[node_number] = np.random.binomial(n=1, p=click_probability)
    
    cascade(social_network.adj_matrix, social_network.active_nodes)

def cascade(adj_matrix, active_nodes):
    already_visited = np.zeros(shape=len(active_nodes))
    go_on = True
    while go_on:
        go_on = False
        i = -1
        for element in active_nodes:
            i += 1
            if element == 1 and already_visited[i] != 1:
                already_visited[i] = 1
                j = -1
                for element in adj_matrix[i]:
                    j += 1
                    if adj_matrix[i][j] != 0 and active_nodes[j] != 1:
                        active_nodes[j] = np.random.binomial(n=1, p=adj_matrix[i][j]) 
                        if active_nodes[j] == 1:
                            go_on = True



            
        

    
