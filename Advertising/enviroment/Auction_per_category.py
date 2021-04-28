from Advertising.enviroment.VCG import VCG
from Advertising.enviroment.Advertising_envirorment import Advertising_envirorment
import numpy as np


#la funzione si occupa di gestire l'auction
# prende in ingresso le bids (lista di oggetti bids)
# calcola la allocazione migliore per gli Ads 
# le bids che sono 0 vanno rimosse
class Auction_per_category():
    def __init__(self, category):
       self.vcg=VCG()
       self.category=category
       pass

    def auction(self,bids):
        for bid in bids:
            if bid.bid==0:
                bids.remove(bid)
        best = self.vcg.best_allocation(bids)
        return best   


