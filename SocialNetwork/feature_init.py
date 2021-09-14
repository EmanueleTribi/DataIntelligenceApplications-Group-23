import numpy as np 
from random import randint
import json
from SocialNetwork.network_init import *

def create_features_from_json(json_path_network=None, json_path_features=None):
    if json_path_network != None:
        try:

            net = Network_creator.fromFilename(json_path_network)
            categories = np.array(net.categories)
            
            features_file = open(json_path_features, 'w', encoding='utf-8')


            age = ['y', 'm', 'o']
            gender = ['m', 'f', 'o']
            money = ['poor', 'average', 'rich', 'very rich']
            favourite_hobby = ['music', 'sports', 'reading', 'movies']
            public_personality = ['politician', 'sportsman', 'cinema personality', 'culture', 'scientist']
            verified = [True, False]
            university = ['scientific', 'humanistic', 'other']
            degree = ['none', 'bachelor', 'master', 'phd']
            features_first = {'features' : {'age' : age, 'gender' : gender}, 'probability' : 0.4}
            features_second = {'features' : {'age' : age, 'gender' : gender, 'money' : money}, 'probability' : 0.3}
            features_third = {'features' : {'age' : age, 'gender' : gender, 'favouritehobby' : favourite_hobby}, 'probability' : 0.5}
            features_fourth = {'features' : {'age' : age, 'gender' : gender, 'public personality' : public_personality, 'verified' : verified}, 'probability' : 0.2}
            features_fifth = {'features' : {'age' : age, 'gender' : gender, 'university' : university, 'degree' : degree}, 'probability' : 0.25}
            instances_first = []
            instances_second = []
            instances_third = []
            instances_fourth = []
            instances_fifth = []
            for i in range(categories.shape[0]):
                if categories[i] == 1:
                    features_list_first = {'position' : i, 'age' : randint(0, len(age) - 1), 'gender' : randint(0, len(gender) - 1)}
                    instances_first.append(features_list_first)
                elif categories[i] == 2:
                    features_list_second = {'position' : i, 'age' : randint(0, len(age) - 1), 'gender' : randint(0, len(gender) - 1), 'money' : randint(0, len(money) - 1)}
                    instances_second.append(features_list_second)
                elif categories[i] == 3:
                    features_list_third = {'position' : i, 'age' : randint(0, len(age) - 1), 'gender' : randint(0, len(gender) - 1), 'favourite_hobby' : randint(0, len(favourite_hobby) - 1)}
                    instances_third.append(features_list_third)
                elif categories[i] == 4:
                    features_list_fourth = {'position' : i, 'age' : randint(0, len(age) - 1), 'gender' : randint(0, len(gender) - 1), 'public_personality' : randint(0, len(public_personality) - 1), 'verified' : randint(0, len(verified) - 1)}
                    instances_fourth.append(features_list_fourth)
                elif categories[i] == 5:
                    features_list_fifth = {'position' : i, 'age' : randint(0, len(age) - 1), 'gender' : randint(0, len(gender) - 1), 'university' : randint(0, len(university) - 1), 'degree' : randint(0, len(degree) - 1)}
                    instances_fifth.append(features_list_fifth)
            instances_first_json = {'instances' : instances_first}
            instances_second_json = {'instances' : instances_second}
            instances_third_json = {'instances' : instances_third}
            instances_fourth_json = {'instances' : instances_fourth}
            instances_fifth_json = {'instances' : instances_fifth}
            tuple_first = [features_first, instances_first_json]
            tuple_second = [features_second, instances_second_json]
            tuple_third = [features_third, instances_third_json]
            tuple_fourth = [features_fourth, instances_fourth_json]
            tuple_fifth = [features_fifth, instances_fifth_json]
            categories = []
            categories.append(tuple_first)
            categories.append(tuple_second)
            categories.append(tuple_third)
            categories.append(tuple_fourth)
            categories.append(tuple_fifth)
            dictionary = {'categories': categories}

            json.dump(dictionary, features_file, separators=(',',':'), indent=4)
        except FileNotFoundError:
            print("File not found - network")