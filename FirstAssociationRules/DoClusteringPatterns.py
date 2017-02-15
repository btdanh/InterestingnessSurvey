'''
Created on Feb 6, 2017

@author: BanhDzui
'''

import getopt
import sys

from IOHelper import readFrequentItemsets, readAssociationRules, writeClustersOfRules,\
    writeDataInLines, writeSerializableObject
from UnexpectedPatterns.kmedoids import kMedoids

from UnexpectedPatterns.RulesClustering import computeFormDistance1, computeFormDistance2,\
    generateFormVectors, generateNumericVectors, computeDistanceMatrix, runDBSCAN

class ComputeDistanceArgs:
    def __init__(self):
        self.freq_itemset_file = ''
        self.rules_file = ''
        
        self.number_of_processes = 1
        self.distance_function = None
        
        self.medoids_file = '' 
        
        self.output_file = ''
        
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['fItemsets=', 'fRules=', 'output=', 'distance=', 'threads=', 'fMedoids='])
        except getopt.GetoptError:
            print ('--fItemsets : file containing frequent item-sets')
            print ('--fRules : file containing association rules')
            print ('--nFiles : number of files containing rules')
            print ('--nSamples: number of selected samples')
            print ('--distance: distance function between two rule(detail/general)')
            print ('--threads: number of processes')
            print ('--output: path of the file containing clusters and theirs members')
            print ('--fMedoids: file saving medoids (if using KMedoids) ')
            return False
    
        for opt, arg in opts:
            
            if opt == '--fItemsets':
                self.freq_itemset_file = arg
            elif opt == '--fRules':
                self.rules_file = arg
            elif opt == '--output':
                self.output_file = arg
            elif opt == '--distance':
                if arg == 'general':
                    self.distance_function = computeFormDistance1
                if arg == 'detail':
                    self.distance_function = computeFormDistance2
            elif opt == '--threads':
                self.number_of_processes = int(arg)    
            elif opt == '--fMedoids':
                self.medoids_file = arg            
                 
        return True
def main(argv):
    
    config = ComputeDistanceArgs()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    print('loading frequent itemsets....')
    datasize, frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
    
    print('loading association rules ....')
    association_rules = {}
    readAssociationRules(config.rules_file, association_rules)
    
    print ('generating feature vectors for each rule....')
    rules_keys = association_rules.keys()
    form_vectors = generateFormVectors(rules_keys, association_rules)
    numeric_vectors = generateNumericVectors(rules_keys, association_rules, frequent_itemsets, datasize)
    
    print ('computing distances ....')
    distance_matrix = computeDistanceMatrix(numeric_vectors, form_vectors, 
                                            config.distance_function, config.number_of_processes)
    
    print ('clustering ....')
    #medoids, labels = kMedoids(distance_matrix, 1000, 10000)
    labels = runDBSCAN(distance_matrix, 0.4, 4, config.number_of_processes)
    #labels = runKMeans(distance_matrix, 500, config.number_of_processes)
    
    print('writing clusters to file....')
    writeClustersOfRules(config.output_file, association_rules.keys(), labels)
    
    writeSerializableObject('distance_logs.txt', distance_matrix)
    
    print ('write selecting medoids to file ...')
    '''selected_rules = []
    for index in medoids:
        selected_rules.append(rules_keys[index])
    writeDataInLines(config.medoids_file, selected_rules)
    '''
    print('Done!!!')
    
if __name__ == '__main__':
    main(sys.argv)