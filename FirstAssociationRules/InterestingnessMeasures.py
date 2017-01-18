import math

def conditionalProbability(both, condition):
    return both/condition

# These measures for rule: left -> right

def confidence(left, right, both, total, k = 1, m = 1):
    return conditionalProbability(both, left)

def coverage(left, right, both, total, k = 1, m = 1):
    return left/total

def prevalence(left, right, both, total, k = 1, m = 1):
    return right/total

def recall(left, right, both, total, k = 1, m = 1):
    return conditionalProbability(both, right)

def specificity(left, right, both, total, k = 1, m = 1):
    not_both = total - (left + right - both)
    not_left = total - left
    return conditionalProbability(not_both, not_left)

def accuracy(left, right, both, total, k = 1, m = 1):
    not_both = total - (left + right - both)
    return both/total + not_both/total

def lift(left, right, both, total, k = 1, m = 1):
    return conditionalProbability(both, left) * (right/total)

def leverage(left, right, both, total, k = 1, m = 1):
    return conditionalProbability(both, left) - (left/total) * (right/total)

def changeOfSupport(left, right, both, total, k = 1, m = 1):
    return conditionalProbability(both, left) - right/total

def relativeRisk(left, right, both, total, k = 1, m = 1):
    not_left = total - left
    right_not_left = right - both
    
    return conditionalProbability(both, left) / conditionalProbability(right_not_left, not_left)

def jaccard(left, right, both, total, k = 1, m = 1):
    return both/(left + right - both)

def certaintyFactor(left, right, both, total, k = 1, m = 1):
    p_right = right/total
    return (conditionalProbability(both, left) - p_right)/(1 - p_right)

def oddRatio(left, right, both, total, k = 1, m = 1):
    not_both = total - (left + right - both)
    return (both / (left - both)) * (not_both/(right - both))

def yuleQ(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_not_both = 1 - (left + right - both)/total
    p_left_not_right = (left - both)/total
    p_right_not_left = (right - both)/total
    return (p_both * p_not_both - p_left_not_right * p_right_not_left)/(p_both * p_not_both + p_left_not_right * p_right_not_left)

def yuleY(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_not_both = 1 - (left + right - both)/total
    p_left_not_right = (left - both)/total
    p_right_not_left = (right - both)/total
    x = math.sqrt(p_both * p_not_both) - math.sqrt(p_left_not_right * p_right_not_left)
    y = math.sqrt(p_both * p_not_both) + math.sqrt(p_left_not_right * p_right_not_left)
    return x/y
    
def klosgen(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_right = right/total
    return math.sqrt(p_both) * (conditionalProbability(both, left) - p_right)

def conviction(left, right, both, total, k = 1, m = 1):
    p_left_not_right = (left - both)/total
    if p_left_not_right == 0:
        return float('inf')
    return (left/total) * ((total - right)/total) / p_left_not_right
    
def interestingnessWeightingDependency(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    return (math.pow(p_both/(p_left * p_right), k) - 1) * math.pow(p_both, m)

def collectiveStrength(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    p_not_both = 1 - (left + right - both)/total
    p_not_left = 1 - p_left
    p_not_right = 1 - p_right
    
    x = (p_both + conditionalProbability(p_not_both, p_not_left))/(p_left*p_right + p_not_left * p_not_right)
    y = (1 - p_left * p_right - p_not_left * p_not_right)/(1 - p_both - conditionalProbability(p_not_both, p_not_left))
    return x * y

def laplaceCorrection(left, right, both, total, k = 1, m = 1):
    return (both + 1)/(left + 2)

def giniIndex(left, right, both, total, k = 1, m = 1):
    p_left = left/total
    p_right = right/total
    p_not_left = 1 - p_left
    p_not_right = 1 - p_right
    
    p_right_con_left = conditionalProbability(both, left)
    p_not_right_con_left = conditionalProbability(left - both, left)
    p_right_con_not_left = conditionalProbability(right - both, total - left)
    p_not_right_con_not_left = conditionalProbability(total - left - right + both, total - left)
    
    x = p_left * (math.pow(p_right_con_left, 2) + math.pow(p_not_right_con_left, 2))
    y = p_not_left * (math.pow(p_right_con_not_left, 2) + math.pow(p_not_right_con_not_left, 2))
    return x + y - math.pow(p_right, 2) - math.pow(p_not_right, 2)

def jmeasure(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_right_con_left = conditionalProbability(both, left)
    p_left_not_right = (left - both)/total
    p_not_right_con_left = conditionalProbability(left - both, left)
    p_right = right/total
    p_not_right = 1 - p_right
    
    return p_both * math.log(p_right_con_left/p_right) + p_left_not_right * math.log(p_not_right_con_left/p_not_right) 

def oneWaySupport(left, right, both, total, k = 1, m = 1):
    p_right_con_left = conditionalProbability(both, left)
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    return p_right_con_left * math.log2(p_both/(p_left * p_right))
    
def twoWaysSupport(left, right, both, total, k = 1, m = 1):   
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    return p_both * math.log2(p_both/(p_left * p_right))

def twoWaysSupportVariation(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    p_left_not_right = (left - both)/total
    p_not_right = 1 - p_right
    
    p_right_not_left = (right - both)/total
    p_not_left = 1 - p_left
    
    p_not_left_not_right = 1 - (left + right - both)/total
    
    x = p_both * math.log2(p_both/(p_left * p_right));
    x = x + p_left_not_right * math.log2(p_left_not_right/(p_left * p_not_right))
    x = x + p_right_not_left * math.log2(p_right_not_left/(p_not_left * p_right)) 
    return (x + p_not_left_not_right * math.log2(p_not_left_not_right/(p_not_left*p_not_right)))

def linearCorrelationCoefficient(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    return (p_both - p_left * p_right)/math.sqrt(p_left * p_right * (1-p_left) * (1 - p_right))

def piatetskyShapiro(left, right, both, total, k = 1, m = 1):
    return (both/total) - (left/total) * (right/total)

def cosine(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    
    return p_both/math.sqrt(p_left * p_right)

def loevinger(left, right, both, total, k = 1, m = 1):
    p_left_not_right = (left - both)/total
    p_left = left/total
    p_not_right = 1 - right/total
    
    return 1 - (p_left * p_not_right)/p_left_not_right

def informationGain(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left = left/total
    p_right = right/total
    return math.log(p_both/(p_left * p_right))

def sebagSchoenauner(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left_not_right = (left  - both)/total
    return p_both/p_left_not_right

def leastContradiction(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left_not_right = (left  - both)/total
    p_right = right/total
    return (p_both - p_left_not_right)/p_right

def oddMultiplier(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left_not_right = (left  - both)/total
    p_right = right/total
    return (p_both * (1 - p_right))/(p_right * p_left_not_right)

def counterexampleRate(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left_not_right = (left  - both)/total
    return 1 - (p_left_not_right/p_both)

def zhang(left, right, both, total, k = 1, m = 1):
    p_both = both/total
    p_left_not_right = (left  - both)/total
    p_left = left/total
    p_right= right/total
    p_not_right = 1 - p_right
    
    x = p_both * p_not_right
    y = p_right * p_left_not_right
    if x < y: 
        x = y
    return (p_both - p_left * p_right)/y