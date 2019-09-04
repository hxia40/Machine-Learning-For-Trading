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
import matplotlib.pyplot as plt
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as it
import time
 			  		 			     			  	   		   	  			  	
if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.genfromtxt(inf, delimiter=',')
    # if sys.argv[1] == 'data/istanbul.csv':
    # print data

    if math.isnan(data[0, 1]) is True:  # this is to check if the first row is NaN -  if yes, ignore it
        data = data[1:, :]
    if math.isnan(data[1, 0]) is True:  # this is to check if the first column is NaN -  if yes, ignore it
        data = data[:, 1:]

    #shuffle the data 20 times and get its average
    total_x = []
    total_y_in = []
    total_y_out = []
    np.random.seed(123)
    # for n in range(20):
    np.random.shuffle(data)

    # compute how much of the data is training and testing

    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows
    # separate out training and testing data
    Xtrain = data[:train_rows,0:-1]
    Ytrain = data[:train_rows,-1]
    Xtest = data[train_rows:,0:-1]
    Ytest = data[train_rows:,-1]

    '''calculate for Quesiton 1: rmse vs leafsize'''
    x_axis = []
    y_axis_in = []
    y_axis_out = []
    in_out_difference = []

    for i in range(1, 101):
        learner = dt.DTLearner(leaf_size=i, verbose=False)  # constructor
        learner.addEvidence(Xtrain, Ytrain)  # training step

        Y_in = learner.query(Xtrain)  # get the predictions
        Y_out = learner.query(Xtest)
        rmse_in = math.sqrt(((Ytrain - Y_in) ** 2).sum() / Ytrain.shape[0])
        rmse_out = math.sqrt(((Ytest - Y_out) ** 2).sum() / Ytest.shape[0])
        each_difference = rmse_in - rmse_out
        x_axis.append(i)
        y_axis_in.append(rmse_in)
        y_axis_out.append(rmse_out)
        in_out_difference.append(each_difference)

    '''plot for Quesiton 1: rmse vs leafsize'''

    plt.plot(x_axis[:100], y_axis_in[:100], label='In sample')
    plt.plot(x_axis[:100], y_axis_out[:100], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q1: Effect of leaf size on over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 1d.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:50], y_axis_in[:50], label='In sample')
    plt.plot(x_axis[:50], y_axis_out[:50], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q1: Effect of leaf size on over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 1c.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:20], y_axis_in[:20], label='In sample')
    plt.plot(x_axis[:20], y_axis_out[:20], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q1: Effect of leaf size on over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 1b.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:10], y_axis_in[:10], label='In sample')
    plt.plot(x_axis[:10], y_axis_out[:10], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q1: Effect of leaf size on over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 1a.png')
    # plt.show()
    plt.clf()

    '''plot for Quesiton 2: bagging to elimate overfitting - 1 run per leaf'''

    x_axis = []
    y_axis_in = []
    y_axis_out = []
    in_out_difference = []

    for i in range(1, 101):
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={'leaf_size': i}, bags=20, boost=False,
                                verbose=False)  # constructor
        learner.addEvidence(Xtrain, Ytrain)  # training step

        Y_in = learner.query(Xtrain)  # get the predictions
        Y_out = learner.query(Xtest)
        rmse_in = math.sqrt(((Ytrain - Y_in) ** 2).sum() / Ytrain.shape[0])
        rmse_out = math.sqrt(((Ytest - Y_out) ** 2).sum() / Ytest.shape[0])
        each_difference = rmse_in - rmse_out
        x_axis.append(i)
        y_axis_in.append(rmse_in)
        y_axis_out.append(rmse_out)
        in_out_difference.append(each_difference)

    plt.plot(x_axis[:100], y_axis_in[:100], label='In sample')
    plt.plot(x_axis[:100], y_axis_out[:100], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 2d.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:50], y_axis_in[:50], label='In sample')
    plt.plot(x_axis[:50], y_axis_out[:50], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 2c.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:20], y_axis_in[:20], label='In sample')
    plt.plot(x_axis[:20], y_axis_out[:20], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 2b.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:10], y_axis_in[:10], label='In sample')
    plt.plot(x_axis[:10], y_axis_out[:10], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 2a.png')
    # plt.show()
    plt.clf()

    '''plot for Question 3: DT Learner vs. RT Learner - Mean absolute error (MAE) and running time'''

    x_axis = []
    y_axis_in_DT = []
    y_axis_out_DT = []
    y_axis_in_RT = []
    y_axis_out_RT = []
    DT_time = []
    RT_time = []
    # in_out_difference = []

    for i in range(1, 101):  # different leaf_size from 1 to 101
        startDT = time.time()
        learnerQ3DT = dt.DTLearner(leaf_size=i, verbose=False)  # constructor
        learnerQ3DT.addEvidence(Xtrain, Ytrain)  # training step
        endDT = time.time()

        startRT = time.time()
        learnerQ3RT = rt.RTLearner(leaf_size=i, verbose=False)  # constructor
        learnerQ3RT.addEvidence(Xtrain, Ytrain)
        endRT = time.time()

        Y_in_DT = learnerQ3DT.query(Xtrain)  # get the predictions
        Y_out_DT = learnerQ3DT.query(Xtest)

        Y_in_RT = learnerQ3RT.query(Xtrain)  # get the predictions
        Y_out_RT = learnerQ3RT.query(Xtest)

        mae_in_DT = (np.absolute(Ytrain - Y_in_DT)).sum() / Ytrain.shape[0]
        mae_out_DT = (np.absolute(Ytest - Y_out_DT)).sum() / Ytest.shape[0]

        mae_in_RT = (np.absolute(Ytrain - Y_in_RT)).sum() / Ytrain.shape[0]
        mae_out_RT = (np.absolute(Ytest - Y_out_RT)).sum() / Ytest.shape[0]

        # each_difference = rmse_in - rmse_out
        x_axis.append(i)
        y_axis_in_DT.append(mae_in_DT)
        y_axis_out_DT.append(mae_out_DT)
        y_axis_in_RT.append(mae_in_RT)
        y_axis_out_RT.append(mae_out_RT)
        DT_time.append(endDT - startDT)
        RT_time.append(endRT - startRT)
        # in_out_difference.append(each_difference)

    plt.plot(x_axis[:50], DT_time[:50], label='Decision Tree Learner')
    plt.plot(x_axis[:50], RT_time[:50], label='Random Tree Learner')
    # plt.gcf().subplots_adjust
    plt.ylabel('Running time')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. running time')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 5a.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:100], DT_time[:100], label='Decision Tree Learner')
    plt.plot(x_axis[:100], RT_time[:100], label='Random Tree Learner')
    # plt.gcf().subplots_adjust
    plt.ylabel('Running time')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. running time')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 5b.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:50], y_axis_in_DT[:50], label='In sample')
    plt.plot(x_axis[:50], y_axis_out_DT[:50], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('MAE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. MAE using DT Learner')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 4a.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:100], y_axis_in_DT[:100], label='In sample')
    plt.plot(x_axis[:100], y_axis_out_DT[:100], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('MAE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. MAE using DT Learner')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 4b.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:50], y_axis_in_RT[:50], label='In sample')
    plt.plot(x_axis[:50], y_axis_out_RT[:50], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('MAE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. MAE using RT Learner')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 4c.png')
    # plt.show()
    plt.clf()

    plt.plot(x_axis[:100], y_axis_in_RT[:100], label='In sample')
    plt.plot(x_axis[:100], y_axis_out_RT[:100], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('MAE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Leaf size vs. MAE using RT Learner')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 4d.png')
    # plt.show()
    plt.clf()

    # plt.plot(x_axis[:50], y_axis_in_DT[:50], label='DT in sample')
    # plt.plot(x_axis[:50], y_axis_out_DT[:50], label='DT out of sample')
    # plt.plot(x_axis[:50], y_axis_in_RT[:50], label='RT in sample')
    # plt.plot(x_axis[:50], y_axis_out_RT[:50], label='RT out of sample')
    # # plt.gcf().subplots_adjust
    # plt.ylabel('MAE')
    # plt.xlabel('Leaf size')
    # plt.grid()
    # plt.title('Leaf size vs. MAE using both Learners')
    # plt.legend()
    # # plt.plot(range(252), port_val, label='xyz')
    # plt.savefig('Figure3_both_50.png')
    # # plt.show()
    # plt.clf()
    #
    # plt.plot(x_axis[:100], y_axis_in_DT[:100], label='DT in sample')
    # plt.plot(x_axis[:100], y_axis_out_DT[:100], label='DT out of sample')
    # plt.plot(x_axis[:100], y_axis_in_RT[:100], label='RT in sample')
    # plt.plot(x_axis[:100], y_axis_out_RT[:100], label='RT out of sample')
    # # plt.gcf().subplots_adjust
    # plt.ylabel('MAE')
    # plt.xlabel('Leaf size')
    # plt.grid()
    # plt.title('Leaf size vs. MAE using both Learners')
    # plt.legend()
    # # plt.plot(range(252), port_val, label='xyz')
    # plt.savefig('Figure3_both_100.png')
    # # plt.show()
    # plt.clf()


    '''plot for Quesiton 2: bagging to elimate overfitting - 20 runs per leaf'''

    total_x_axis = []
    total_y_axis_in = []
    total_y_axis_out = []

    for i in range(1, 101):
        # print "i =", i
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={'leaf_size': i}, bags=20, boost=False, verbose=False)  # constructor
        x_axis = []
        y_axis_in = []
        y_axis_out = []
        in_out_difference = []

        for n in range(20):  # n runs for each leaf size
            # print 'n=', n
            learner.addEvidence(Xtrain, Ytrain)  # training step
            Y_in = learner.query(Xtrain)  # get the predictions
            Y_out = learner.query(Xtest)
            rmse_in = math.sqrt(((Ytrain - Y_in) ** 2).sum() / Ytrain.shape[0])
            rmse_out = math.sqrt(((Ytest - Y_out) ** 2).sum() / Ytest.shape[0])
            each_difference = rmse_in - rmse_out
            x_axis.append(i)
            y_axis_in.append(rmse_in)
            y_axis_out.append(rmse_out)
            in_out_difference.append(each_difference)

        total_x_axis.append(x_axis)
        total_y_axis_in.append(y_axis_in)
        total_y_axis_out.append(y_axis_out)

    xx = np.mean(np.array(total_x_axis).T, axis = 0)
    yin = np.mean(np.array(total_y_axis_in).T, axis=0)
    yout = np.mean(np.array(total_y_axis_out).T, axis=0)

    plt.plot(xx[:100], yin[:100], label='In sample')
    plt.plot(xx[:100], yout[:100], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 3d')
    # plt.show()
    plt.clf()

    plt.plot(xx[:50], yin[:50], label='In sample')
    plt.plot(xx[:50], yout[:50], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 3c')
    # plt.show()
    plt.clf()

    plt.plot(xx[:20], yin[:20], label='In sample')
    plt.plot(xx[:20], yout[:20], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 3b')
    # plt.show()
    plt.clf()

    plt.plot(xx[:10], yin[:10], label='In sample')
    plt.plot(xx[:10], yout[:10], label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    plt.title('Q2: Effect of bagging on over fitting (bags = 20)')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure 3a')
    # plt.show()
    plt.clf()



    '''below are old testing codes, they do not plot anything'''

    # print 'create a Linear Regression learner and train it'

    #
    # learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    # learner.addEvidence(Xtrain, Ytrain) # train it
    # print learner.author()
    #
    # # evaluate out of sample
    # Y = learner.query(Xtest)  # get the predictions
    # rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    # print
    # print "Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytest)
    # print "corr: ", c[0, 1]
    #
    # # evaluate in sample
    # Y = learner.query(Xtrain)  # get the predictions
    # rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    #
    # print
    # print "In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytrain)
    # print "corr: ", c[0, 1]
    #
    #
    #
    # print 'create a DT learner and train it'

    #
    # learner = dt.DTLearner(leaf_size=1, verbose=False)  # constructor
    # learner.addEvidence(Xtrain, Ytrain)  # training step
    # print learner.author()
    # Y = learner.query(Xtest)  # get the predictions
    # rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    # print
    # print "DT Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytest)
    # print "corr: ", c[0, 1]
    #
    # Y = learner.query(Xtrain)  # query
    # rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    # print
    # print "DT In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytrain)
    # print "corr: ", c[0, 1]
    #
    #
    # print 'create a RT learner and train it'

    #
    # learner = rt.RTLearner(leaf_size=1, verbose=False)  # constructor
    # learner.addEvidence(Xtrain, Ytrain)  # training step
    # print learner.author()
    # Y = learner.query(Xtest)  # query
    # rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    # print
    # print "RT Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytest)
    # print "corr: ", c[0, 1]
    #
    # Y = learner.query(Xtrain)  # query
    # rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    # print
    # print "RT In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytrain)
    # print "corr: ", c[0, 1]
    #
    # print 'create a bag learner'
    #

    # learner = bl.BagLearner(learner=dt.DTLearner, kwargs={}, bags=3, boost=False, verbose=False)
    # # learner = bl.BagLearner(learner=3, kwargs={}, bags=20, boost=False, verbose=False)
    # learner.addEvidence(Xtrain, Ytrain)
    # print learner.author()
    # Y = learner.query(Xtest)
    # rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    # print
    # print "BAG Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytest)
    # print "corr: ", c[0, 1]
    #
    # Y = learner.query(Xtrain)  # query
    # rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    # print
    # print "BAG In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytrain)
    # print "corr: ", c[0, 1]
    #
    # print 'create a insane learner'
    #

    #
    # learner = it.InsaneLearner(verbose=False)  # constructor
    # learner.addEvidence(Xtrain, Ytrain)  # training step
    # Y = learner.query(Xtest)  # query
    #
    # rmse = math.sqrt(((Ytest - Y) ** 2).sum() / Ytest.shape[0])
    # print
    # print "INSANE Out of sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytest)
    # print "corr: ", c[0, 1]
    #
    # Y = learner.query(Xtrain)  # query
    # rmse = math.sqrt(((Ytrain - Y) ** 2).sum() / Ytrain.shape[0])
    # print
    # print "INSANE In sample results"
    # print "RMSE: ", rmse
    # c = np.corrcoef(Y, y=Ytrain)
    # print "corr: ", c[0, 1]
    #
