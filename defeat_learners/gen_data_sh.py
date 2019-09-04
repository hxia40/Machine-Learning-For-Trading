"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math
import random

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4DT(seed=1489683273):

    """
    random.seed(seed)
    row = random.randint(10,1000)  # number of lines in dataX
    column = random.randint (2, 1000) # number of columns in dataX
    print 'dataX includes: ', row, ' lines, ', column, ' columns.'
    """

    np.random.seed(seed)
    row = 100
    column = 10
    X = np.zeros((row, column))
    for i in range(row):
        X[i,:] = np.random.random(column)*10
    # print 'X: ', X
    # Y = np.random.random(size=(100,)) * 200 - 100
    Y = X[:,0] + np.sin(X[:,1]) + np.cos(X[:, 2])
    for j in range (3, column):
        Y = Y+ X[:,j]**(j-2)
    return X, Y

def best4LinReg(seed=1489683273):

    """
    random.seed(seed)
    row = random.randint(10, 1000)  # number of lines in dataX
    column = random.randint(2, 1000)  # number of columns in dataX
    """

    row = 100
    column = 10
    np.random.seed(seed)
    X = np.random.rand(row, column)
    # print X
    Y = np.zeros(row)
    for i in range (column):
        Y = Y + X[:, i]*i
    # print Y
    return X, Y

def author():
    return 'shuang379' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
