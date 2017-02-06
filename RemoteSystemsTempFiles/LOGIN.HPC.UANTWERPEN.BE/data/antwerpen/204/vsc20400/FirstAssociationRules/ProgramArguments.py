import getopt

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
        self.number_of_samples = 1000
    
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['option=','db=', 'minsup=', 'itemset=', 'rules=', 'interest=', 'corr=', 'clusters=', 'samples=', 'alg=', 'amount='])
        except getopt.GetoptError:
            print ('main.py --option=<function> --db=<database file> --minsup=<min sup value> --alg=<clustering algorithm> --itemset=<frequent itemset file> --rules=<rules files> --interest=<interestingness file> --corr=<correlation coefficient file --clusters=<clustering result file --samples=<samples file> --amount=<number of samples>')
            return False
    
        for opt, arg in opts:
            if opt == "--option":
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
                 
        return True
            