import numpy as np
import json 

def compute_probabilities(adj_matrix=None, categories=None, feature_values=None, create_json=False):
    i = -1
    for line in adj_matrix:
        i += 1
        j = -1
        for element in line:
            j += 1
            if element == 1:
                category_i = categories[i]
                category_j = categories[j]
                element = activation_probability(category_i=category_i, category_j=category_j, feature_values_i=feature_values[i], feature_values_j=feature_values[j])
                if (category_i == 4 and category_j != 4) or (category_i != 4 and category_j == 4):
                    print(str(i) + ", " + str(j) + "categories are " + str(category_i) + ", " + str(category_j))
                    print(element)
                adj_matrix[i][j] = element
    if create_json:
        new_adj_matrix_file = open("Config/new_adj_matrix_file.json", 'w', encoding='utf-8')
        dictionary = {'adj_matrix': adj_matrix.tolist()}
        json.dump(dictionary, new_adj_matrix_file, separators=(',',':'), indent=4)


def activation_probability(category_i=1, category_j=1, feature_values_i=None, feature_values_j=None, minimum=0.03, maximum=0.7):
    similarity = jaccard_similarity(feature_values_i, feature_values_j)
    if similarity == 0:
        if category_j == 4:
            if feature_values_i.get("verified"):
                return minimum + 0.2
            return minimum + 0.1
        return minimum
    if category_i != category_j and category_j == 4:
        if feature_values_i.get("verified"):
            return maximum*similarity + 0.2
        return maximum*similarity + 0.1
    return maximum*similarity

def jaccard_similarity(vector1=None, vector2=None):
    intersection = 0
    
    for key in vector1:
        if key in vector2 and vector1[key] == vector2[key]:
            intersection += 1
    union = len(vector1) + len(vector2) - intersection
    return float(intersection/union)