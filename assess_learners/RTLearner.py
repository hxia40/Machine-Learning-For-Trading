import numpy as np

class RTLearner(object):
    def __init__(self, leaf_size, verbose = False):
        self.leaf_size = leaf_size
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'hxia40' # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        leafsize = self.leaf_size

        def build_tree(dataX, dataY):

            '''if dataY is a number, just return the tree with that number.'''
            if np.ndim(dataY) == 0:
                return np.array([[-1, dataY, -1, -1]])
            '''the frist two return cases in class'''
            if dataX.shape[0] <= leafsize:
                # print '~~~~~~called single line return~~~~~~'
                # print [-1, dataY[0], -2, -2]
                return np.matrix([[-1, dataY[0], -1, -1]])
            if len(set(dataY)) == 1:
                # print '~~~~~~called same line return~~~~~~'
                # print [-1, dataY[0], -2, -2]
                return np.matrix([[-1, dataY[0], -1, -1]])
            else:
                '''determine RANDOM feature i to split on:'''
                i = np.random.randint(dataX.shape[1])
                # print '===i==='
                # print i
                '''use the i to do the calculating works'''
                # rand1 = np.random.randint(dataX.shape[0])
                # rand2 = np.random.randint(dataX.shape[0])
                rand1 = np.random.randint(dataX.shape[0])
                rand2 = np.random.randint(dataX.shape[0])
                # while rand1 == rand2 and (rand1 == 0 or rand1 == dataX.shape[0] - 1):
                #     rand1 = np.random.randint(dataX.shape[0])
                #     rand2 = np.random.randint(dataX.shape[0])
                # print 'rand 1 and rand 2'
                # print rand1
                # print rand2
                SplitVal = (dataX[rand1, i] + dataX[rand2, i])/2

                dataX_left = dataX[dataX[:, i] <= SplitVal]
                dataY_left = dataY[dataX[:, i] <= SplitVal]
                dataX_right = dataX[dataX[:, i] > SplitVal]
                dataY_right = dataY[dataX[:, i] > SplitVal]

                ''' need to consider a side case: sometimes several rows have exact i value. In this case,
                all rows could stay on the same (left) side of the median, generating an empty right tree.
                THus, if this happens, we should directly return the left tree as a leaf '''

                if dataX_right.shape[0] == 0:
                    # print 'it happens!!!!!'
                    return np.matrix([-1, dataY_left.mean(), -1, -1])

                '''combinging root,lefttree, and righttree together'''

                lefttree = build_tree(dataX_left, dataY_left)
                righttree = build_tree(dataX_right, dataY_right)
                root = np.matrix([i, SplitVal, 1, lefttree.shape[0] + 1])
                the_arr_for_return = np.concatenate((root, lefttree, righttree), axis=0)

                return the_arr_for_return

        self.Dtree = build_tree(dataX, dataY)
        # print '======the returned random tree array======'
        # print build_tree(dataX, dataY)
        # # print build_tree(dataX, dataY).shape
        # # return build_tree(dataX, dataY)



    def query(self,testX):
        predY = np.array([])

        for j in range(testX.shape[0]):
            row_in_dtree = 0  #tracks which row of the decision tree that we are checking
            trait_no = int(self.Dtree[0, 0])
            split_value = self.Dtree[0, 1]
            # print 'two stuffs'
            # print trait_no
            # print split_value
            while trait_no != -1:
                # print 'the comparable'
                # print testX[j, trait_no]

                if testX[j, trait_no] <= split_value:  # if this row of the decision tree points to left tree, then move left
                    row_in_dtree = row_in_dtree + 1
                    trait_no = int(self.Dtree[row_in_dtree, 0])
                    split_value = self.Dtree[row_in_dtree, 1]
                elif testX[j, trait_no] > split_value:  # if this row of the decision tree points to right tree, then move right
                    row_in_dtree = int(row_in_dtree + self.Dtree[row_in_dtree, 3])
                    trait_no = int(self.Dtree[row_in_dtree, 0])
                    split_value = self.Dtree[row_in_dtree, 1]
                else:
                    print 'edge case happens!!!!'
            if trait_no == -1:
                predY = np.append(predY, split_value)  # if this row of the decision tree is a leaf, then the predicted Y should be the SplitValue
        return predY


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"