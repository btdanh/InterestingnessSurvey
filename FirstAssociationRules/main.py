import DataSet
import Apriori
import sys

def main(argv):
    input_file = 'input_4.csv'
    output_file = 'output_4.txt'
    min_sup = 2.0
    min_conf = 1
    apriori_alg = Apriori.Apriori(min_sup, min_conf)
    
    data = DataSet.DataSet()
    #data.loadInHorizontalFormat(input_file)
    data.loadInVerticalFormat(input_file)
    
    L = apriori_alg.generateFrequentItemSets(data)
    with open(output_file, "w") as text_file:
        for item_set in L:
            text_file.write(','.join(item for item in item_set))
            text_file.write('\n')
    
if __name__ == "__main__":
    main(sys.argv)