import DataSet
import Apriori
import sys
from AssociationRule import AssociationRuleGenerator
from InterestingnessMeasures import confidence, jaccard

def writeAssociationRulesToFile(file_name, rules):
    rules.sort(key=lambda x: (x[2], x[3]))
    with open(file_name, "w") as text_file:
        for r in rules:
            text_file.write(str(r[0]) + ' # ' + str(r[1]) + ' # ' + r[2] + '->' + r[3])
            text_file.write('\n')

def main(argv):
    input_file = 'input_4.csv'
    output_file_2 = 'output_4_jaccard.txt'
    output_file_1 = 'output_4_confidence.txt'
    min_sup = 5.0
    min_conf = 1
    apriori_alg = Apriori.Apriori(min_sup, min_conf)
    
    data = DataSet.DataSet()
    #data.loadInHorizontalFormat(input_file)
    data.loadInVerticalFormat(input_file)
    
    frequent_itemsets = apriori_alg.generateFrequentItemSets(data, 4)
    
    conf_generator = AssociationRuleGenerator(confidence)
    conf_rules_and_ranks = conf_generator.generateRules(frequent_itemsets)
    print('selecting rule for evaluation......')
    conf_rules = conf_generator.selectEvaluatedRules(conf_rules_and_ranks, 10)
    print('searching ranks for selected rules...')
    conf_ranks = conf_generator.searchRankForValues(conf_rules.values(), conf_rules_and_ranks[1])
    
    print('writing rules for confidence...')
    writeAssociationRulesToFile(output_file_1, conf_ranks)
    print ("Done!!!")
    
    jacc_generator = AssociationRuleGenerator(jaccard)
    jacc_rules_and_ranks = jacc_generator.generateRules(frequent_itemsets, conf_rules)
    print('searching ranks for selected rules...')
    jacc_ranks = jacc_generator.searchRankForValues(jacc_rules_and_ranks[0], jacc_rules_and_ranks[1])
    
    print('writing rules for jaccard...')
    writeAssociationRulesToFile(output_file_2, jacc_ranks)
    print ("Done!!!")
                
if __name__ == "__main__":
    main(sys.argv)