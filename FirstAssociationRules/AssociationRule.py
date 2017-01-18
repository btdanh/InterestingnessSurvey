import ItemsetHelper

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
    def generateRules(self, frequentItemsets, number_of_rules, m = 1, k = 1):
        
        best_rules = []
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
                index = len(best_rules)-1
                while index >= 0:
                    if value <= best_rules[index][0]:
                        best_rules.insert(index+1, (value, left_subset_key, right_subset_key))
                        break
                    else:
                        index -= 1
                if index < 0:
                    best_rules.insert(0, (value, left_subset_key, right_subset_key))
                if len(best_rules) > number_of_rules:
                    best_rules.pop()
        return best_rules
            