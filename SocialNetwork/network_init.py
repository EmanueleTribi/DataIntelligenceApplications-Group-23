import os
import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import random
from ast import literal_eval

class Network_creator:

    #Creates Barabasi-Albert Network with N nodes and M initial edges for each node
    def __init__(self, nodes = 50, start_edges = 5, adj_matrix = None):
        self.nodes = nodes
        self.start_edges = start_edges

        #clear creation
        if adj_matrix.any():
            self.graph = nx.barabasi_albert_graph(n = nodes, m = start_edges)
            self.categories = np.empty(shape = self.nodes)
            self.adj_matrix = nx.adjacency_matrix(self.graph)

            for i in range(self.nodes):
                self.categories[i] = random.randint(1,5)

        #needed for fromFilename purposes
        else:
            self.adj_matrix = adj_matrix
            self.graph = nx.from_numpy_matrix(adj_matrix)
     
    
    #Generates a Network from adjacency matrix in specified file
    @classmethod
    def fromFilename(cls, json_path):
        try:
            with open(json_path, 'r') as network_file:

                if(os.path.getsize(json_path) == 0):
                    print("File is empty, creating a network with default parameters...")
                    return cls()
                
                net_dict = json.load(network_file)

                net = cls(nodes = net_dict["nodes"], 
                          start_edges = net_dict["start_edges"],
                          adj_matrix = np.array(net_dict["adj_matrix"]))

                net.categories = net_dict["categories"]
                
                return net
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
        nx.draw_random(self.graph, with_labels = labels)
        plt.show()
    
    #Creates JSON file storing the adjacency matrix of the Network
    def generate_json(self):
        file_path = "SocialNetwork/network.json"
        network_file = open(file_path, 'w', encoding='utf-8')

        net_dict = {"nodes": self.nodes,
                    "start_edges": self.start_edges,
                    "categories": self.categories.tolist(),
                    "adj_matrix": self.adj_matrix.tolist()
                    }
       
        json.dump(net_dict, network_file, separators=(',',':'))

        network_file.close()


