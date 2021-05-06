import numpy as np
import json
from ast import literal_eval
from random import randint
from activation_probabilities import *

class social_network_environment:

    def __init__(self, active_nodes=None, adj_matrix=None, weights_fictitious_nodes=None, 
            categories=None, features_names=None, features_domain = None, features_instances=None):
        self.active_nodes = active_nodes
        self.adj_matrix = adj_matrix
        #self.fictitious_nodes = fictitious_nodes
        # Is an array of 1s useful to represent fictitious? 
        self.weights_fictitious_nodes = weights_fictitious_nodes
        self.categories = categories
        self.features_names = features_names
        self.features_domain = features_domain
        self.features_instances = features_instances

    
    def init_from_json(self, json_path_network=None, json_path_features=None):
        if json_path_network != None:
            try:
                with open(json_path_network, 'r') as network_file:
                    data = json.load(network_file)
                    matrix = np.array(data.get('adj_matrix'))
                    self.adj_matrix = matrix.astype(dtype=np.float)
                    self.categories = np.array(data.get('categories'))
                    n_nodes = self.categories.shape[0]
                    self.active_nodes = np.zeros(n_nodes)
                    #self.fictitious_nodes = np.ones(n_nodes) 
                    # Is an array of 1s useful to represent fictitious? 
                    self.weights_fictitious_nodes = np.ones(n_nodes)
                     
            except FileNotFoundError:
                print("File not found - network")
        
        if json_path_features != None:
            try:
                with open(json_path_features, 'r') as features_file:
                    data = json.load(features_file)
                feature_list = []
                domain_list = []
                first = data.get('categories')[0]
                second = data.get('categories')[1]
                third = data.get('categories')[2]
                fourth = data.get('categories')[3]
                fifth = data.get('categories')[4]
                feature_categories_list = [first[0], second[0], third[0], fourth[0], fifth[0]]
                for element in feature_categories_list:
                    features = element.get('features')
                    for element_bis in features:
                        if element_bis not in feature_list:
                            feature_list.append(element_bis)
                            domain_list.append(features.get(element_bis))
                self.features_names = feature_list
                self.features_domain = domain_list

                # Creating an ordered list of the respective features for each node
                first_instances = (data.get('categories')[0])[1].get('instances')
                second_instances = (data.get('categories')[1])[1].get('instances')
                third_instances = (data.get('categories')[2])[1].get('instances')
                fourth_instances = (data.get('categories')[3])[1].get('instances')
                fifth_instances = (data.get('categories')[4])[1].get('instances')
                
                all_instances = first_instances + second_instances + third_instances + fourth_instances + fifth_instances
                all_instances = sorted(all_instances, key = lambda x: x['position'])
        
                self.features_instances = all_instances
                
            except FileNotFoundError:
                print("File not found - features")

    def preliminary_operations(self):
        compute_probabilities(adj_matrix=self.adj_matrix, categories=self.categories,
                                                feature_values=self.features_instances)
