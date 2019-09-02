'''Fit a line to a given set of data points using optimization'''

import scipy.optimize as sco
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def error(line, data):
    """Compute error between given line model and observed data

    Parameters
    ----------
    line: tuple/list/array (C0, C1), where C0 is the slope and C1 is the Y-intercept
    data: 2D array where eavh row is a point (x,y)

    Returns error as a single real value
    """
    #Metric: Sum of squared Y-axis differences
    err = np.sum((data[:,1]-(line[0]*data[:,0]+line[1]))**2)
    return err

def fit_line(data, error_func):
    '''fit a line to given data, using a supplied error function

    parameters
    ----------
    data: 2D array where each row is a point (X0, Y)
    error_func: function that computes the error between a line and observed data

    returns line that minimizes the error function
    '''
    #Generate initial guess for the line model
    l = np.float32([0,np.mean(data[:,1])])  #slope =  0, intercept = mean(y values)
    print "l"
    print l
    print type(l)

    #plot initial guess (optional)
    x_ends = np.float32([5,-5])
    plt.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth = 2.0, label = 'Initial guess')

    # call optimizer to minimize error function
    result = sco.minimize(error_func, l, args=(data,), method = 'SLSQP', options = {'disp' :True})
    print 'ddfdsfsdf'
    print type(result.x)
    print result.x
    print type(l)
    print l
    return result.x

def test_run():
    #define the original line
    l_orig = np.float32([4,2])
    print "Original line: C0 = {}. C1 = {}". format(l_orig[0],l_orig[1])
    Xorig = np.linspace(0,10,21)
    Yorig = l_orig[0] * Xorig + l_orig[1]
    plt.plot(Xorig, Yorig, 'b--', linewidth = 2.0, label = "Original line")

    #Generate noisy data points
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, Yorig.shape)
    data = np.asarray([Xorig, Yorig + noise]).T
    plt.plot(data[:,0], data[:,1],'go', label = 'Data points')

    #Try to fit a line to this data
    l_fit = fit_line(data, error)
    print "Fitted line: C0 = {}, C1 = {}".format(l_fit[0],l_fit[1])
    plt.plot(data[:,0],l_fit[0]* data[:,0]+ l_fit[1], 'r--', linewidth = 2.0, label = 'fitted line')

    #Add legend and show plot
    plt.legend()
    plt.show()

if __name__ == "__main__":
    test_run()

