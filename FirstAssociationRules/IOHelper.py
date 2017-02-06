
from InterestingPatterns.ItemsetHelper import getItemsetFromKey
from InterestingPatterns.AssociationRuleGenerator import AssociationRule

def writeTransactionDB(file_name, data):
    with open(file_name, "w") as text_file:
        for transaction in data:
            text_file.write(transaction)
            text_file.write('\n')
            
def readTransactionDBFileFrom(inputfile, n):
    data = []
    with open(inputfile, "r") as text_in_file:
        k = 1
        for line in text_in_file:
            if k > n:
                data.append(line.strip())
            k += 1
    return data

def appendFrequentItemsetsToFile(file_name, itemsets, data_size):
    with open(file_name, "a") as text_file:
        if (data_size  is not None):
            text_file.write(str(data_size))
            text_file.write('\n')
        for key, value in itemsets.items():
            text_file.write(key + ':' + str(value))
            text_file.write('\n')
            
def readFrequentItemsets(file_name):
    dataset_size = 0
    frequent_itemsets = {}
    with open(file_name, "r") as text_file:
        dataset_size = int(text_file.readline())
        for line in text_file:
            subStrings = line.split(':')
            itemset_key = subStrings[0].strip()
            frequency = int(subStrings[1].strip())
            
            frequent_itemsets[itemset_key] = frequency
    return (dataset_size, frequent_itemsets)

def appendAssociationRulesToFile(file_name, association_rules):
    with open(file_name, "a") as text_file:
        for subset in association_rules:
            for rule in subset:
                text_file.write(rule.getRuleKey())
                text_file.write('\n')

def readAssociationRules(file_name):
    association_rules = {}
    with open(file_name, "r") as text_file:
        for line in text_file:
            subStrings = line.split(">")
            left = getItemsetFromKey(subStrings[0].strip())
            right = getItemsetFromKey(subStrings[1].strip())
            rule = AssociationRule(left, right)
            association_rules[rule.getRuleKey()] = rule
    return association_rules
            
def writeInterestingness(file_name, selected_keys, association_rules):
    with open(file_name, "w") as text_file:
        for rule in selected_keys:
            text_file.write(rule)
            text_file.write(';')
            text_file.write(';'.join(map(str, association_rules[rule].scores)))
            text_file.write('\n') 

            
def writeClustersOfRules(file_name, association_rules, labels):
    combined_list = list(zip(association_rules, labels))
    combined_list.sort(key= lambda tup: tup[1])
    
    with open(file_name, "w") as text_file:
        for rule, label in combined_list:
            text_file.write(str(label))
            text_file.write(':')
            text_file.write(rule)
            text_file.write('\n')
        
def writeCorrelationMatrix(file_name, matrix):
    with open(file_name, "w") as text_file:
        for line in matrix:
            text_file.write(','.join(str(x) for x in line.tolist()))
            text_file.write('\n')
    
def readRulesClusters(file_name):
    association_rules = {}
    with open(file_name, "r") as text_file:
        for line in text_file:
            subStrings = line.split(":")
            label = subStrings[0].strip()
            rule_key = subStrings[1].strip()
            if label not in association_rules:
                association_rules[label] = []
            association_rules[label].append(rule_key)
    return association_rules

def writeRulesForAnnotation(file_name, association_rules):
    with open(file_name, "w") as text_file:
        for rule in association_rules:
            text_file.write(rule)
            text_file.write(':')
            text_file.write('u')
            text_file.write('\n')