from InterestingPatterns.ItemsetHelper import getItemsetFromKey, createKeyFromItemset
import random
import numpy
from multiprocessing import Process
from multiprocessing import Manager


def massSpectrumFilter(rule):
    return rule.getLeftKey().isdigit() and (not rule.getRightKey().isdigit())

class AssociationRule:
    def __init__(self, left, right):
        self.left_items = left
        self.right_items = right
        self.scores = []
        
    def firstScore(self):
        return self.scores[0]
        
    def getRuleKey(self):
        left_key = self.getLeftKey()
        right_key = self.getRightKey()
        return left_key + ">" + right_key
    
    def getLeftKey(self):
        return createKeyFromItemset(self.left_items)
        
    def getRightKey(self):
        return createKeyFromItemset(self.right_items)
    
    def appendScore(self, score):
        self.scores.append(score)
        
    def getItemset(self):
        itemset = []
        itemset.extend(self.left_items)
        itemset.extend(self.right_items)
        itemset.sort()
        return itemset
        
        
    def getItemsetKey(self):
        itemset = self.getItemset()
        return createKeyFromItemset(itemset)
        
     
def generateSubsets(bits, item_set, k, sub_lists): 
    if k >= len(item_set):
        return 
    bits[k] = False
    generateSubsets(bits, item_set, k+1, sub_lists)
    
    bits[k] = True
    left = []
    right = []
    for index in range(len(bits)):
        if bits[index] == True:
            left.append(item_set[index])
        else:
            right.append(item_set[index])
    if (len(left) > 0 and len(right) > 0):
        sub_lists.append((left, right))
    
    generateSubsets(bits, item_set, k+1, sub_lists)
    bits[k] = False
    
def runForRulesFromItemsets(frequent_itemsets, rules, rule_filter):
    k = 0
    for itemset in frequent_itemsets:
        k += 1
        if k % 500 == 0:
            print ('working on the itemset: ' + str(k))
        if len(itemset) == 1:
            continue
        sub_lists = []
        bits = [False] * len(itemset)
        generateSubsets(bits, itemset, 0, sub_lists)
        for subset_pair in sub_lists:
            rule = AssociationRule(subset_pair[0], subset_pair[1])
            if rule_filter == None or rule_filter(rule) == True:
                rules.append(rule)
    print ('Done for o sub frequent itemsets!!!')
                
def getItemsetsWithSpecificLength(frequent_itemsets_keys, from_len, to_len):
    selected_itemsets = []
    for itemset_key in frequent_itemsets_keys:
        itemset = getItemsetFromKey(itemset_key)
        if len(itemset) >= from_len and len(itemset) <= to_len:
            selected_itemsets.append(itemset)
    return selected_itemsets
            
def generateRules(frequent_itemsets, number_of_threads, rule_filter, from_len, to_len):
    selected_itemsets = getItemsetsWithSpecificLength(frequent_itemsets.keys(), from_len, to_len)
     
    number_of_itemsets = len(selected_itemsets)
    print ('Number of frequent itemsets: ' + str(number_of_itemsets))
    if number_of_itemsets < number_of_threads:
        association_rules = []
        runForRulesFromItemsets(selected_itemsets, association_rules, rule_filter)
        return [association_rules]
    else:
        sub_itemsets = [[] for x in range(number_of_threads)]
        
        number_for_each_part = (int)(number_of_itemsets/number_of_threads) + 1
                    
        index = 0
        counter = 0
        
        for itemset in selected_itemsets:
            if counter < number_for_each_part:
                sub_itemsets[index].append(itemset)
                counter += 1
            elif counter == number_for_each_part:
                index += 1
                sub_itemsets[index].append(itemset)
                counter = 1
                
        sub_rules = []
        manager = Manager()
        for i in range(number_of_threads):
            sub_rules.append(manager.list([]))
        
        processes = []
        for index in range(number_of_threads):
            process_i = Process(target=runForRulesFromItemsets, args=(sub_itemsets[index], sub_rules[index], rule_filter))
            processes.append(process_i)
            
            
        for process_i in processes:
            process_i.start()
            
        # wait for all thread completes
        for process_i in processes:
            process_i.join()
            
        '''for index in range(number_of_threads):
            association_rules.extend(sub_rules[index])
        '''
        print ('go here!!!!')    
    return sub_rules
  
def computeInterestingness(measures, association_rules, frequent_itemsets, total, m = 1, k = 1):
    
    rank_collectors = [[] for x in range(len(measures))]
    for rule_key, rule in association_rules.items():
        left = frequent_itemsets[rule.getLeftKey()]
        right = frequent_itemsets[rule.getRightKey()]
        both = frequent_itemsets[rule.getItemsetKey()]
        
        for index in range(len(measures)):
            value = measures[index](left, right, both, total)
            association_rules[rule_key].appendScore(value)
            rank_collectors[index].append(value)

    rank_indicators = []
    for rank_list in rank_collectors:
        r = list(set(rank_list))
        r.sort(reverse=True)
        rank_indicators.append(r)

    return rank_indicators
    
def findRank(item_list, element):
    left = 0
    right = len(item_list) - 1
    
    while left <= right:
        pivot = int((left + right)/2)
        if element == item_list[pivot]:
            return pivot + 1
        elif element < item_list[pivot]:
            left = pivot + 1
        else:
            right = pivot -1
    return -1

def selectRandomRules(association_rules, threshold = None):
    if threshold == None:
        return association_rules.keys()
    return random.sample(association_rules.keys(), min(threshold,len(association_rules)))
        

def searchRankForValues(measures, selected_keys, association_rules, rank_indicators):
    
    ranks_matrix = numpy.zeros((len(selected_keys), len(measures)))
    i = 0
    for rule_key in selected_keys:
        for j in range(len(measures)):
            value = association_rules[rule_key].scores[j]
            rank = findRank(rank_indicators[j], value)
            ranks_matrix[i,j] = rank
        i += 1
    return ranks_matrix
    
            
            