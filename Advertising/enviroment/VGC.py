from itertools import combinations,permutations
import numpy as np
# test probability of observing a slot: equivalent to delta_s q_a
deltas=[0.8,0.5,.44,0.40,0.35,0.20]

#this is the best possible auction we can make 
#le statistiche di click le calcolerò poi con qualche formula a caso rubata dal
# egidio Battistini

class VCG():
    def __init__(self,deltas=[0.8,0.5,.44,0.40,0.35,0.20]):
        self.deltas=np.array(deltas)

    def payment(self,bid, bids):
        newbids=bids[:]
        newbids.remove(bid)
        best_allo=self.best_allocation(bids)
        xa=np.inner(self.deltas,np.array(best_allo))
        ya=0
        newbids=bids[:]
        newbids.remove(bid)
        ya=np.inner(self.deltas,np.array(self.best_allocation(newbids)))

        delta=0
        if bid in best_allo:
            delta=self.deltas[best_allo.index(bid)]
        else:
            delta=0
        payment=(xa-ya)/deltas[best_allo.index(bid)]
        return payment


    def best_allocation(self,bids):
        combos= list(permutations(bids, 6))
        values=[]
        for combo in combos:
            combo=np.array(combo)
            print(combo)
            values.append(np.inner(combo,self.deltas))
        
        return combos[np.argmax(values)]       
   


