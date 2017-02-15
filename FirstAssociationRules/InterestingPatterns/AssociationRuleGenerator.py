from InterestingPatterns.ItemsetHelper import createKeyFromItemset,\
    getItemsetFromKey
import random
from multiprocessing import Process


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

def appendAssociationRulesToFile(file_name, association_rules):
    with open(file_name, "a") as text_file:
        for rule in association_rules:
            text_file.write(rule.getRuleKey())
            text_file.write('\n')
            
def runForRulesFromItemsets(frequent_itemsets, rule_filter, output_file):
    k = 0
    rules = []
    for itemset in frequent_itemsets:
        k += 1
        if k % 250 == 0:
            print ('writing some rules to file: ' + str(k))
            appendAssociationRulesToFile(output_file, rules)
            rules.clear()
            
        if len(itemset) == 1:
            continue
        sub_lists = []
        bits = [False] * len(itemset)
        generateSubsets(bits, itemset, 0, sub_lists)
        for subset_pair in sub_lists:
            rule = AssociationRule(subset_pair[0], subset_pair[1])
            if rule_filter == None or rule_filter(rule) == True:
                rules.append(rule)
    print ('writing last rules to file: ' + str(k))
    appendAssociationRulesToFile(output_file, rules)
    rules.clear()
    print ('Done for o sub frequent itemsets!!!')
                
            
def generateRules(frequent_itemsets, number_of_threads, rule_filter, output_file):
    selected_itemsets = frequent_itemsets.keys()
     
    number_of_itemsets = len(selected_itemsets)
    print ('Number of frequent itemsets: ' + str(number_of_itemsets))
    sub_itemsets = [[] for x in range(number_of_threads)]
        
    number_for_each_part = (int)(number_of_itemsets/number_of_threads) + 1
                
    index = 0
    counter = 0
    
    for itemset_key in selected_itemsets:
        if counter < number_for_each_part:
            sub_itemsets[index].append(getItemsetFromKey(itemset_key))
            counter += 1
        elif counter == number_for_each_part:
            index += 1
            sub_itemsets[index].append(getItemsetFromKey(itemset_key))
            counter = 1
         
    processes = []
    for index in range(number_of_threads):
        file_name = str(index) + output_file
        print('file name: ' + file_name)
        process_i = Process(target=runForRulesFromItemsets, args=(sub_itemsets[index], rule_filter, file_name))
        processes.append(process_i)
        
        
    for process_i in processes:
        process_i.start()
        
    # wait for all thread completes
    for process_i in processes:
        process_i.join()
        
    print ('go here!!!!')    
    


def selectRandomRules(rule_file_suffix, number_of_files, sampling_rate):
    
    selected_rules = []
    i = 0
    j = 0
    for k in range(number_of_files):
        file_name = str(k) + rule_file_suffix
        with open(file_name, "r") as text_file:
            for line in text_file:
                r = random.uniform(0, 1)
                if r <= sampling_rate: 
                    selected_rules.append(line.strip())
                    j += 1
                    if j % 10000 == 0: print('selected ' + str(j) + ' patterns')
                i += 1
    print (str(i))
    return selected_rules    

    
            
            