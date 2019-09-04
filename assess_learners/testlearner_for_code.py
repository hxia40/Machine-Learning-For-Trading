""" 			  		 			     			  	   		   	  			  	
Test a learner.  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import math
import sys 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.genfromtxt(inf, delimiter=',')
    # if sys.argv[1] == 'data/istanbul.csv':
    # print data

    if math.isnan(data[0, 1]) is True:  # this is to check if the first row is NaN -  if yes, ignore it
        # print data[0, 1]
        # print type(data[0, 1])
        # print 'first worked'
        data = data[1:, :]
    if math.isnan(data[1, 0]) is True:  # this is to check if the first column is NaN -  if yes, ignore it
        # print data[1, 0]
        # print type(data[1, 0])
        # print 'second worked'
        data = data[:, 1:]
    # print 'ddddddddddddddddddddata'
    # print data

    # compute how much of the data is training and testing
    if len(data.shape) == 1:
        train_rows = 1
        test_rows = 0
        Xtrain = data[0:-1]
        Ytrain = data[-1]
        Xtest = Xtrain
        Ytest = Ytrain
    else:
        train_rows = int(0.6* data.shape[0])
        test_rows = data.shape[0] - train_rows
        # separate out training and testing data
        Xtrain = data[:train_rows,0:-1]
        Ytrain = data[:train_rows,-1]
        Xtest = data[train_rows:,0:-1]
        Ytest = data[train_rows:,-1]
 			  		 			     			  	   		   	  			  	
    # print Xtest.shape
    # print Ytest.shape



    print 'create a Linear Regression learner and train it'
    import LinRegLearner as lrl

    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    learner.addEvidence(Xtrain, Ytrain) # train it
    print learner.author()

    # evaluate out of sample
    Y = learner.query(Xtest)  # get the predictions
    rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytest)
    print "corr: ", c[0, 1]

    # evaluate in sample
    Y = learner.query(Xtrain)  # get the predictions
    rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])

    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytrain)
    print "corr: ", c[0, 1]



    print 'create a DT learner and train it'
    import DTLearner as dt

    learner = dt.DTLearner(leaf_size=1, verbose=False)  # constructor
    learner.addEvidence(Xtrain, Ytrain)  # training step
    print learner.author()
    Y = learner.query(Xtest)  # get the predictions
    rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    print
    print "DT Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytest)
    print "corr: ", c[0, 1]

    Y = learner.query(Xtrain)  # query
    rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    print
    print "DT In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytrain)
    print "corr: ", c[0, 1]


    print 'create a RT learner and train it'
    import RTLearner as rt

    learner = rt.RTLearner(leaf_size=1, verbose=False)  # constructor
    learner.addEvidence(Xtrain, Ytrain)  # training step
    print learner.author()
    Y = learner.query(Xtest)  # query
    rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    print
    print "RT Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytest)
    print "corr: ", c[0, 1]

    Y = learner.query(Xtrain)  # query
    rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    print
    print "RT In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytrain)
    print "corr: ", c[0, 1]

    print 'create a bag learner'

    import BagLearner as bl
    learner = bl.BagLearner(learner=dt.DTLearner, kwargs={}, bags=3, boost=False, verbose=False)
    # learner = bl.BagLearner(learner=3, kwargs={}, bags=20, boost=False, verbose=False)
    learner.addEvidence(Xtrain, Ytrain)
    print learner.author()
    Y = learner.query(Xtest)
    rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    print
    print "BAG Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytest)
    print "corr: ", c[0, 1]

    Y = learner.query(Xtrain)  # query
    rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    print
    print "BAG In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytrain)
    print "corr: ", c[0, 1]

    print 'create a insane learner'

    import InsaneLearner as it

    learner = it.InsaneLearner(verbose=False)  # constructor
    learner.addEvidence(Xtrain, Ytrain)  # training step
    Y = learner.query(Xtest)  # query

    rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    print
    print "INSANE Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytest)
    print "corr: ", c[0, 1]

    Y = learner.query(Xtrain)  # query
    rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    print
    print "INSANE In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(Y, y=Ytrain)
    print "corr: ", c[0, 1]

