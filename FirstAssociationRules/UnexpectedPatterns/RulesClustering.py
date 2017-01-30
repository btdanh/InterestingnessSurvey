'''
Created on Jan 26, 2017

@author: BanhDzui
'''
import numpy as np
from InterestingPatterns.AssociationRuleGenerator import AssociationRule
from sklearn.cluster.dbscan_ import DBSCAN

from math import sqrt

def generateRuleVector(selected_keys, association_rules, frequent_itemsets, number_of_transactions):
    association_vectors = []
    
    for rule_key in selected_keys:
        rule = association_rules[rule_key]
        
        vector = []
        vector.append(rule.left_items)
        vector.append(rule.right_items)
        
        left = frequent_itemsets[rule.getLeftKey()]
        right = frequent_itemsets[rule.getRightKey()]
        
        both = frequent_itemsets[rule.getItemsetKey()]
        
        ''' P(A)'''
        p_A = left/number_of_transactions
        vector.append(p_A)
        
        ''' P(B)'''
        p_B = right/number_of_transactions
        vector.append(p_B)
        
        ''' P(~A)'''
        p_not_A = 1 - p_A
        vector.append(p_not_A)
        
        ''' P(~B)'''
        p_not_B = 1 - p_B
        vector.append(p_not_B)
        
        ''' P(AB) '''
        p_A_and_B = both/number_of_transactions
        vector.append(p_A_and_B)
        
        ''' P(~AB)'''
        p_not_A_and_B = (right - both)/number_of_transactions
        vector.append(p_not_A_and_B)
        
        ''' P(A~B)'''
        p_A_and_not_B = (left - both)/number_of_transactions
        vector.append(p_A_and_not_B)
        
        ''' P(~A~B)'''
        p_not_A_and_not_B = 1 - (left + right - both)/number_of_transactions
        vector.append(p_not_A_and_not_B)
        
        association_vectors.append(vector)
        
    return association_vectors
        
def computeDistances(rule_vectors):
    number_of_rule = len(rule_vectors)
    distance_matrix = np.zeros((number_of_rule, number_of_rule))
    
    print ('Number of rules:' + str(number_of_rule))
    min_distance = -1
    max_distance = -1
    for i in range(number_of_rule):
        if (i % 1000) == 0:
            print (str(i))
        item_set_1 = []
        item_set_1.extend(rule_vectors[i][0])
        item_set_1.extend(rule_vectors[i][1])
        for j in range(0, i):
            
            item_set_2 = []
            item_set_2.extend(rule_vectors[j][0])
            item_set_2.extend(rule_vectors[j][1])
            
            d = 0
            for k in range(2, len(rule_vectors[i])):
                d += (rule_vectors[i][k] - rule_vectors[j][k]) ** 2
            left_diff = AssociationRule.distanceSubsets(rule_vectors[i][0], rule_vectors[j][0])
            d += (left_diff ** 2)
            right_diff = AssociationRule.distanceSubsets(rule_vectors[i][1], rule_vectors[j][1])
            d += (right_diff ** 2)
            
            both_diff = AssociationRule.distanceSubsets(item_set_1, item_set_2)
            d += (both_diff ** 2)
            
            d = sqrt(d)
            distance_matrix[i, j] = d
            distance_matrix[j, i] = d
            
            if min_distance == -1 or min_distance > d:
                min_distance = d
            if max_distance == -1 or max_distance < d:
                max_distance = d
    print ('Max distance :' + str(max_distance))
    print ('Min distance :' + str(min_distance))
    return distance_matrix
                
def runDBSCAN(distance_matrix, my_eps, my_min_samples):
    db = DBSCAN(eps = my_eps, min_samples=my_min_samples)
    db.fit(distance_matrix)
    
    labels = db.labels_
    n_clusters = len(set(labels))- (1 if -1 in labels else 0)
    n_noises = list(labels).count(-1)
    
    print('Number of clusters' + str(n_clusters))
    print('Number of noises' + str(n_noises))

    return list(labels)
                