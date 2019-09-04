import numpy, BagLearner, LinRegLearner
class InsaneLearner(object):
    def __init__(self, verbose=False):
        pass  # move along, these aren't the drones you're looking for
    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username
    def addEvidence(self, trainX, trainY):
        self.learners = BagLearner.BagLearner(learner = BagLearner.BagLearner, kwargs={'learner': LinRegLearner.LinRegLearner, 'kwargs': {}, 'bags': 20, 'boost': False, 'verbose':False}, bags=20, boost=False, verbose=False)
        self.learners.addEvidence(trainX,trainY)
        return self.learners
    def query(self, testX):
        predY = numpy.array([])
        for i in range(20):
            if len(predY) == 0: predY = numpy.array([self.learners.query(testX)])
            else:  predY = numpy.vstack((predY, self.learners.query(testX)))
        return numpy.sum(predY, axis=0) / predY.shape[0]
if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

