import getopt
from InterestingPatterns.AssociationRuleGenerator import massSpectrumFilter
from UnexpectedPatterns.RulesClustering import generalDistance, detailDistance

class ProgramArguments:
    
    def __init__(self):
        self.db_file = ''
        self.opt = ''
        self.min_sup = 1
        self.freq_itemset_file = ''
        self.rules_file = ''
        self.samples_file = ''
        self.interestingness_file = ''
        self.correlation_file = ''
        self.clusters_file = ''
        self.clustering_algorithm = ''
        self.number_of_samples = None
        self.from_index = 1 # not limited
        self.to_index = 1
        self.rule_filter = None
        self.distance_function = None
        self.number_of_processes = 2
        self.k_1_frequent_itemsets_file = ''
    
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['option=','db=', 'minsup=', 'itemset=', 'rules=', 'interest=', 
                                                      'corr=', 'clusters=', 'samples=', 'alg=', 'amount=', 'from=', 'to=', 
                                                      'rfilter=', 'distance=', 'threads=', 'prefile='])
        except getopt.GetoptError:
            print ('main.py --option=<function> --db=<database file> --minsup=<min sup value> --alg=<clustering algorithm> --itemset=<frequent itemset file> --rules=<rules files> --interest=<interestingness file> --corr=<correlation coefficient file --clusters=<clustering result file> --samples=<samples file> --amount=<number of samples>')
            return False
    
        for opt, arg in opts:
            
            if opt == '--option':
                self.opt = arg
            elif opt == '--db':
                self.db_file = arg
            elif opt == '--minsup':
                self.min_sup = float(arg)
            elif opt == '--itemset':
                self.freq_itemset_file = arg
            elif opt == '--rules':
                self.rules_file = arg
            elif opt == '--interest':
                self.interestingness_file = arg
            elif opt == '--corr':
                self.correlation_file = arg
            elif opt == '--clusters':
                self.clusters_file = arg 
            elif opt == '--samples':
                self.samples_file = arg 
            elif opt == '--alg':
                self.clustering_algorithm = arg
            elif opt == '--amount':
                self.number_of_samples = int(arg)
            elif opt == '--from':
                self.from_index = int(arg)
            elif opt == '--to':
                self.to_index = int(arg)
            elif opt == '--rfilter':
                self.rule_filter = massSpectrumFilter
            elif opt == '--distance':
                if arg == 'general':
                    self.distance_function = generalDistance
                if arg == 'detail':
                    self.distance_function = detailDistance
            elif opt == '--threads':
                self.number_of_processes = int(arg)
            elif opt == '--prefile':
                self.k_1_frequent_itemsets_file = arg
                
                 
        return True
            
