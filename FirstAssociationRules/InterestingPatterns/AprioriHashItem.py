import json

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
    
    def toString(self):
        return json.dumps((self.last_item, self.tids))
    
    def loadFromString(self, jsonString):
        result = json.loads(jsonString)
        self.last_item = result[0]
        self.tids = result[1]
        