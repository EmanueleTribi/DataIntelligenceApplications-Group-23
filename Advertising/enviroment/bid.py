#class to identify who bidded and how much
class Bid(object):
    def __init__(self,bid,id):
        self.bid=bid
        self.ad_id=id
    
    def __str__(self):
        return "bid="+str(self.bid)+", id="+str(self.ad_id)
    def __repr__(self):    
        return "(bid="+str(self.bid)+", id="+str(self.ad_id)+")"
