'''
Created on Feb 6, 2017

@author: BanhDzui
'''
import sys
import numpy
import getopt

from InterestingPatterns.InterestingnessMeasures import *

from InterestingPatterns.AssociationRuleGenerator import AssociationRule
from InterestingPatterns.ItemsetHelper import getItemsetFromKey

from IOHelper import readFrequentItemsets, writeSerializableObject,\
    loadSerializeObject, readAssociationRules
from builtins import range


def findRank(item_list, element):
    left = 0
    right = len(item_list) - 1
    
    while left <= right:
        pivot = int((left + right)/2)
        if element == item_list[pivot]:
            return pivot + 1
        elif element < item_list[pivot]:
            left = pivot + 1
        else:
            right = pivot -1
    return -1

def rankAssociationRules(input_file, output_file, indicators, nBins):
    
    bin_ranges = []
    for pair in indicators:
        x = (pair[1] - pair[0])/nBins
        bin_ranges.append(x)
    
    k = 0
    with open(output_file, 'w') as write_file:
        with open(input_file, "r") as text_file:
            for line in text_file:
                k += 1
                if k % 5000 == 0: print(str(k))
                
                subStrings = line.split(';')
                rule_key = subStrings[0].strip()
                write_file.write(rule_key)
                i = 0
                for value in subStrings[1:]:
                    write_file.write(';')
                    
                    x = float(value)
                    if x < indicators[i][0]:
                        write_file.write(str(nBins+2))
                    elif x > indicators[i][1]:
                        write_file.write(str(0))
                    else:
                        r = int((x - indicators[i][0])/bin_ranges[i]) + 1
                        write_file.write(str(r))
                    i += 1
                write_file.write('\n')
       
def computeRankIndicators(n_measures, interesting_file):
    indicators = []
    for i in range(n_measures):
        indicators.append([float('inf'), float('-inf')])
    
    k = 0
    with open(interesting_file, "r") as text_file:
        for line in text_file:
            k += 1
            if k % 5000 == 0: print(str(k))
            
            subStrings = line.split(';')
            i = 0
            for value in subStrings[1:]:
                x = float(value)
                if not math.isinf(x):
                    if x < indicators[i][0]:
                        indicators[i][0] = x
                    if x > indicators[i][1]:
                        indicators[i][1] = x
                i += 1
    return indicators
                        
def computeInterestingness(measures, input_file, output_file, frequent_itemsets, total):
    k = 0
    with open(output_file, 'w') as write_file:
        with open(input_file, "r") as text_file:
            for line in text_file:
                k+= 1
                if k % 5000 == 0: print('computed ' + str(k) + ' patterns')
                subStrings = line.split(">")
                left_key = subStrings[0].strip()
                right_key = subStrings[1].strip()
                
                left = getItemsetFromKey(left_key)
                right = getItemsetFromKey(right_key)
                
                rule = AssociationRule(left, right)
                
                left = frequent_itemsets[left_key]
                right = frequent_itemsets[right_key]
                both = frequent_itemsets[rule.getItemsetKey()]
                
                write_file.write(rule.getRuleKey())
                
                for index in range(len(measures)):
                    value = measures[index](left, right, both, total)
                    write_file.write(';')
                    write_file.write(str(value))
                write_file.write('\n')        
               

class ComputeCorrelationArgs:
    def __init__(self):
        self.option = ''
        self.other_file = ''
        self.input_file = ''
        self.output_file = ''
    
    def loadArguments(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], '', ['option=','other=', 'input=','output='])
        except getopt.GetoptError:
            print ('--input : file containing association rules or interestingness values')
            print ('--output : result file')
            print ('--other : another input file')
            return False
    
        for opt, arg in opts:
            
            if opt == '--option':
                self.option = arg
            elif opt == '--other':
                self.other_file = arg
            elif opt == '--input':
                self.input_file = arg
            elif opt == '--output':
                self.output_file = arg 
        return True
    
def main(argv):
    
    config = ComputeCorrelationArgs()
    if not config.loadArguments(argv) :
        print ('Arguments is not correct. Please try again ...')
        sys.exit(2)
        
    if (config.option == 'compute'):
        print ('computing correlation among interestingness measures...')
        measures = [confidence, coverage, prevalence, recall, specificity, accuracy, lift, leverage, changeOfSupport,
                relativeRisk, jaccard, certaintyFactor, oddRatio, yuleQ, yuleY, klosgen, conviction,
                interestingnessWeightingDependency, collectiveStrength, laplaceCorrection, jmeasure, oneWaySupport,
                twoWaysSupport, twoWaysSupportVariation, linearCorrelationCoefficient, piatetskyShapiro, loevinger,
                informationGain, sebagSchoenauner, leastContradiction, oddMultiplier, counterexampleRate, zhang]
        print('loading frequent item-sets....')
        data_size, frequent_itemsets = readFrequentItemsets(config.other_file)
        
     
        print ('computing interestingness for all rules ....')
        computeInterestingness(measures, config.input_file, config.output_file, frequent_itemsets, data_size)
    elif (config.option == 'indicator'):
        rank_indicators = computeRankIndicators(33, config.input_file)
        writeSerializableObject(config.output_file, rank_indicators)
    elif (config.option == 'rank'):
        rank_indicators = loadSerializeObject(config.other_file)
        
        print('ranking rules...')
        rankAssociationRules(config.input_file, config.output_file, rank_indicators, 5000)
        
    else:
        print ('Not support this argument.')
    
    print('Done!!!')
    
if __name__ == '__main__':
    main(sys.argv)