
import numpy as np
import RTLearner as rt
from scipy import stats
import math

class BagLearner(object):
    def __init__(self,  bags, learner, kwargs,  boost=False, verbose=False):

        self.learner = learner
        self.bags = bags
        self.kwargs = kwargs

        pass

    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        def generate_train_data(dataX, dataY):
            '''combine dataX and dataY first, preparing for random sampling at next step'''
            combined_data = np.zeros((dataX.shape[0], dataX.shape[1] + 1))
            # print combined_data
            for i in range(len(dataY)):
                data_new = np.append(dataX[i], dataY[i])
                combined_data[i] = data_new

            '''use a random 60% portion of combined dataX/dataY to make the trainX, trainY'''
            random_no = np.random.choice(combined_data.shape[0], size=int(0.6 * combined_data.shape[0]),
                                         replace=True)
            test_rows_no = np.random.choice(random_no, size=combined_data.shape[0], replace=True)
            # print ' ==========test_rows_no======'
            # print test_rows_no

            train_combined_data = []
            for j in test_rows_no:
                if len(train_combined_data) == 0:
                    train_combined_data = combined_data[j]
                else:
                    train_combined_data = np.vstack((train_combined_data, combined_data[j]))
            # print train_combined_data
            trainX = train_combined_data[:, :-1]
            trainY = train_combined_data[:, -1]

            return trainX, trainY

        def build_tree(dataX, dataY):
            global self_learners
            self_learners = []
            learner_result = []

            for i in range(0, self.bags):
                # print i
                this_learner = self.learner(**self.kwargs)
                trainX, trainY = generate_train_data(dataX, dataY)

                ''' use the learner to train, i.e. generate the tree form (or equation for the liner regression)'''
                # learner_result.append(this_learner.addEvidence(trainX, trainY)) #9:54 one row gives out matrix, not nparray
                this_learner.addEvidence(trainX, trainY)
                self_learners.append(this_learner)     # make a list of learners

            # return learner_result
        self.learner_result = build_tree(dataX, dataY)   # should be same as learner_result, is a stacked tree forms.

    def query(self,testX):
        predY = np.array([])
        # print '=======sefl_learners====\n', self_learners
        # print '=====self_learners===\n', self_learners
        # print '===rows of testX==='
        # print testX.shape[0]
        for i in range(self.bags):
            # print each_tree
            if len(predY) == 0:
                predY = np.array([self_learners[i].query(testX)])
            else:
                predY = np.vstack((predY, self_learners[i].query(testX)))
        # print '=========predY=========='
        # print predY
        # Y = np.sum(predY, axis=0) / predY.shape[0]  # for number-based, use this
        Y = stats.mode(predY, axis=0)[0]   # for classification , use this
        # print "generated Y form"
        # print len(Y)
        # print Y
        return Y

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"