'''
Created on Feb 6, 2017

@author: BanhDzui
'''

import getopt
import sys

from IOHelper import readFrequentItemsets
from InterestingPatterns.AssociationRuleGenerator import massSpectrumFilter, generateRules

class GenerateAssociationRulesArgs:
    def __init__(self):
        
        self.freq_itemset_file = ''
        self.output_file = ''
        self.rule_filter = None
        self.number_of_processes = 2
        
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['fItemsets=', 'output=', 'filter=', 'threads='])
        except getopt.GetoptError:
            print ('--fItemsets : file containing all frequent item-sets')
            print ('--output : file containing all association rules')
            print ('--filter : constraints to filter rules (default is None)')
            print ('--threads : number of processes')
            return False
    
        for opt, arg in opts:
            
            if opt == '--fItemsets':
                self.freq_itemset_file = arg
            elif opt == '--output':
                self.output_file = arg
            elif opt == '--filter':
                self.rule_filter = massSpectrumFilter
            elif opt == '--threads':
                self.number_of_processes = int(arg)
            
        return True

def main(argv):
    
    config = GenerateAssociationRulesArgs()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    print('loading frequent item-sets....')
    datasize, frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
        
    print ('generating rules ....')
    generateRules(frequent_itemsets, config.number_of_processes, config.rule_filter, config.output_file)    
   
    print ('Done !!!')
    
if __name__ == '__main__':
    main(sys.argv)
    