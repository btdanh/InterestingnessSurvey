import sys
from InterestingPatterns.DataSet import DataSet
from InterestingPatterns.Apriori import generateFrequentItemSets, generateL1, insertHashIntoDictionary
from InterestingPatterns.AssociationRuleGenerator import generateRules, selectRandomRules, computeInterestingness,searchRankForValues
from UnexpectedPatterns.RulesClustering import generateRuleVector, computeDistances, runDBSCAN,\
    selectCandidateFromClusters
from ProgramArguments import ProgramArguments
from IOHelper import appendFrequentItemsetsToFile, appendAssociationRulesToFile,\
    readFrequentItemsets, readAssociationRules, writeInterestingness,\
    writeCorrelationMatrix, writeClustersOfRules, readRulesClusters, writeRulesForAnnotation,\
    writeTransactionDB, appendFrequentItemsetsToFile, readTransactionDBFileFrom
from InterestingPatterns.InterestingnessMeasures import *
from InterestingPatterns.CorrelationMeasures import computePearmanCorrelation
import random
from InterestingPatterns.AprioriHashTable import AprioriHashTable

#from InterestingPatterns.CorrelationMeasures import computePearmanCorrelation


            
def main(argv):
    
    config = ProgramArguments()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
    '''
    -----------------GENERATE FREQUENT ITEMSETS--------------------------
    '''
    if config.opt == 'generate_frequent_itemsets':
        
        L_k_1 = None
        k = config.from_index
        if k == 1:
            dataset = DataSet()
            
            print ('loading transaction database ....')
            dataset.loadInHorizontalFormat(config.db_file)
            #data.loadInVerticalFormat(config.db_file)
            
            L_k_1 = generateL1(config.min_sup,dataset)
            L = {}
            insertHashIntoDictionary(L_k_1, L)
            appendFrequentItemsetsToFile(config.freq_itemset_file, L, dataset.size())
            
            k += 1
        else:
            L_k_1 = AprioriHashTable()
            L_k_1.loadFromFile(config.k_1_frequent_itemsets_file)
        
        print ('generating frequent item-sets ....')
        generate_result = generateFrequentItemSets(config.min_sup, config.number_of_processes, k, config.to_index, L_k_1)
        generate_result[0].writeToFile(config.k_1_frequent_itemsets_file)
        
        print ('writing frequent item-sets to file ....')
        appendFrequentItemsetsToFile(config.freq_itemset_file, generate_result[1], None)
        
        print ('Size of the last frequent itemsets: ' + str(generate_result[0].size()))
        print('Done!!!')
    '''
    ------------------GENERATE ASSOCIATION RULES-------------------------
    '''
    if config.opt == 'generate_rules':
        print('loading frequent item-sets....')
        frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
        
        print ('generating rules ....')
        association_rules = generateRules(frequent_itemsets[1], config.number_of_processes, config.rule_filter, config.from_index, config.to_index)    
       
        print('writing association rule to file ....')
        appendAssociationRulesToFile(config.rules_file, association_rules)
        print ('Done !!!')
    
    '''
    ----------------COMPUTE CORRELATION---------------------------
    '''
    if config.opt == 'compute_correlation':
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
        
        rank_indicators = computeInterestingness(measures, association_rules, frequent_itemsets[1], frequent_itemsets[0])
        print ('selecting association rules....')
        selected_keys = selectRandomRules(association_rules, config.number_of_samples)
        print ('assigning rank to association rules....')
        rank_matrix = searchRankForValues(measures, selected_keys, association_rules, rank_indicators)
        correlation_matrix = computePearmanCorrelation(rank_matrix)
        
        print ('writing result to files ....')
        writeInterestingness(config.interestingness_file, selected_keys, association_rules)
        writeCorrelationMatrix(config.correlation_file, correlation_matrix[0])
        writeCorrelationMatrix("ranks.txt", rank_matrix)
        print('Done!!!')
    '''
    ----------------DO CLUSTERING---------------------------
    '''    
    if config.opt == 'clustering':
        print('loading frequent itemsets....')
        frequent_itemsets = readFrequentItemsets(config.freq_itemset_file)
        
        print('loading association rules ....')
        association_rules = readAssociationRules(config.rules_file)
        
        print ('selecting association rules....')
        selected_keys = selectRandomRules(association_rules, config.number_of_samples)
        
        print ('generating feature vectors for each rule....')
        rule_vectors = generateRuleVector(selected_keys, association_rules, frequent_itemsets[1], frequent_itemsets[0])
        
        print ('computing distances ....')
        distance_matrix = computeDistances(rule_vectors, config.number_of_processes, config.distance_function)
        print ('clustering ....')
        labels = runDBSCAN(distance_matrix, 1.8, 3)
        
        print('writing clusters to file....')
        writeClustersOfRules(config.clusters_file, selected_keys, labels)
        print('Done!!!')
    
    '''
    ----------------COMPUTE CORRELATION---------------------------
    '''
    if (config.opt == 'select_rules'):
        association_rules = readRulesClusters(config.db_file)
        selectCandidateFromClusters(association_rules, 3, 0.5)
        writeRulesForAnnotation(config.interestingness_file)
        print('Done!!!')
    '''
    ----------------SELECT DB TRANSACTIONS--------------------------
    '''
    if (config.opt == 'select_trans'):
        data = readTransactionDBFileFrom(config.db_file, 1)
        n = min(len(data),config.number_of_samples)
        selected_trans = random.sample(data,n )
        writeTransactionDB('reduced' + str(n) + config.db_file, selected_trans)
        print('Done!!!')
                
if __name__ == "__main__":
    main(sys.argv)
