class AprioriHashItem:
    
    def __init__(self, item):
        self.last_item = item 
        self.tids = []
    
    def addTransaction(self, tid):
        self.tids.append(tid)
        
    def addTransactions(self, tids):
        self.tids.extend(tids)
    
    def size(self):
        return len(self.tids)
        