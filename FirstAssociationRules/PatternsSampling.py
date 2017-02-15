'''
Created on Feb 7, 2017

@author: BanhDzui
'''

import getopt
import sys
import numpy as np
import heapq

from IOHelper import readRulesClusters
from UnexpectedPatterns.RulesClustering import selectCandidateFromClusters
from InterestingPatterns.AssociationRuleGenerator import selectRandomRules
from multiprocessing.util import sub_debug
    
def writeRulesForAnnotation(file_name, association_rules):
    with open(file_name, "w") as text_file:
        for rule in association_rules:
            text_file.write(rule)
            text_file.write(':')
            text_file.write('u')
            text_file.write('\n')
            
def readRankingFile(input_file):
    
    association_rules = []
    ranking = []
    k = 0
    with open(input_file, "r") as text_file:
        for line in text_file:
            subStrings = line.split(';')
            rule_key = subStrings[0].strip()
            association_rules.append(rule_key)
            ranking.append([])
            for v in subStrings[1:]:
                r = int(v)
                ranking[k].append(r)
            
            k += 1
            if k % 1000 == 0: print(str(k))
    return association_rules, np.array(ranking) 

def selectCandidateByDisjointAlgorithm(association_rules, k, rank_matrix):
    selected_rules = []
    ''' Compute mean and standard deviation of rankings'''
    std_for_patterns = np.std(rank_matrix, axis = 1)
    
    m = np.argmax(std_for_patterns)
    selected_rules.append(association_rules[m])
    association_rules.pop(m)
    
    
    n = len(association_rules)
    dij = np.zeros((n, n))
    
    for i in range(n):
        if i % 100 == 0:
            print(str(i))
        for j in range (0, i):
            delta = rank_matrix[i] - rank_matrix[j]
            mean_delta = np.mean(delta)
            std_delta = np.std(delta)
            
            dij[i][j] = mean_delta + std_delta
            dij[j][i] = -mean_delta + std_delta
            
    sum_dij = np.sum(dij, axis=0)
    largest_indexes = heapq.nlargest(k - 1, range(n), sum_dij.take) 
    for index in largest_indexes:
        selected_rules.append(association_rules[index])       
                        
    return selected_rules

class PatternSamplingArgs:
    def __init__(self):
        self.opt = 'random'
        self.input_file = ''
        self.number_of_inputs = 1
        self.output_file = ''
        self.sampling_rate = 0.2
        
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['option=', 'input=', 'nInput=', 'output=', 'rate='])
        except getopt.GetoptError:
            print ('--options : algorithm to select patterns')
            print ('--input : path of input file(s)')
            print ('--nInput : number of input file(s)')
            print ('--output: path of the file containing selected patterns')
            print ('--rate: sampling rate')
            return False
    
        for opt, arg in opts:
            if opt == '--option':
                self.opt = arg
            elif opt == '--input':
                self.input_file = arg
            elif opt == '--output':
                self.output_file = arg
            elif opt == '--nInput':
                self.number_of_inputs = int(arg)
            elif opt == '--rate':
                self.sampling_rate = float(arg)
        return True

def main(argv):
    config = PatternSamplingArgs()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
    
    if (config.opt == 'random'):
        selected_rules = selectRandomRules(config.input_file,config.number_of_inputs, config.sampling_rate)
        writeRulesForAnnotation(config.output_file, selected_rules)
    elif (config.opt == 'disjoint'):
        association_rules,rank_matrix = readRankingFile(config.input_file)
        print (rank_matrix)
        candidates = selectCandidateByDisjointAlgorithm(association_rules, 500, rank_matrix)
        writeRulesForAnnotation(config.output_file, candidates)
    else:
        association_rules = readRulesClusters(config.input_file)
        candidates = selectCandidateFromClusters(association_rules, 2, config.number_of_samples)
        writeRulesForAnnotation(config.output_file, candidates)
    
    print('Done!!!')
    
if __name__ == '__main__':
    main(sys.argv)