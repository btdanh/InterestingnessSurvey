'''
Created on Feb 6, 2017

@author: BanhDzui
'''

import getopt
import sys

from InterestingPatterns.DataSet import DataSet
from InterestingPatterns import AprioriHashTable

from InterestingPatterns.Apriori import generateL1, insertHashIntoDictionary, generateFrequentItemSets
from IOHelper import appendFrequentItemsetsToFile

class GenerateFrequentItemsetArgs:
    def __init__(self):
        self.db_file = ''
        self.min_sup = 2
        self.output_file = ''
        self.number_of_processes = 1
        self.from_index = 1
        self.to_index = 2
        self.pre_file = ''
        
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['db=', 'minsup=', 'output=', 'threads=', 'from=', 'to=', 'fprevious='])
        except getopt.GetoptError:
            print ('--db : path of database file')
            print ('--minsup: minimum support value')
            print ('--output: path of the file containing frequent itemsets')
            print ('--threads: number of processes for running')
            print ('--from: size (in items) of minimum frequent itemset')
            print ('--to: size (in items) of maxiumum frequent itemset')
            print ('--fprevious: path of the file containing the frequent itemsets in previous run, should be from - 1')
            return False
    
        for opt, arg in opts:
            
            if opt == '--db':
                self.db_file = arg
            elif opt == '--minsup':
                self.min_sup = float(arg)
            elif opt == '--output':
                self.output_file = arg
            elif opt == '--threads':
                self.number_of_processes = int(arg)
            elif opt == '--from':
                self.from_index = int(arg)
            elif opt == '--to':
                self.to_index = int(arg)
            elif opt == '--fprevious':
                self.pre_file = arg
            
        return True

def main(argv):
    
    config = GenerateFrequentItemsetArgs()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    L_k_1 = None
    k = config.from_index
    if k == 1:
        dataset = DataSet()
        
        print ('loading transaction database ....')
        dataset.loadInHorizontalFormat(config.db_file)
        #data.loadInVerticalFormat(config.db_file)
        
        L_k_1 = generateL1(config.min_sup,dataset)
        L = {}
        insertHashIntoDictionary(L_k_1, L)
        appendFrequentItemsetsToFile(config.output_file, L, dataset.size())
        
        k += 1
    else:
        L_k_1 = AprioriHashTable()
        L_k_1.loadFromFile(config.pre_file)
    
    print ('generating frequent item-sets ....')
    last_rules_table, all_rules_table = generateFrequentItemSets(config.min_sup, config.number_of_processes, k, config.to_index, L_k_1)
    last_rules_table.writeToFile(config.pre_file)
    
    print ('writing frequent item-sets to file ....')
    appendFrequentItemsetsToFile(config.output_file, all_rules_table, None)
    
    print ('Size of the last frequent itemsets: ' + str(last_rules_table.size()))
    print('Done!!!')
        
if __name__ == '__main__':
    main(sys.argv)