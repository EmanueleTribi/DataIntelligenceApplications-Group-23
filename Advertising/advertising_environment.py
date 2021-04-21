import numpy as np

#this is an example of possible function of given a bid return the number of clicks
class Clicks():
    def clicks(x):
        return 1-np.exp(-4*x)


class Advertising_envirorment():
    def __init__(self, bids, sigma, clicks):
        self.bids=bids
        self.means=clicks.clicks(bids)
        self.sigmas=np.ones(len(bids))*sigma

    def round(self, pulled_arm):
        return np.random.normal(self.means[pulled_arm], self.sigmas[pulled_arm])

    def round_all(self, pulled_arms):
        table=[]
        for pulled_arm in pulled_arms:
            table.append(self.round(pulled_arm))
        return table        

