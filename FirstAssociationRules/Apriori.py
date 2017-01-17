from AprioriHashTable import AprioriHashTable
from AprioriHashItem import AprioriHashItem, AprioriHashItemCollection
from threading import Thread

class Apriori:
    
    def __init__(self, min_support, interest_measure):
        self.min_support = min_support
        self.interest_measure = interest_measure
        
        self.L_k = AprioriHashTable()
        
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
        
    @staticmethod
    def hasInfrequentSubset(candidate_first_items, candidate_last_item, L_k_1, k):
        for index in range(len(candidate_first_items) - 1):
            subset = list(candidate_first_items)
            subset.pop(index)
            key = AprioriHashTable.createKeyFromItemset(subset)
            if L_k_1.notBelongTo(key, candidate_last_item):
                return True
        return False
    
    @staticmethod
    def generateCandidates(L_k_1, k):
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
                    if not Apriori.hasInfrequentSubset(candidate, item.last_item, L_k_1, k):
                        new_item = AprioriHashItem(item.last_item)
                        inter_items = set(index_th_item.tids).intersection(item.tids)      
                        if len(inter_items) > 0:  
                            new_item.addTransactions(list(inter_items))
                            new_hash_collection.addItem(new_item)
                        
                if new_hash_collection.size() > 0:        
                    C_k.insertKeyAndValue(new_key,  new_hash_collection)     
        return C_k

    @staticmethod
    def separateToSubParts(hash_table, n):
        number_of_keys = hash_table.size()
        if number_of_keys < n:
            return [hash_table]
        
        number_for_each_part = (int)(number_of_keys/n) + 1
        counter = 0
        sub_hash_tables = []
        sub_hash_table = AprioriHashTable()
        
        for key, hash_item_collection in hash_table.getItems():
            if counter < number_for_each_part:
                sub_hash_table.insertKeyAndValue(key, hash_item_collection)
            elif counter == number_for_each_part:
                sub_hash_tables.append(sub_hash_table)
                sub_hash_table = AprioriHashTable()
                sub_hash_table.insertKeyAndValue(key, hash_item_collection)
                counter = 0
        sub_hash_tables.append(sub_hash_table)
        return sub_hash_tables
    
    @staticmethod
    def getFrequentItemSets(apriori_alg,  L_k_1, k):
        C_k = Apriori.generateCandidates(L_k_1, k)
        L_k_1 = C_k.getFrequentItemsets(apriori_alg.min_support)
        apriori_alg.L_k.merge(L_k_1)
            
    def generateFrequentItemSets(self, dataset, number_of_threads, output_file):
       
        L_k_1 = self.generateL1(dataset)
        print("extract 1 item-sets: done")
        
        k = 2
        while not L_k_1.isEmpty():
            
            print("extract {0} item-sets....", k)
            
            #divide L_k_1 into n parts
            self.L_k = AprioriHashTable()
            sub_parts = Apriori.separateToSubParts(L_k_1, number_of_threads)
            threads = []
            
            for sub_L_k_1 in sub_parts:
                thread_i = Thread(target=Apriori.getFrequentItemSets, args=(self, sub_L_k_1, k))
                threads.append(thread_i)
                thread_i.start()
            
            # wait for all thread completes
            for thread_i in threads:
                thread_i.join()
                
            L_k_1.clear()
            L_k_1 = self.L_k

            print('Write to file...')
            
            file_name = output_file + str(k) + ".txt"
            with open(file_name, "w") as text_file:
                item_sets = L_k_1.getItemsets()
                for item_set in item_sets:
                    text_file.write(','.join(item for item in item_set))
                    text_file.write('\n')
            print ("Done!!!")
            k += 1
        
        