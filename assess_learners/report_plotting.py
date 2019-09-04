import numpy as np
import DTLearner as dt
import sys
import math
import matplotlib.pyplot as plt


if __name__=="__main__":
    # if len(sys.argv) != 2:
    #     print "Usage: python testlearner.py <filename>"
    #     sys.exit(1)
    inf = open('Data/simple.csv')
    data = np.genfromtxt(inf, delimiter=',')
    # if sys.argv[1] == 'data/istanbul.csv':
    # print data

    if math.isnan(data[0, 1]) is True:  # this is to check if the first row is NaN -  if yes, ignore it
        data = data[1:, :]
    if math.isnan(data[1, 0]) is True:  # this is to check if the first column is NaN -  if yes, ignore it
        data = data[:, 1:]

    np.random.shuffle(data)

    if len(data.shape) == 1:
        train_rows = 1
        test_rows = 0
        Xtrain = data[0:-1]
        Ytrain = data[-1]
        Xtest = Xtrain
        Ytest = Ytrain
    else:
        train_rows = int(0.6 * data.shape[0])
        test_rows = data.shape[0] - train_rows
        # separate out training and testing data
        Xtrain = data[:train_rows, 0:-1]
        Ytrain = data[:train_rows, -1]
        Xtest = data[train_rows:, 0:-1]
        Ytest = data[train_rows:, -1]

    x_axis = []
    y_axis_in = []
    y_axis_out = []
    in_out_difference = []

    for i in range(100):
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


    # print 'dataz'
    # print x_axis
    # print y_axis_in
    # print y_axis_out

    '''plot for rmse vs leafsize'''

    plt.plot(x_axis, y_axis_in, label='In sample')
    plt.plot(x_axis, y_axis_out, label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('RMSE')
    plt.xlabel('Leaf size')
    plt.grid()
    # plt.title('Over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure1.png')
    # plt.show()
    plt.clf()

    '''plot for in-out-sample difference vs leafsize'''

    plt.plot(x_axis, in_out_difference, label='In sample RMSE - Out of sample RMSE')
    # plt.plot(x_axis, y_axis_out, label='Out of sample')
    # plt.gcf().subplots_adjust
    plt.ylabel('In/Out of Sample Difference')
    plt.xlabel('Leaf size')
    plt.grid()
    # plt.title('Over fitting')
    plt.legend()
    # plt.plot(range(252), port_val, label='xyz')
    plt.savefig('Figure4.png')
    # plt.show()
    plt.clf()
