from InterestingPatterns.ItemsetHelper import getItemsetFromKey, createKeyFromItemset
import random
import numpy

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
        
    @staticmethod    
    def distanceSubsets(first, second):
        intersect_set = set(first).intersection(set(second))
        return (len(first) + len(second) - 2 * len(intersect_set))/(len(first) + len(second) - len(intersect_set))
        
    def getItemset(self):
        itemset = []
        itemset.extend(self.left_items)
        itemset.extend(self.right_items)
        itemset.sort()
        return itemset
        
        
    def getItemsetKey(self):
        itemset = self.getItemset()
        return createKeyFromItemset(itemset)
        
    def distance(self, another, theta_params):
        left_distance = AssociationRule.distanceSubsets(self.left_items, another.left_items)
        right_distance = AssociationRule.distanceSubsets(self.right_items, another.right_items)
        both_distance = AssociationRule.distanceSubsets(self.getItemset(), another.getItemset())
        return theta_params[0] * both_distance + theta_params[1] * left_distance + theta_params[2] * right_distance
        
        
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
            sub_lists.append((left, right))
        
        self.generateSubsets(bits, item_set, k+1, sub_lists)
        bits[k] = False
        
    def generateRules(self, frequentItemsets):
        
        association_rules = []
        
        for itemset_key in frequentItemsets.keys():
            itemset = getItemsetFromKey(itemset_key)
            if len(itemset) == 1:
                continue
            sub_lists = []
            bits = [False] * len(itemset)
            self.generateSubsets(bits, itemset, 0, sub_lists)
            for subset_pair in sub_lists:
                rule = AssociationRule(subset_pair[0], subset_pair[1])
                association_rules.append(rule)
                
        return association_rules
      
    def computeInterestingness(self, association_rules, frequent_itemsets, total, m = 1, k = 1):
        
        rank_collectors = [[] for x in range(len(self.measures))]
        for rule_key, rule in association_rules.items():
            left = frequent_itemsets[rule.getLeftKey()]
            right = frequent_itemsets[rule.getRightKey()]
            both = frequent_itemsets[rule.getItemsetKey()]
            
            for index in range(len(self.measures)):
                value = self.measures[index](left, right, both, total)
                association_rules[rule_key].appendScore(value)
                rank_collectors[index].append(value)

        rank_indicators = []
        for rank_list in rank_collectors:
            r = list(set(rank_list))
            r.sort(reverse=True)
            rank_indicators.append(r)

        return rank_indicators
        
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
    
    @staticmethod
    def selectRandomRules(association_rules, threshold = 500):
        return random.sample(association_rules.keys(), min(threshold,len(association_rules)))
            
    
    def searchRankForValues(self, selected_keys, association_rules, rank_indicators):
        
        ranks_matrix = numpy.zeros((len(selected_keys), len(self.measures)))
        i = 0
        for rule_key in selected_keys:
            for j in range(len(self.measures)):
                value = association_rules[rule_key].scores[j]
                rank = AssociationRuleGenerator.findRank(rank_indicators[j], value)
                ranks_matrix[i,j] = rank
            i += 1
        return ranks_matrix
    
    
            
            