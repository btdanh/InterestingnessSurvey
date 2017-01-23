import DataSet
import Apriori
import sys
from AssociationRule import AssociationRuleGenerator
from InterestingnessMeasures import confidence, jaccard, coverage
import CorrelationMeasures

def writeAssociationRules(file_name, selected_keys, association_rules):
    with open(file_name, "w") as text_file:
        for rule in selected_keys:
            text_file.write(rule)
            values = association_rules[rule]
            text_file.write(';')
            text_file.write(';'.join(map(str, values)))
            text_file.write('\n')
            
def writeMatrix(file_name, matrix):
    with open(file_name, "w") as text_file:
        for line in matrix:
            text_file.write(','.join(map(str, line)))
            text_file.write('\n')
            
def main(argv):
    input_file = 'input_4.csv'
    output_file_1 = 'rules_4.csv'
    output_file_2 = 'ranks_4.csv'
    output_file_3 = 'correlation_4.csv'
    
    min_sup = 5.0
    min_conf = 1
    apriori_alg = Apriori.Apriori(min_sup, min_conf)
    
    data = DataSet.DataSet()
    #data.loadInHorizontalFormat(input_file)
    data.loadInVerticalFormat(input_file)
    
    frequent_itemsets = apriori_alg.generateFrequentItemSets(data, 4)
    
    measures = [confidence, jaccard, coverage]
    rule_generator = AssociationRuleGenerator(measures)
    rules_and_ranks = rule_generator.generateRules(frequent_itemsets)    
    selected_keys = rule_generator.selectRandomRules(rules_and_ranks[0], 3000)
    print('writing selected rules....')
    writeAssociationRules(output_file_1, selected_keys, rules_and_ranks[0])
    
    ranks_matrix = rule_generator.searchRankForValues(selected_keys, rules_and_ranks[0], rules_and_ranks[1])
    print('writing rank matrix ....')
    writeMatrix(output_file_2, ranks_matrix)
    
    correlation_coefs = CorrelationMeasures.computePearmanCorrelation(ranks_matrix)
    print('writing correlation matrix ...')
    writeMatrix(output_file_3, correlation_coefs[0])
    
    print ("Done!!!")
                
if __name__ == "__main__":
    main(sys.argv)