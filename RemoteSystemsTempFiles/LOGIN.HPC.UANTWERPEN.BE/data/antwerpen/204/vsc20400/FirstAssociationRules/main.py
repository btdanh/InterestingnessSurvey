import sys
from InterestingPatterns.Apriori import Apriori
from InterestingPatterns.DataSet import DataSet
from InterestingPatterns.AssociationRuleGenerator import AssociationRuleGenerator
from UnexpectedPatterns.RulesClustering import generateRuleVector, computeDistances, runDBSCAN
from ProgramArguments import ProgramArguments
from IOHelper import writeFrequentItemsets, writeAssociationRules,\
    readFrequentItemsets, readAssociationRules, writeInterestingness,\
    writeCorrelationMatrix, writeClustersOfRules
from InterestingPatterns.InterestingnessMeasures import *
from InterestingPatterns.CorrelationMeasures import computePearmanCorrelation

            
def main(argv):
    
    config = ProgramArguments()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    if config.opt == 'generate_rules':
        apriori_alg = Apriori(config.min_sup)
        data = DataSet()
        print ('loading transaction database ....')
        data.loadInHorizontalFormat(config.db_file)
        
        #data.loadInVerticalFormat(config.db_file)
        print ('generating frequent item-sets ....')
        frequent_itemsets = apriori_alg.generateFrequentItemSets(data, 4)
        print('generating all association rules...')
        rule_generator = AssociationRuleGenerator([])
        association_rules = rule_generator.generateRules(frequent_itemsets)    
        print ('writing frequent item-sets to file ....')
        writeFrequentItemsets(config.freq_itemset_file, frequent_itemsets, data.size())
        print('writing association rule to file ....')
        writeAssociationRules(config.rules_file, association_rules)
        print ('Done !!!')
    elif config.opt == 'compute_correlation':
        print ('computing correlation among interestingness measures...')
        measures = [confidence, coverage, prevalence, recall, specificity, accuracy, lift, leverage, changeOfSupport,
                    relativeRisk, jaccard, certaintyFactor, oddRatio, yuleQ, yuleY, klosgen, conviction,
                    interestingnessWeightingDependency, collectiveStrength, laplaceCorrection, jmeasure, oneWaySupport,
                    twoWaysSupport, twoWaysSupportVariation, linearCorrelationCoefficient, piatetskyShapiro, loevinger,
                    informationGain, sebagSchoenauner, leastContradiction, oddMultiplier, counterexampleRate, zhang]
        print('loading frequent item-sets....')
        frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
        
        print('loading association rules ....')
        association_rules = readAssociationRules(config.rules_file)
        
        print ('computing interestingness for all rules ....')
        rule_generator = AssociationRuleGenerator(measures)
        rank_indicators = rule_generator.computeInterestingness(association_rules, frequent_itemsets[1], frequent_itemsets[0])
        print ('selecting association rules....')
        selected_keys = AssociationRuleGenerator.selectRandomRules(association_rules, config.number_of_samples)
        print ('assigning rank to association rules....')
        rank_matrix = rule_generator.searchRankForValues(selected_keys, association_rules, rank_indicators)
        correlation_matrix = computePearmanCorrelation(rank_matrix)
        
        print ('writing result to files ....')
        writeInterestingness(config.interestingness_file, selected_keys, association_rules)
        writeCorrelationMatrix(config.correlation_file, correlation_matrix[0])
        writeCorrelationMatrix("ranks.txt", rank_matrix)
        print('Done!!!')
        
    elif config.opt == 'clustering':
        print('loading frequent itemsets....')
        frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
        
        print('loading association rules ....')
        association_rules = readAssociationRules(config.rules_file)
        
        print ('selecting association rules....')
        selected_keys = AssociationRuleGenerator.selectRandomRules(association_rules, config.number_of_samples)
        
        print ('generating feature vectors for each rule....')
        rule_vectors = generateRuleVector(selected_keys, association_rules, frequent_itemsets[1], frequent_itemsets[0])
        
        print ('clustering rules ....')
        distance_matrix = computeDistances(rule_vectors)
        labels = runDBSCAN(distance_matrix, 2.5, 3)
        
        print('writing clusters to file....')
        writeClustersOfRules(config.clusters_file, selected_keys, labels)
        print('Done!!!')
    else:
        print ('The option is not supported!!!')
                
if __name__ == "__main__":
    main(sys.argv)