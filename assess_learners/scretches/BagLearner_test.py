# def greet_me(**kwargs):
#     for key, value in kwargs.items():
#         print("{0} = {1}".format(key, value))
#
# greet_me(name="yasoob", qcq = 'efe')

import LinRegLearner as lrl
import numpy as np
import DTLearner as dt
import math

class BagLearner(object):
    def __init__(self, learner, bags,**kwargss):
        self.learner = learner
        self.bags = bags
        self.kwargs = kwargss
        # for key, value in kwargs.items():
        #     self.kwargs[key] = value
        # print self.kwargs

        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):

        bag_num = self.bags
        print bag_num
        learners = []

        kwargs = {'leaf_size': 10}
        print kwargs
        # for i in range(0, bag_num):
        #     learners.append(self.learner(**kwargs))
        learners = dt.DTLearner(leaf_size=1, verbose=False)  # constructor
        Y = learners.query(dataX)  # get the predictions
        rmse = math.sqrt(((dataY - Y) ** 2).sum() / dataY.shape[0])
        print
        print "Out of sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(Y, y=dataY)
        print "corr: ", c[0, 1]
        # print learners
        # print dataX
        # print dataY
        # print '===try to learn==='

        # learner.addEvidence(dataX, dataY)

data = np.array([[ 1.0, 2.0, 6.0, 4.0, 5.0, 6.0, 7.0, 8.0],
                 [ 2.0, 3.3, 8.0, 5.1, 6.9, 7.3, 8.0, 9.3],
                 [-1.0,-2.0,-3.0,-4.0,-5.0,-6.0,-7.0,-8.0]])
data1 = data
dataX = data[:, :-1]
dataY = data[:, -1]

learner = BagLearner(learner = dt.DTLearner,  bags = 10, kwargs = {}) # create a LinRegLearner

learner.addEvidence(dataX, dataY) # train it



# print rand2

# class LinRegLearner(object):
#
#     def __init__(self, verbose=False):
#         self.calculation = new
#         pass  # move along, these aren't the drones you're looking for
#     def calculation(self, array1):
#         new = array1 * 2
#
#
#     def query(self,arrayX):
#         xyz = self.new(arrayX)
#         print 'xyz'
#         print xyz
#
#     if __name__ == "__main__":
#         query(a)



