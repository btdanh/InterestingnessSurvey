from AprioriHashTable import AprioriHashTable
from AprioriHashItem import AprioriHashItem, AprioriHashItemCollection

class Apriori:
    
    def __init__(self, min_support, interest_measure):
        self.min_support = min_support
        self.interest_measure = interest_measure
        
    def generateL1(self, dataset):
        C_1 = AprioriHashTable()
        itemset_key = ''
        C_1.insertKey(itemset_key)
        
        for tid in range(dataset.size()):
            transaction = dataset.getTransaction(tid)
            for item in transaction:
                C_1.addTransaction(itemset_key, item, tid)
        L_1 = C_1.getFrequentItemsets(self.min_support)
        L_1.sort()
        return L_1        
        
    def hasInfrequentSubset(self, candidate_first_items, candidate_last_item, L_k_1, k):
        for index in range(len(candidate_first_items) - 1):
            subset = list(candidate_first_items)
            subset.pop(index)
            key = AprioriHashTable.createKeyFromItemset(subset)
            if L_k_1.notBelongTo(key, candidate_last_item):
                return True
        return False
    
   
    
    def generateCandidates(self, L_k_1, k):
        print('generate candidates with {0} items', k)
        C_k = AprioriHashTable()
        for key, hash_item_collection in L_k_1.getItems():
            for index in range(hash_item_collection.size() - 1):
                
                index_th_item = hash_item_collection.at(index)
                new_key = ''
                if key == '':
                    new_key = index_th_item.last_item
                else:
                    new_key = key +',' + index_th_item.last_item
                new_hash_collection = AprioriHashItemCollection()
                
                #check if it is infrequent item-set
                candidate = AprioriHashTable.getItemsetFromKey(new_key)
                for item in hash_item_collection.fromIndexToEnd(index + 1):
                    if not self.hasInfrequentSubset(candidate, item.last_item, L_k_1, k):
                        new_item = AprioriHashItem(item.last_item)
                        inter_items = set(index_th_item.tids).intersection(item.tids)      
                        if len(inter_items) > 0:  
                            new_item.addTransactions(list(inter_items))
                            new_hash_collection.addItem(new_item)
                        
                if new_hash_collection.size() > 0:        
                    C_k.insertKeyAndValue(new_key,  new_hash_collection)     
        return C_k

    def generateFrequentItemSets(self, dataset):
        L = []
        
        L_k_1 = self.generateL1(dataset)
        print(L_k_1)
        L.extend(L_k_1.getItemsets())
        
        k = 2
        while not L_k_1.isEmpty():
            C_k = self.generateCandidates(L_k_1, k)
            L_k_1 = C_k.getFrequentItemsets(self.min_support)
            L.extend(L_k_1.getItemsets())
            print('------------------------------')
            print(L_k_1)
            k += 1
        return L
        
        