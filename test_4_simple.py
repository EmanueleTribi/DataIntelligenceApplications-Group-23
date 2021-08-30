#from SocialNetwork.influence_estimation import *
from SocialNetwork.social_network_environment import *
from Advertising.enviroment.bid import *
from Advertising.enviroment.VCG import *

social_network = social_network_environment()
social_network.init_from_json(
    json_path_network='Config/network.json', json_path_features='Config/features.json')
lambdas = [0.8, 0.5, .44, 0.40, 0.35, 0.20]

vcg = VCG()

print(social_network.categories)
