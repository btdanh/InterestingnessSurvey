'''
Created on Feb 7, 2017

@author: BanhDzui
'''
import getopt
import sys
import random

from IOHelper import readTransactionDBFileFrom, writeDataInLines

class TransactionSamplingArgs:
    def __init__(self):
        self.db_file = ''
        self.number_of_samples = 500
        
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['db=', 'nSamples='])
        except getopt.GetoptError:
            print ('--db : path of database file')
            print ('--output: path of the file containing selected transactions')
            print ('--nSamples: number of samples')
            return False
    
        for opt, arg in opts:
            
            if opt == '--db':
                self.db_file = arg
            elif opt == '--nSamples':
                self.number_of_samples = int(arg)
            
        return True
    
if __name__ == '__main__':
    
    config = TransactionSamplingArgs()
    if not config.loadArguments(sys.argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    data = readTransactionDBFileFrom(config.db_file, 1)
    n = min(len(data),config.number_of_samples)
    selected_trans = random.sample(data,n )
    writeDataInLines('reduced' + str(n) + config.db_file, selected_trans)
    print('Done!!!')