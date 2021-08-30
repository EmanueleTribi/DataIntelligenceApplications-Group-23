from itertools import combinations,permutations
import numpy as np
import operator
# test probability of observing a slot: equivalent to delta_s(observe prob) q_a(click probability)
#i assume that the quality of the ad is for all 1 (WRONG ASSUMPTION!!!!)
deltas=[0.8,0.5,.44,0.40,0.35,0.20]

#this is the best possible auction we can make 
# test probability of observing a slot: equivalent to delta_s(observe prob) q_a(click probability)
#i assume that the quality of the ad is for all 1 (WRONG ASSUMPTION!!!!)
deltas=[0.8,0.5,.44,0.40,0.35,0.20]

#this is the best possible auction we can make 

class VCG():
    def __init__(self,deltas=deltas):
        self.deltas=np.array(deltas)

    
    #bids = bids made by ALL the advertires 
    #campaign = category, needed to extract from the social network the click probability 
    #social newtwork = explained before why we need it 
    #allocation lenght = how long should the allocation be, by default it is 6
    def best_allocation(self, bids, campaign, social_network=None, allocation_length=6):
        #make a copy 
        ausiliary_array = bids

        #quality is the same for all the nodes belonging to a certain category and it is saved 
        #in the social network - so I will take the first node of the considered category
        index_first_node = np.where(social_network.categories == campaign)[0][0]
        quality = social_network.weights_fictitious_nodes[index_first_node]

        best_allocation = []

        for i in range(0, allocation_length):
            item = max(ausiliary_array, key=lambda item:item.bid*quality)
            if(item.bid != 0):
                best_allocation.append(item)
            ausiliary_array = np.delete(ausiliary_array, np.where(np.array(ausiliary_array) == item))

        
        return best_allocation
        
    #can be divided maybe in two functions, as we do for the best allocation
    def payments(self, bids, best_allocation, social_network=None):
        #the payment list will be an array of dimension 5. array[i] == payment for category i+1 
        payments=[]
        
        for i in range(0, len(best_allocation)): #len(best_allocation) = number of campaigns
            found = False
            #reasoning about quality same as before 
            index_first_node = np.where(social_network.categories == i+1)[0][0]
            quality = social_network.weights_fictitious_nodes[index_first_node]

            for j in range(0, len(best_allocation[i])): #for each ad displayed in the slots...
                if best_allocation[i][j].ad_id == 1:
                    found = True
                    auxiliary=[]
                    #take the bids without the player and find the new best allocation
                    #NB - np.delete() removes the INDEX, so j is right, putting "player" would be wrong
                    auxiliary = np.delete(bids[i], j) 
                    auxiliary_allocation = self.best_allocation(bids=auxiliary, campaign=i+1, 
                                social_network=social_network, allocation_length=6) 
                    
                    #calculate x_a
                    x_a = 0
                    for k in range(0, len(auxiliary_allocation)):
                        x_a += deltas[k]*quality*auxiliary_allocation[k].bid

                    #calculate y_a
                    y_a = 0
                    for k in range(0, len(best_allocation[i])):
                        if best_allocation[i][k].ad_id != 1:
                            y_a += deltas[k]*quality*best_allocation[i][k].bid

                    #calculate the payment of player i for this allocation 
                    div = 0
                    div = deltas[j]*quality
                    
                    payment = 0
                    payment = (1/div) * (x_a-y_a)
                    payments.append(payment) ##CHECK

            #if i don't find the player in the best allocation, the payment will be 0
            if not found:
                payments.append(float(0))
               
        

        return payments


                        



            
             

        
    ##function that finds the best allocation of all the campaigns
    def all_best_allocations(self, list_camp_bids, social_network=None):
        best_alloc_all_camp = []
        
        for i in range(0, 5):
            best_alloc_all_camp.append(self.best_allocation(bids=list_camp_bids[i], campaign=i+1, social_network=social_network))

        #for now I wont return the payments since they have to be done better
        return best_alloc_all_camp#, self.payments(bids=list_camp_bids, best_allocation=best_alloc_all_camp)


'''
##this is the payment function 
## take in input the payment for a single ad (the bid)
# and the list of all bids, necessary to calculate the VCG payment function
    def payments(self, bids):
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
'''
