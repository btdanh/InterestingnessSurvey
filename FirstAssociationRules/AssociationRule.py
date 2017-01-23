import ItemsetHelper
import random
import numpy
from scipy._lib.six import xrange

class AssociationRuleGenerator:
    
    def __init__(self, measures):
        self.measures = measures
       
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
        
    def generateRules(self, frequentItemsets, m = 1, k = 1):
        
        association_rules = {}
        rank_indicators = [[] for x in xrange(len(self.measures))]
        
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
                
                rule_key = left_subset_key + "=>" + right_subset_key
                association_rules[rule_key] = []
                
                for index in range(len(self.measures)):
                    value = self.measures[index](left, right, frequency, m, k)
                    association_rules[rule_key].append(value)
                    rank_indicators[index].append(value)

        final_rank_indicator = []
        for rank_list in rank_indicators:
            r = list(set(rank_list))
            r.sort(reverse=True)
            final_rank_indicator.append(r)
            
        return (association_rules, final_rank_indicator)
    
    @staticmethod
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
    
    def selectRandomRules(self, association_rules, threshold = 500):
        return random.sample(association_rules.keys(), min(threshold,len(association_rules)))
            
    
    def searchRankForValues(self, selected_keys, association_rules, rank_indicators):
        
        ranks_matrix = numpy.zeros((len(selected_keys), len(self.measures)))
        i = 0
        for rule_key in selected_keys:
            for j in range(len(self.measures)):
                rank = AssociationRuleGenerator.findRank(rank_indicators[j], association_rules[rule_key][j])
                ranks_matrix[i,j] = rank
            i += 1
        return ranks_matrix