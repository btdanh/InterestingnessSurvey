'''
Created on Jan 26, 2017

@author: BanhDzui
'''
import numpy as np
import random

from sklearn.cluster.dbscan_ import DBSCAN
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from math import sqrt
from InterestingPatterns.AssociationRuleGenerator import AssociationRule

class My2DArray:
    def __init__(self, n, m):
        self.matrix = np.zeros((n, m))
        
    def getMatrix(self):
        return self.matrix
    
    def insertValue(self, i, j, value):
        self.matrix[i,j] = value

def longestCommonString(str1, str2):
    longest = 0
    n = len(str1)
    m = len(str2)

    for i in range(n):
        for j in range(m):
            if not (str1[i] == str2[j]): continue
            
            k = 0
            while (k + i < n and k + j < m):
                if (not (str1[k+i] == str2[k + j])): break
                k += 1
            if k > longest: longest = k
    return longest

def distanceInStructure(first, second):
    summary = 0
    for i in range(len(first)):
        for j in range(len(second)):
            longest = longestCommonString(first[i], second[j])
            
            x = (len(first[i]) + len(second[j]) - 2 * longest)
            y = (len(first[i]) + len(second[j]) - longest)
            summary += x/y
    return summary

def distanceSubsets(first, second):
    intersect_set = set(first).intersection(set(second))
    return (len(first) + len(second) - 2 * len(intersect_set))/(len(first) + len(second) - len(intersect_set))

def generalDistance(vector1, vector2):
    item_set_1 = []
    item_set_1.extend(vector1[0])
    item_set_1.extend(vector1[1])

    item_set_2 = []
    item_set_2.extend(vector2[0])
    item_set_2.extend(vector2[1])
    d = 0
 
    left_diff = distanceSubsets(vector1[0], vector2[0])
    d += (left_diff ** 2)
    right_diff = distanceSubsets(vector1[1], vector2[1])
    d += (right_diff ** 2)
    
    both_diff = distanceSubsets(item_set_1, item_set_2)
    d += (both_diff ** 2)
    return d
    
    
def detailDistance(vector1, vector2):
    d = 0
 
    left_diff = distanceSubsets(vector1[0], vector2[0])
    d += (left_diff ** 2)
    right_diff = distanceInStructure(vector1[1], vector2[1])
    d += (right_diff ** 2)
    return d

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
        
def runToComputeDistances(rule_vectors, distance_function, my_matrix, start, end):
    min_distance = -1
    max_distance = -1
    for i in range(start,  end):
        if i % 1000 == 0: 
            print (str(i))
        for j in range(0, i):
            
            d = 0
            for k in range(2, len(rule_vectors[i])):
                d += (rule_vectors[i][k] - rule_vectors[j][k]) ** 2
            if not (distance_function == None): 
                d += distance_function(rule_vectors[i], rule_vectors[j])
            
            d = sqrt(d)
            my_matrix.insertValue(i,j, d)
            my_matrix.insertValue(j, i, d)
            if min_distance == -1 or min_distance > d:
                min_distance = d
            if max_distance == -1 or max_distance < d:
                max_distance = d
    
                
    print ('min distance: ' + str(min_distance))
    print ('max distance: ' + str(max_distance))
            

def computeDistances(rule_vectors, number_of_threads, distance_function = None):
    number_of_rule = len(rule_vectors)
    
    ''' 
    Run in the case just need one thread
    '''
    if number_of_threads == 1:
        my_matrix = My2DArray(number_of_rule, number_of_rule)
        runToComputeDistances(rule_vectors, distance_function, my_matrix, 0, number_of_rule)
        return my_matrix.getMatrix()
    
    ''' 
    Run in the case just need more than one thread
    '''
    number_for_part = (int)(number_of_rule / number_of_threads) + 1
    
    start = 0
    sub_ranges = []
    for i in range(number_of_threads):
        end = min(start + number_for_part, number_of_rule)
        sub_ranges.append((start, end))
        start = end
    BaseManager.register('My2DArray', My2DArray)
    manager = BaseManager()
    manager.start()
    my_matrix = manager.My2DArray(number_of_rule, number_of_rule)
        
    processes = []
    for value_pair in sub_ranges:
        process_i = Process(target = runToComputeDistances, args = (rule_vectors, distance_function, my_matrix, value_pair[0], value_pair[1]))
        process_i.start()
        processes.append(process_i)
        
    for process_i in processes:
        process_i.join()
        
    return my_matrix.getMatrix()
                
def runDBSCAN(distance_matrix, my_eps, my_min_samples):
    db = DBSCAN(eps = my_eps, min_samples=my_min_samples)
    db.fit(distance_matrix)
    
    labels = db.labels_
    n_clusters = len(set(labels))- (1 if -1 in labels else 0)
    n_noises = list(labels).count(-1)
    
    print('Number of clusters' + str(n_clusters))
    print('Number of noises' + str(n_noises))

    return list(labels)

def selectCandidateFromClusters(clusters_and_rules, for_cluster, for_noises):
    selected_rules = []
    for cluster_label, rules in clusters_and_rules.items():
        if cluster_label == '-1':
            count = for_noises * len(rules)
            selected_rules.extend(random.sample(rules, count))
        else:
            selected_rules.extend(random.sample(rules, for_cluster))
    return selected_rules
                