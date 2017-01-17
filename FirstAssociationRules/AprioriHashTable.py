from AprioriHashItem import AprioriHashItemCollection
from threading import Lock

class AprioriHashTable:
    def __init__(self):
        self.table = {}
        self.table_write_lock = Lock()
        
    def size(self):
        return len(self.table)
    
    def isEmpty(self):
        return len(self.table) == 0;
    
    def notBelongTo(self, key, last_item):
        return (key not in self.table) or (not self.table[key].belongTo(last_item))
    
    def getItems(self):
        return self.table.items()
    
    # insert a new key into the table
    def insertKey(self, key):
        self.table[key] = AprioriHashItemCollection()
    
    def insertKeyAndValue(self, key, value):
        self.table[key] = value
            
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
    @staticmethod
    def getItemsetFromKey(key):
        if key == '':
            return []
        else: 
            return key.split(',')
    
    # create a key from a item - set
    @staticmethod
    def createKeyFromItemset(itemset):
        return ",".join(itemset)
    
    # get all item-set in the hash table
    def getItemsets(self):
        itemsets = []
        for key, hash_item_collection in self.table.items():
            prefix_items = AprioriHashTable.getItemsetFromKey(key)
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

    # this function is used for multi-thread
    def merge(self, other_hash_table):
        with self.table_write_lock:
            for key, hash_item_collection in other_hash_table.getItems():
                self.table[key] = hash_item_collection
    
    def clear(self):
        self.table.clear()