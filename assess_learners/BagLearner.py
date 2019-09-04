import LinRegLearner as lrl
import numpy as np
import DTLearner as dt
import RTLearner as rt
import InsaneLearner as it
import math

class BagLearner(object):
    def __init__(self,  bags, learner, kwargs,  boost=False, verbose=False):
        # print '=======gib learner!!!==='
        # print learner
        # if learner != dt.DTLearner and learner != rt.RTLearner and learner!= lrl.LinRegLearner and learner!= BagLearner:
        #     print 'ibg learner works!=!=!'
        #
        #     # learner = BagLearner(learner = BagLearner, kwargs={'learner': lrl.LinRegLearner, 'kwargs': {}, 'bags': 20, 'boost': False, 'verbose':False}, bags=20, boost=False, verbose=False)
        #     learner = it.InsaneLearner
        #     # kwargs = {'leaf_size': 1}
        #     print 'herrrrre comes our self.learner!!'
        #     print learner
        #     print kwargs
        self.learner = learner
        self.bags = bags
        self.kwargs = kwargs


        # for key, value in kwargs.items():
        #     self.kwargs[key] = value
        # print self.kwargs

        pass  # move along, these aren't the drones you're looking for

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
            self.learners = []
            learner_result = []

            for i in range(0, self.bags):
                this_learner = self.learner(**self.kwargs)
                trainX, trainY = generate_train_data(dataX, dataY)

                ''' use the learner to train, i.e. generate the tree form (or equation for the liner regression)'''

                learner_result.append(this_learner.addEvidence(trainX, trainY))  #9:54 one row gives out matrix, not nparray
                self.learners.append(this_learner)     # make a list of learners

            # print '===bag learner result===='
            # print learner_result
            # print type(learner_result)
            return learner_result

        self.learner_result = build_tree(dataX, dataY)   # should be same as learner_result, is a stacked tree forms.
        # print '======self.learner_result===='
        # print self.learner_result
        # print type(self.learner_result)

    def query(self,testX):
        predY = np.array([])
        # print '===rows of testX==='
        # print testX.shape[0]
        for i in range(self.bags):
            # print each_tree
            if len(predY) == 0:
                predY = np.array([self.learners[i].query(testX)])
            else:
                predY = np.vstack((predY, self.learners[i].query(testX)))
        # print '=========predY=========='
        # print predY
        Y = np.sum(predY, axis=0) / predY.shape[0]
        # print "generated Y form"
        # print len(Y)
        # print Y
        return Y

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"