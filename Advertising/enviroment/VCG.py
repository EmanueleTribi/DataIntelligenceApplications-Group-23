from itertools import combinations,permutations
import numpy as np
import operator
# test probability of observing a slot: equivalent to delta_s(observe prob) q_a(click probability)
#i assume that the quality of the ad is for all 1 (WRONG ASSUMPTION!!!!)
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

## function that finds the best allocation  of 6 ads of a campaign

    def best_allocation(self,bids):
        #make a copy 
        ausiliary_array = bids

        best_allocation = []

        for i in range(0, 5):

            ##TODO: CHECK THE FUNCTION WITH MAX OPERATOR
            
            item = max(ausiliary_array, key=operator.attrgetter('ad_id'))[0]
            best_allocation.append(item)
            ausiliary_array.remove(item)

        return best_allocation
        
    ##function that finds the best allocation of all the campaigns
    def all_best_allocations(self, list_camp_bids):

        best_alloc_all_camp = []
    
        for i in range(0, 4):
            best_alloc_all_camp.append(best_allocation(list_camp_bids(i)))
        
        return best_alloc_all_camp





'''
        combos= list(permutations(bids, 6))
        values=[]
        for combo in combos:
           
            bidsOfCombo=[]
            for i in combo:
                bidsOfCombo.append(i.bid)
            bidsOfCombo=np.array(bidsOfCombo)    
            values.append(np.inner(combo,self.deltas))
        
        return combos[np.argmax(values)]       
'''   


