from scipy import stats
 
def computePearmanCorrelation(rank_matrix):
    return stats.spearmanr(rank_matrix)