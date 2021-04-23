from itertools import combinations,permutations
import numpy as np
# test probability of observing a slot: equivalent to delta_s q_a
#i assume that the quality of the ad is for all 1
deltas=[0.8,0.5,.44,0.40,0.35,0.20]

#this is the best possible auction we can make 

class VCG():
    def __init__(self,deltas=[0.8,0.5,.44,0.40,0.35,0.20]):
        self.deltas=np.array(deltas)

##this is the payment function 
## take in input the payment for a single ad (the bid)
# and the list of all bids, necessary to calculate the VCG payment function
    def payment(self,bid, bids):
        best_allo=self.best_allocation(bids)
        xa=np.inner(self.deltas,np.array(best_allo))
        ya=0
        newbids=bids[:]
        for e in newbids:
            if e.ad_id==bid.ad_id:
                newbids.remove(e)
                break    
        ya=np.inner(self.deltas,np.array(self.best_allocation(newbids)))

        payment=(xa-ya)/deltas[best_allo.index(bid)]
        return payment

## this code finds the best allocation  of 6 ads
## this is a combinatorial problem, given the values of the ads and the probability of
## click an ad in base of the chosen slot and the quality of the ad
## for semplicity we assum quality=1 forall ad
    def best_allocation(self,bids):
        combos= list(permutations(bids, 6))
        values=[]
        for combo in combos:
           
            bidsOfCombo=[]
            for i in combo:
                bidsOfCombo.append(i.bid)
            bidsOfCombo=np.array(bidsOfCombo)    
            values.append(np.inner(combo,self.deltas))
        
        return combos[np.argmax(values)]       
   


