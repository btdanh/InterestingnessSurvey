import DataSet
import Apriori
import sys
from AssociationRule import AssociationRuleGenerator
from InterestingnessMeasures import confidence, jaccard

def main(argv):
    input_file = 'input_4.csv'
    output_file = 'output_4_jaccard.txt'
    min_sup = 5.0
    min_conf = 1
    apriori_alg = Apriori.Apriori(min_sup, min_conf)
    
    data = DataSet.DataSet()
    #data.loadInHorizontalFormat(input_file)
    data.loadInVerticalFormat(input_file)
    
    frequent_itemsets = apriori_alg.generateFrequentItemSets(data, 4)
    
    rule_generator = AssociationRuleGenerator(jaccard)
    rules = rule_generator.generateRules(frequent_itemsets, 100)
    
    print('writing best rules to find...')
    with open(output_file, "w") as text_file:
        for r in rules:
            text_file.write(str(r[0]) + ' # ' + r[1] + '->' + r[2])
            text_file.write('\n')
    print ("Done!!!")
                
if __name__ == "__main__":
    main(sys.argv)