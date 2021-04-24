import numpy as np

#this is an example of possible function of given a bid return the number of clicks

def clicks(x):
    return 1-np.exp(-4*x)


class Advertising_envirorment():
    def __init__(self, bids, sigma):
        self.bids=bids
        self.means=clicks(bids)
        self.sigmas=np.ones(len(bids))*sigma

    def round(self, pulled_arm):
        return np.random.normal(self.means[pulled_arm], self.sigmas[pulled_arm])

    def round_all(self, pulled_arms):
        table=np.array([])
        for pulled_arm in pulled_arms:
            table=np.append(table,self.round(pulled_arm))
        return table        

