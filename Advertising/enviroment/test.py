from Advertising.enviroment.Advertising_envirorment import*
from Advertising.enviroment.Auction_per_category import*
from Advertising.learners.GeneralLearner import*
from Advertising.learners.StochasticAdvertiser import*



#variabili locali
 n_arms = 5
 min_bid = 0.0
 max_bid = 4.0
 bids = np.linspace(min_bid, max_bid, n_arms)

 T = 50
 n_experiments = 100

 gpts_learner = GPTSLearner()
# creare enviroment


env =  (bids=)
# creare le auction
# creare i learners
