import numpy as np
#this is an example of possible function of given a bid return the number of clicks

def clicks(x):
    return 1-np.exp(-4*x)


class Advertising_envirorment():
    def init(self, bids, sigma):
        self.bids=bids
        self.means=clicks(bids)
        self.sigmas=np.ones(len(bids))*sigma

        #per ora ha una struttura semplice
        #andrà modificato affinchè ritorni un reward in funzione delle features
    def round(self, pulled_arm):
        return np.random.normal(self.means[pulled_arm], self.sigmas[pulled_arm])

    def round_all(self, pulled_arms):
        table=[]
        for pulled_arm in pulled_arms:
            table.append(self.round(pulled_arm))
        return table