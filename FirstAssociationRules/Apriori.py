import itertools
from AprioriHashTable import AprioriHashTable

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
            key = self.createKeyFromItemset(subset)
            if (key not in L_k_1) or (candidate_last_item not in L_k_1[key]) :
                return True
        return False
    
   
    
    def generateCandidates(self, L_k_1, k):
        print('generate candidates with {0} items', k)
        C_k = {}
        for key, bin_value in L_k_1.items():
            bin_size = len(bin_value)
            for index in range(bin_size - 1):
                new_key = ''
                if key == '':
                    new_key = bin_value[index]
                else:
                    new_key = key +',' + bin_value[index]
                new_bin_value = []
                
                #check if it is infrequent item-set
                candidate = self.getItemsetFromKey(new_key)
                for item in bin_value[index+1:bin_size]:
                    if not self.hasInfrequentSubset(candidate, item, L_k_1, k): 
                        new_bin_value.append(item)
                if len(new_bin_value) > 0:        
                    C_k[new_key] = new_bin_value     
        return C_k

    def getItemsets(self, itemset_hash):
        itemsets = []
        for key, bin_value in itemset_hash.items():
            if key == '':
                itemsets.extend(bin_value)
            else:
                prefix_items = self.getItemsetFromKey(key)
                for item in bin_value:
                    new_itemset = list(prefix_items)
                    new_itemset.append(item)
                    itemsets.append(new_itemset)
        return itemsets
                    
    def countFrequencyForItemsets(self, C_k, dataset):
        print('count for support')
        counter = {}
        prefix_itemsets = {}
        for key, bin_value in C_k.items():
            counter[key] = list(itertools.repeat(0, len(bin_value)))
            prefix_itemsets[key] = self.getItemsetFromKey(key)
            
        for transaction in dataset:
            for key, bin_value in C_k.items():
                for index in range(len(bin_value)):
                    
                    itemset = list(prefix_itemsets[key])
                    itemset.append(bin_value[index])
                    
                    if set(itemset) <= transaction:
                        counter[key][index] += 1
        return counter;

    def generateFrequentItemSets(self, dataset):
        L = []
        
        L_k_1 = self.generateL1(dataset)
        print(L_k_1)
        L.extend(self.getItemsets(L_k_1))
        
        k = 2
        while len(L_k_1) > 0:
            C_k = self.generateCandidates(L_k_1, k)
            
            counter = self.countFrequencyForItemsets(C_k, dataset)
            
            L_k_1 = {}
            print('get frequent itemsets')
            for key, bin_value in counter.items():
                key_flag = False
                for index in range(len(bin_value)):
                    if bin_value[index] >= self.min_support and key_flag == False:
                        key_flag = True
                        L_k_1[key] = []
                        L_k_1[key].append(C_k[key][index])
                    elif bin_value[index] >= self.min_support and key_flag == True:
                        L_k_1[key].append(C_k[key][index])
                        
            L.extend(self.getItemsets(L_k_1))
            print('------------------------------')
            print(L_k_1)
            k += 1
        return L
        
        