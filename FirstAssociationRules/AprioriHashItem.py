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
        
class AprioriHashItemCollection:
    def __init__(self):
        self.data = []
    
    def __iter__(self):
        return iter(self.data)
    
    def at(self, index):
        return self.data[index]
    
    def fromIndexToEnd(self, index):
        return self.data[index : ]
    
    def size(self):
        return len(self.data)
    
    def belongTo(self, item):
        for current_item in self.data:
            if current_item.last_item == item : 
                return True
        return False
        
    def sort(self):
        self.data.sort(key=lambda x: x.last_item, reverse=False)
    
    def addItem(self, hash_item):
        self.data.append(hash_item)
        
    def addTransaction(self, item, tid):
        item_existed = False
        for element in self.data:
            if element.last_item == item:
                element.addTransaction(tid)
                item_existed = True
                break
        if item_existed == False:
            hash_item = AprioriHashItem(item)
            hash_item.addTransaction(tid)
            self.data.append(hash_item)       