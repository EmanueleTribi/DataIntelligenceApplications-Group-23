import os
import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
from ast import literal_eval

class Network_creator:

    #Creates Barabasi-Albert Network with N nodes and M initial edges for each node
    def __init__(self, nodes = 50, edges = 5, graph = None):
        self.nodes = nodes
        self.edges = edges

        if graph == None:
            self.graph = nx.barabasi_albert_graph(n = nodes, m = edges)
        else:
            self.graph = graph
    
    #Generates a Network from adjacency matrix in specified file
    @classmethod
    def fromFilename(cls, json_path):
        try:
            with open(json_path, 'r') as network_file:

                if(os.path.getsize(json_path) == 0):
                    print("File is empty, creating a network with default parameters...")
                    return cls()
                
                adj_matrix_string = json.load(network_file)
                adj_matrix = np.array(literal_eval(adj_matrix_string))
                
                graph = nx.from_numpy_matrix(adj_matrix)
                nodes,_ = adj_matrix.shape
                
                return cls(nodes = nodes, edges = _, graph = graph)
        except FileNotFoundError:
            print("File not found, creating a network with default parameters...")
            return cls()
                

    def visualize(self, labels=True):

        options = {
                "font_size": 12,
                "node_size": 50,
                "node_color": "white",
                "edgecolors": "black",
                "linewidths": 1,
                "width": 2,
                }
        
        #nx.draw_networkx(self.graph, arrows=False, with_labels=labels, **options)
        nx.draw_random(self.graph, with_labels = True)
        plt.show()
    
    #Creates JSON file storing the adjacency matrix of the Network
    def generate_json(self):
        adj_mat = nx.adjacency_matrix(self.graph).toarray()
        file_path = "SocialNetwork/network.json"
        network_file = open(file_path, 'w', encoding='utf-8')
        
        json_string = json.dumps(adj_mat.tolist())
        json.dump(json_string, network_file, separators=(',',':'))

        network_file.close()


