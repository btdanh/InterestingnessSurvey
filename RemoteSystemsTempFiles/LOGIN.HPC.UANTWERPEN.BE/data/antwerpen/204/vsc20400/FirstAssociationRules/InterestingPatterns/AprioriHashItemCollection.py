from InterestingPatterns.AprioriHashItem import AprioriHashItem

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
        
    def findLastItem(self, item):
        left = 0
        right = len(self.data) - 1
        while (left <= right):
            pivot = int((left + right)/2)
            if self.data[pivot].last_item == item: 
                return pivot
            if self.data[pivot].last_item < item:
                left = pivot + 1
            else:
                right = pivot - 1 
        return -1
        
    def addTransaction(self, item, tid):
        index = self.findLastItem(item)
        if index == -1:
            hash_item = AprioriHashItem(item)
            hash_item.addTransaction(tid)
            
            index = len(self.data) - 1
            self.data.append(hash_item)
            
            while index >= 0:
                if self.data[index].last_item > item:
                    self.data[index + 1] = self.data[index]
                    index -= 1
                else:
                    break
            self.data[index + 1] = hash_item        
        else:
            self.data[index].addTransaction(tid)
            