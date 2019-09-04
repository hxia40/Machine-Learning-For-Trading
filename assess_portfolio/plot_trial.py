import scipy.optimize as sco
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def f(X):
    Y = np.float32([1,2]) * X
    print Y
    print 'one iteration'

    print type(Y)


    return Y


def test_run():
    XZguess = np.float32([3,4])
    min_result = sco.minimize(f, XZguess, method = 'SLSQP', options = {'disp': True})
    print "Minima found at:"
    print min_result.x
    # print "X = {}, Y = {}, Z = {}".format(min_result.x[0], min_result.fun, min_result.x[1])
    print "end"
    #
    # Xplot = np.linspace(0.5,2.5,21)
    # Yplot = f(Xplot)
    # plt.plot(Xplot, Yplot)
    # plt.plot(min_result.x,min_result.fun,'ro')
    # plt.show()

if __name__ == "__main__":
    test_run()





