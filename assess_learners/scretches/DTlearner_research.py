import numpy as np


data = np.array([
                 [ 1.0, 2.0, 6.0, 4.0, 5.0, 6.0, 7.0, 8.0],
                 [ 2.0, 3.3, 8.0, 5.1, 6.9, 7.3, 8.0, 9.3],
                 [-1.0,-2.0,-3.0,-4.0,-5.0,-6.0,-7.0,-8.0]])

dataX = data[:, :-1]
dataY = data[:, -1]
# print '===dataX==='
# print dataX
# print '===dataY==='
# print dataY

def build_tree(dataX, dataY):

    if dataX.shape[0] == 1:
        print '~~~~~~called single line return~~~~~~'
        # print [-1, dataY[0], -2, -2]
        return np.array([[-1, dataY[0], -2, -2]])
    if len(set(dataY)) == 1:
        print '~~~~~~called same line return~~~~~~'
        # print [-1, dataY[0], -2, -2]
        return np.array([[-1, dataY[0], -2, -2]])
    else:
        '''determine best feature i to split on:'''
        corr_array = np.array([])
        for counter in range(dataX.shape[1]):
            # print counter
            corr = np.corrcoef(dataX[:, counter], y=dataY)[0, 1]
            # print corr
            abs_corr = np.absolute(corr)
            # print abs_corr
            corr_array = np.append(corr_array, abs_corr)
            ''' a shorter verson'''
            # corr_array = np.append(corr_array, np.absolute(np.corrcoef(dataX[:, a], y=dataY))[0,1])
        print '===corr_array==='
        print corr_array
        i = np.argmax(corr_array)  # here comes the i used below
        print '===i==='
        print i
        '''use the i to do the calculating works'''
        SplitVal = np.median(dataX[:, i])
        print '===SplitVal==='
        print SplitVal
        lefttree = build_tree(dataX[dataX[:, i] <= SplitVal], dataY[dataX[:, i] <= SplitVal]) # the 2nd argument is the last column of first argument
        print '===lefttree==='
        print lefttree
        # print type(lefttree)
        print lefttree.shape

        righttree = build_tree(dataX[dataX[:, i] > SplitVal], dataY[dataX[:, i] > SplitVal])
        print '===righttree==='
        print righttree
        # print type(righttree)
        print righttree.shape
        # if lefttree.ndim == 1:
        #     root = np.array([i, SplitVal, 1, 1 + 1])
        # else:
        root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]])

        print '===root==='
        print root
        print root.shape
        # print type(root)

        root = np.append(root,lefttree)
        root = np.append(root,righttree)
        root = root.reshape(-1,4)
        # # the_arr_for_return = np.stack(the_arr_for_return, righttree)
        print '===the return root==='
        print root
        return root

if __name__=="__main__":
    print '======main======'
    build_tree(dataX, dataY)

