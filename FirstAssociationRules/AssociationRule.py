import ItemsetHelper
import random

class AssociationRuleGenerator:
    
    def __init__(self, interestingness):
        self.measure = interestingness
       
    def generateSubsets(self, bits, item_set, k, sub_lists): 
        if k >= len(item_set):
            return 
        bits[k] = False
        self.generateSubsets(bits, item_set, k+1, sub_lists)
        
        bits[k] = True
        left = []
        right = []
        for index in range(len(bits)):
            if bits[index] == True:
                left.append(item_set[index])
            else:
                right.append(item_set[index])
        if (len(left) > 0 and len(right) > 0):
            sub_lists.append((ItemsetHelper.createKeyFromItemset(left), ItemsetHelper.createKeyFromItemset(right)))
        
        self.generateSubsets(bits, item_set, k+1, sub_lists)
        bits[k] = False
        
    # just keep number_of_rules best rules in mining process.
    def generateRules(self, frequentItemsets, selected_rules_dict = None, m = 1, k = 1):
        
        association_rules = []
        ranks = []
        
        for itemset_key, frequency in frequentItemsets.items():
            itemset = ItemsetHelper.getItemsetFromKey(itemset_key)
            if len(itemset) == 1:
                continue
            sub_lists = []
            bits = [False] * len(itemset)
            self.generateSubsets(bits, itemset, 0, sub_lists)
            for element in sub_lists:
                left_subset_key = element[0]
                left = frequentItemsets[left_subset_key]
                
                right_subset_key = element[1]
                right = frequentItemsets[right_subset_key]
                
                value = self.measure(left, right, frequency, m, k)
                ranks.append(value)
                
                rule = (value, left_subset_key, right_subset_key)
                rule_key = left_subset_key + "=>" + right_subset_key
                if selected_rules_dict == None or (rule_key in selected_rules_dict):
                    association_rules.append(rule)
        ranks = list(set(ranks))
        ranks.sort(reverse=True)
        return (association_rules, ranks)
    
    @staticmethod
    def findRank(item_list, element):
        left = 0
        right = len(item_list) - 1
        
        while left <= right:
            pivot = int((left + right)/2)
            if element == item_list[pivot]:
                return pivot
            elif element < item_list[pivot]:
                left = pivot + 1
            else:
                right = pivot -1
        return -1
    
    def selectEvaluatedRules(self, rules_and_ranks, threshold = 500):
        rules = rules_and_ranks[0]
        selected_rules = random.sample(rules, threshold)
        
        selected_rules_dict = {}
        for r in selected_rules:
            rule_key = r[1] + "=>" +r[2]
            selected_rules_dict[rule_key] = r
        return selected_rules_dict
        
    
    def searchRankForValues(self, selected_rules, ranks):
        rule_ranks = []
        for rule in selected_rules:
            rule_ranks.append((AssociationRuleGenerator.findRank(ranks, rule[0]), rule[0], rule[1], rule[2]))
        return rule_ranks
    
        