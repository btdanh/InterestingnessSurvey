from threading import Thread
from InterestingPatterns.AprioriHashTable import AprioriHashTable
from InterestingPatterns.AprioriHashItem import AprioriHashItem
from InterestingPatterns.AprioriHashItemCollection import AprioriHashItemCollection

class Apriori:
    
    def __init__(self, min_support):
        self.min_support = min_support
        self.L_k = AprioriHashTable()
        
    def generateL1(self, dataset):
        C_1 = AprioriHashTable()
        itemset_key = ''
        C_1.insertKey(itemset_key)
        
        n = dataset.size()
        print ('size of dataset: ' + str(n))
        for tid in range(n):
            transaction = dataset.getTransaction(tid)
            for item in transaction:
                C_1.addTransaction(itemset_key, item, tid)
            if tid % 5000 == 0: 
                print (str(tid))
                
        print ('get frequent item sets with 1 item')
        L_1 = C_1.getFrequentItemsets(self.min_support)
        print ('Sort the itemsets')
        #L_1.sort()
        print ('Done sort!')
        return L_1        

    def generateFrequentItemsetsWithKItems(self, L_k_1, k):
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
                for item in hash_item_collection.fromIndexToEnd(index + 1):
                    new_item = AprioriHashItem(item.last_item)
                    inter_items = set(index_th_item.tids).intersection(item.tids)      
                    if len(inter_items) >= self.min_support:  
                        new_item.addTransactions(list(inter_items))
                        new_hash_collection.addItem(new_item)
                        
                if new_hash_collection.size() > 0:        
                    C_k.insertKeyAndValue(new_key,  new_hash_collection)     
        return C_k

    @staticmethod
    def runForFrequentItemsetsWithKItems(apriori_alg,  L_k_1, k):
        C_k = apriori_alg.generateFrequentItemsetsWithKItems(L_k_1, k)
        apriori_alg.L_k.merge(C_k)
            
    def generateFrequentItemSets(self, dataset, number_of_threads):
        L_k_1 = self.generateL1(dataset)
        L = L_k_1.getItemsets()
        
        print("extract 1 item-sets: done")
        
        k = 2
        while not L_k_1.isEmpty():
            
            print('extracting item-sets with ' + str(k) + ' items ....')
            
            #divide L_k_1 into n parts
            self.L_k = AprioriHashTable()
            sub_parts = L_k_1.separateToSubParts(number_of_threads)
            threads = []
            
            for sub_L_k_1 in sub_parts:
                thread_i = Thread(target=Apriori.runForFrequentItemsetsWithKItems, args=(self, sub_L_k_1, k))
                threads.append(thread_i)
                thread_i.start()
            
            # wait for all thread completes
            for thread_i in threads:
                thread_i.join()
                
            L_k_1.clear()
            L_k_1 = self.L_k

            item_sets = L_k_1.getItemsets()
            for key, value in item_sets.items():
                L[key] = value
            k += 1
        return L
        
        