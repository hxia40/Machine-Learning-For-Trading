import numpy as np

class DTLearner(object):
    def __init__(self, verbose = False):
        pass # move along, these aren't the drones you're looking for
    def author(self):
        return 'hxia40' # replace tb34 with your Georgia Tech username

    #Decision TreeAlgorithm (JR Quinlan)

    # def addEvidence(self, dataX, dataY):
    #     """
    #     @summary: Add training data to learner
    #     @param dataX: X values of data to add
    #     @param dataY: the Y training values
    #     """
    #     # slap on 1s column so linear regression finds a constant term
    #     newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
    #     newdataX[:,0:dataX.shape[1]]=dataX
    #     # build and save the model
    #     self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)

    def addEvidence(self, dataX, dataY):

        def build_tree(dataX, dataY):
            if np.ndim(dataY) == 0:
                return np.array([[-1, dataY, -1, -1]])
            if dataX.shape[0] == 1:
                # print '~~~~~~called single line return~~~~~~'
                # print [-1, dataY[0], -2, -2]
                return np.array([[-1, dataY[0], -1, -1]])
            if len(set(dataY)) == 1:
                # print '~~~~~~called same line return~~~~~~'
                # print [-1, dataY[0], -2, -2]
                return np.array([[-1, dataY[0], -1, -1]])
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
                # print '===corr_array==='
                # print corr_array
                i = np.argmax(corr_array)  # here comes the i used below
                # print '===i==='
                # print i
                '''use the i to do the calculating works'''
                SplitVal = np.median(dataX[:, i])
                # print '===SplitVal==='
                # print SplitVal
                lefttree = build_tree(dataX[dataX[:, i] <= SplitVal], dataY[dataX[:, i] <= SplitVal])  # the 2nd argument is the last column of first argument
                # print '===lefttree==='
                # print lefttree
                # print type(lefttree)
                # print lefttree.shape

                righttree = build_tree(dataX[dataX[:, i] > SplitVal], dataY[dataX[:, i] > SplitVal])
                # print '===righttree==='
                # print righttree
                # print type(righttree)
                # print righttree.shape
                # if lefttree.ndim == 1:
                #     root = np.array([i, SplitVal, 1, 1 + 1])
                # else:
                root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]])

                # print '===root==='
                # print root
                # print root.shape
                # print type(root)
                the_arr_for_return = np.concatenate((root, lefttree, righttree), axis=0)

                # root = np.append(root, lefttree)
                # root = np.append(root, righttree)
                # root = root.reshape(-1, 4)

                return the_arr_for_return

        """ 			  		 			     			  	   		   	  			  	
                @summary: Add training data to learner 			  		 			     			  	   		   	  			  	
                @param dataX: X values of data to add 			  		 			     			  	   		   	  			  	
                @param dataY: the Y training values 			  		 			     			  	   		   	  			  	
                """
        # slap on 1s column so linear regression finds a constant term
        # newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        # newdataX[:, 0:dataX.shape[1]] = dataX
        # build and save the model
        # print build_tree(newdataX, dataY)
        # return build_tree(newdataX, dataY)
        print '======the returned tree array======'
        print build_tree(dataX, dataY)
        print build_tree(dataX, dataY).shape
        return build_tree(dataX, dataY)

        # self.d_tree = build_tree(dataX, dataY)

    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
if __name__=="__main__":
    print "the secret clue is 'zzyzx'"