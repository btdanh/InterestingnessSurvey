import json
import numpy

from InterestingPatterns.ItemsetHelper import getItemsetFromKey
from InterestingPatterns.AssociationRuleGenerator import AssociationRule

def removeFirstLinesFromFiles(inputfile, outputfile, n):
    with open(inputfile, "r") as text_in_file:
        with open(outputfile, "w") as text_out_file:
            k = 1
            for line in text_in_file:
                if k > n: 
                    text_out_file.write(line)
                    text_out_file.write('\n')
                k += 1
                
def writeFrequentItemsets(file_name, itemsets, data_size):
    with open(file_name, "w") as text_file:
        json.dump((data_size, itemsets), text_file)
            
def readFrequentItemsets(file_name):
    with open(file_name, "r") as text_file:
        itemsets = json.load(text_file)
    return itemsets

def writeAssociationRules(file_name, association_rules):
    with open(file_name, "w") as text_file:
        for rule in association_rules:
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