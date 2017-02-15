from multiprocessing import Process
from multiprocessing.managers import BaseManager

from InterestingPatterns.AprioriHashTable import AprioriHashTable
from InterestingPatterns.AprioriHashItem import AprioriHashItem
from InterestingPatterns.AprioriHashItemCollection import AprioriHashItemCollection

def generateL1(min_support, dataset):
    C_1 = AprioriHashTable()
    itemset_key = ''
    C_1.insertKey(itemset_key)
    
    n = dataset.size()
    print ('size of dataset: ' + str(n))
    for tid in range(n):
        transaction = dataset.getTransaction(tid)
        for item in transaction:
            C_1.addTransaction(itemset_key, item, tid)
            
    print ('get frequent item sets with 1 item')
    L_1 = C_1.getFrequentItemsets(min_support)
    return L_1        

def generateFrequentItemsetsWithKItems(min_support, L_k_1, k, C_k):
    print('generate candidates with {0} items', k)
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
                if len(inter_items) >= min_support:  
                    new_item.addTransactions(list(inter_items))
                    new_hash_collection.addItem(new_item)
                    
            if new_hash_collection.size() > 0:        
                C_k.insertKeyAndValue(new_key,  new_hash_collection)     

def runForFrequentItemsetsWithKItems(L_k_1, k, min_support, C_k):
    generateFrequentItemsetsWithKItems(min_support, L_k_1, k, C_k)
        
def insertHashIntoDictionary(L_k_1, L):
    item_sets = L_k_1.getItemsets()
    for key, value in item_sets.items():
        L[key] = value
            
def generateFrequentItemSets(min_support, number_of_threads, start_k, end_k, old_L_k_1):
    L = {}
    k = start_k
    L_k_1 = old_L_k_1
    
    while not L_k_1.isEmpty() and k <= end_k:
        
        print('extracting item-sets with ' + str(k) + ' items ....')
        
        #divide L_k_1 into n parts
        L_k = AprioriHashTable()
        sub_parts = L_k_1.separateToSubParts(number_of_threads)
        processes = []
        
        C_ks = []
        BaseManager.register("AprioriHash", AprioriHashTable)
        manager = BaseManager()
        manager.start()
        C_ks.append(manager.AprioriHash())
        
        index = 0
        for sub_L_k_1 in sub_parts:
            process_i = Process(target = runForFrequentItemsetsWithKItems, args=(sub_L_k_1, k, min_support, C_ks[index]))
            processes.append(process_i)
        
        # wait for all thread completes
        for process_i in processes:
            process_i.start()
            process_i.join()
         
        for new_C_k in C_ks:
            L_k.merge(new_C_k)
        L_k_1.clear()
        L_k_1 = L_k

        insertHashIntoDictionary(L_k_1, L)
        k += 1
    print ('stop at k = ' + str(k))
    return L_k_1, L
        
        
        