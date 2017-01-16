from AprioriHashItem import AprioriHashItemCollection

class AprioriHashTable:
    def __init__(self):
        self.table = {}
    
    def isEmpty(self):
        return len(self.table) == 0;
    
    # insert a new key into the table
    def insertKey(self, key):
        self.table[key] = AprioriHashItemCollection()
        
    # remove a key from the table
    def removeKey(self, key):
        self.table.pop(key, None)
        
    # insert a new transaction id into a specific item-set
    def addTransaction(self, key, item, tid):
        self.table[key].addTransaction(item, tid)
        
    # insert a item set and its transaction 
    def addItemset(self, key, hash_item):
        self.table[key].addItem(hash_item)
        
    # get a item-set from its key
    def getItemsetFromKey(self, key):
        if key == '':
            return []
        else: 
            return key.split(',')
    
    # create a key from a item - set
    def createKeyFromItemset(self, itemset):
        return ",".join(itemset)
    
    # get all item-set in the hash table
    def getItemsets(self):
        itemsets = []
        for key, hash_item_collection in self.table.items():
            prefix_items = self.getItemsetFromKey(key)
            for hash_item in hash_item_collection:
                new_itemset = list(prefix_items)
                new_itemset.append(hash_item.last_item)
                itemsets.append(new_itemset)
        return itemsets
    
    # get number of item-set have same K - 1 first items.
    def getNumberOfItemsets(self, key):
        return self.table[key].size()
    
    # get frequent item-set
    def getFrequentItemsets(self, minsup):
        L = AprioriHashTable()
        for key, hash_item_collection in self.table.items():
            L.insertKey(key)
            for hash_item in hash_item_collection:
                if hash_item.size() >= minsup:
                    L.addItemset(key, hash_item)
            if L.getNumberOfItemsets(key) == 0:
                L.removeKey(key)
        return L

    def sort(self):
        for hash_item_collection in self.table.values():
            hash_item_collection.sort()