import numpy as np

def kMedoids(distance_matrix, k, tmax=100):
    # determine dimensions of distance matrix D
    n = np.shape(distance_matrix)[0]

    if k > n:
        raise Exception('too many medoids')
    
    # randomly initialize an array of k medoid indices
    medoids = np.arange(n)
    np.random.shuffle(medoids)
    medoids = np.sort(medoids[:k])

    # create a copy of the array of medoid indices
    newMedoids = np.copy(medoids)

    # initialize a dictionary to represent clusters
    clusters = {}
    labels = np.zeros(n)
    
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        labels = np.argmin(distance_matrix[:,medoids], axis=1)
        for label in range(k):
            clusters[label] = np.where(labels == label)[0]
            
            J = np.mean(distance_matrix[np.ix_(clusters[label], clusters[label])], axis = 1)
            j = np.argmin(J)
            newMedoids[label] = clusters[labels][j]
        np.sort(newMedoids)
        # check for convergence
        if np.array_equal(medoids, newMedoids):
            break
        medoids = np.copy(newMedoids)
    
    labels = np.argmin(distance_matrix[:, medoids], axis = 1)    
    # return results
    return medoids, labels