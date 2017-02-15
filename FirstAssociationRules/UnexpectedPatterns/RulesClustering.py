'''
Created on Jan 26, 2017

@author: BanhDzui
'''
import numpy as np
import random

from sklearn.cluster.dbscan_ import DBSCAN
from sklearn.metrics.pairwise import pairwise_distances

from math import sqrt
from numpy import histogram
from sklearn.cluster.k_means_ import KMeans
from difflib import SequenceMatcher

def computeDetailDistance(first, second):
    summary = 0
    
    for i in range(len(first)):
        for j in range(len(second)):
            s = SequenceMatcher(None, first[0], second[0])
            result = s.find_longest_match(0, len(first[0]), 0, len(second[0]))
        
            x = (len(first[i]) + len(second[j]) - 2 * result.size)
            y = (len(first[i]) + len(second[j]) - result.size)
            
            summary += x/y
    return summary

def computeGeneralDistance(first, second):
    
    intersect_set = set(first).intersection(set(second))
    x = len(first) + len(second) - 2 * len(intersect_set)
    y = len(first) + len(second) - len(intersect_set)
    return x / y
    
def computeFormDistance1(vector1, vector2):
    item_set_1 = []
    item_set_1.extend(vector1[0])
    item_set_1.extend(vector1[1])

    item_set_2 = []
    item_set_2.extend(vector2[0])
    item_set_2.extend(vector2[1])
    d = 0
 
    left_diff = computeGeneralDistance(vector1[0], vector2[0])
    d += (left_diff ** 2)
    right_diff = computeGeneralDistance(vector1[1], vector2[1])
    d += (right_diff ** 2)
    
    both_diff = computeGeneralDistance(item_set_1, item_set_2)
    d += (both_diff ** 2)
    return sqrt(d)
    
    
def computeFormDistance2(vector1, vector2):
    d = 0
 
    left_diff = computeGeneralDistance(vector1[0], vector2[0])
    d += (left_diff ** 2)
    right_diff = computeDetailDistance(vector1[1], vector2[1])
    d += (right_diff ** 2)
    return sqrt(d)

def generateFormVectors(selected_keys, association_rules):
    form_vectors = []
    for rule_key in selected_keys:
        rule = association_rules[rule_key]
        
        vector = []
        vector.append(rule.left_items)
        vector.append(rule.right_items)
        
        form_vectors.append(vector)
    return form_vectors
        
def generateNumericVectors(selected_keys, association_rules, frequent_itemsets, number_of_transactions):
    numeric_vectors = []
    
    for rule_key in selected_keys:
        rule = association_rules[rule_key]
        
        vector = []
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
        numeric_vectors.append(vector)
        
    return np.array(numeric_vectors)
        
def computePairwiseFormDistance(form_vectors, distance_func):
    n = len(form_vectors)
    distance = np.zeros((n, n))
    for i in range(n):
        if i % 500 == 0: print (str(i))
        for j in range(i + 1, n):
            d = distance_func(form_vectors[i], form_vectors[j])
            distance[i, j] = d
            distance[j, i] = d
    return distance
    
def computeDistanceMatrix(numeric_vectors, form_vectors, distance_func, number_of_threads):
    matrix_1 = pairwise_distances(X = numeric_vectors, metric = 'euclidean', n_jobs = number_of_threads)
    #matrix_2 = pairwise_distances(X = form_vectors, metric = distance_func, n_jobs = number_of_threads)
    matrix_2 = computePairwiseFormDistance(form_vectors, distance_func)
    
    distance_matrix = 0.5 * matrix_1 + 0.5 * matrix_2
    a = histogram(distance_matrix, density = True)
    print (a)
    
    return distance_matrix

def runKMeans(distance_matrix, nClusters, number_of_threads):
    
    km = KMeans(n_clusters=nClusters, max_iter = 100, init='k-means++', precompute_distances=True, n_jobs=number_of_threads)
    km.fit(distance_matrix)
    
    labels = km.labels_
    n_clusters = len(set(labels))- (1 if -1 in labels else 0)
    n_noises = list(labels).count(-1)
    
    print('Number of clusters' + str(n_clusters))
    print('Number of noises' + str(n_noises))

    return list(labels)

def runDBSCAN(distance_matrix, my_eps, my_min_samples, number_of_threads):
    db = DBSCAN(eps = my_eps, min_samples=my_min_samples, metric='precomputed', n_jobs=number_of_threads)
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
            count = min(for_noises, len(rules))
            selected_rules.extend(random.sample(rules, count))
        else:
            selected_rules.extend(random.sample(rules, for_cluster))
    return selected_rules
                