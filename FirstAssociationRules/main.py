import DataSet
import Apriori
import sys

def main(argv):
    input_file = 'input_4.csv'
    output_file = 'output'
    min_sup = 2.0
    min_conf = 1
    apriori_alg = Apriori.Apriori(min_sup, min_conf)
    
    data = DataSet.DataSet()
    #data.loadInHorizontalFormat(input_file)
    data.loadInVerticalFormat(input_file)
    
    apriori_alg.generateFrequentItemSets(data, 4, output_file)
    
if __name__ == "__main__":
    main(sys.argv)