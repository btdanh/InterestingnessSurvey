'''
Created on Jan 24, 2017

@author: BanhDzui
'''
import numpy

class NeighborBasedMethod(object):
    '''
    This algorithm is proposed by Guozhu Dong and Jinyan Li, 1998. 
    It is a method determining which patterns are unexpected by using neighbors and their confidence
    '''


    def __init__(self, theta, radius, threshold, density):
        self.theta = theta
        self.radius = radius
        self.threshold = threshold
        self.density = density
        
    
    def discoverUnexpectedPattern(self, association_rules):
        other_rules = []
        unexpected_rules = []
        
        for first_key in association_rules.keys():
            neighbors = []
            for second_key in association_rules.keys():
                if first_key == second_key: continue
                d = association_rules[first_key].distance(association_rules[second_key])
                # second rule is neighbor of first rule
                if d <= self.radius:
                    neighbors.append(association_rules[second_key].firstScore())
            if len(neighbors) <= self.density:
                unexpected_rules.append(first_key)
            else:
                a = numpy.array(neighbors)
                mean = numpy.mean(a)
                std = numpy.std(a) 
            
                if abs(abs(association_rules[first_key].firstScore() - mean) - std) >= self.threshold:
                    unexpected_rules.append(first_key)
                else:
                    other_rules.append(first_key)
        return (unexpected_rules, other_rules)
                