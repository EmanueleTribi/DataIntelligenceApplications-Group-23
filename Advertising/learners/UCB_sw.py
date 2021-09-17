import numpy as np
import math
from UCB_Learner import *

class UCB_sw(UCB_Learner):
    def __init__(self, arms, hyperpar, window_size):
        super().__init__(arms, hyperpar)
        self.window_size = window_size
        self.rewards_per_arm = [[] for _ in range(self.n_arms)]
    
    

