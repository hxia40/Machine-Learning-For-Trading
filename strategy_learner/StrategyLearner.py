""" 			  		 			     			  	   		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
Student Name: Hui Xia (replace with your name)
GT User ID: hxia40 (replace with your User ID)
GT ID: 903459648 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
import datetime as dt
import pandas as pd
import util as ut
import random
import RTLearner as rt
import BagLearner as bl
import indicators
import numpy as np


class StrategyLearner(object):
    # constructor
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        # self.learner = rt.RTLearner(leaf_size=5, verbose=False)  # constructor
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={'leaf_size': 5}, bags=20, boost=False, verbose=True)
        self.lookback = 14
        self.impact = impact

    def author(self):
        return 'hxia40' # replace tb34 with your Georgia Tech username

    def addEvidence(self, symbol="IBM", \
                    sd=dt.datetime(2008, 1, 1), \
                    ed=dt.datetime(2009, 1, 1), \
                    sv=10000):

        '''Firstly assemble the indicators into the trainning Dataframe (Xtrain and Ytrain), then train the RTLearner'''
        '''calculate indicators'''
        stock_older_days = 45
        symbols = [symbol]
        prices, unused_a, unused_b = indicators.price_sma(start_date=(sd - dt.timedelta(days=stock_older_days)),
                                                          end_date=ed, symbols=symbols)
        first_trading_day = sd
        while first_trading_day not in prices.index:
            first_trading_day += dt.timedelta(days=1)
        prices = prices / prices.loc[first_trading_day]
        sma = prices.copy().rolling(14).mean()
        p_to_sma = prices / sma
        prices.columns = ['Price']
        sma.columns = ['sma']
        p_to_sma.columns = ['p/sma']

        rsi = indicators.rsi(start_date=(sd - dt.timedelta(days=stock_older_days)), end_date=ed, symbols=symbols)
        mfi = indicators.mfi(start_date=(sd - dt.timedelta(days=stock_older_days)), end_date=ed, symbols=symbols)
        vix = indicators.vix(start_date=sd, end_date=ed, symbols=symbols)
        rsi.columns = ['RSI']
        mfi.columns = ['MFI']
        vix.columns = ['VIX']

        '''cut indicators into proper size. i.e. betyween start_date and end_date'''

        prices = prices.loc[first_trading_day:]
        sma = sma.loc[first_trading_day:]
        p_to_sma = p_to_sma.loc[first_trading_day:]
        rsi = rsi.loc[first_trading_day:]
        mfi = mfi.loc[first_trading_day:]
        vix = vix.loc[first_trading_day:]

        '''assemble Xtrain'''

        Xtrain = pd.concat([p_to_sma, rsi, mfi, vix], axis=1)
        # Xtrain.fillna(value=0, inplace=True)
        # print '=========Xtrain=======\n'
        # print Xtrain
        Xtrain = Xtrain.values[:, 1:]
        # print '=========trainX=======\n'
        # print trainX

        '''assemble Ytrain'''

        Ytrain = (prices.shift(-self.lookback) / prices) - 1  # Ytrain is 14 day return
        # print '=========Ytrain=======\n', Ytrain

        Ytrain[Ytrain > 0] = prices.shift(-self.lookback) / (prices * (1.0 + 2 * self.impact)) - 1.0
        Ytrain[Ytrain < 0] = prices.shift(-self.lookback) / (prices * (1.0 - 2 * self.impact)) - 1.0
        Ytrain = Ytrain.values
        # Ytrain.nan_to_num(0, copy=True)shift
        # print '=========Ytrain=======\n', Ytrain

        YBUY = 0.08
        YSELL = -0.08
        for i in range(len(Ytrain)):
            if Ytrain[i] > YBUY:
                Ytrain[i] = 1
            elif Ytrain[i] < YSELL:
                Ytrain[i] = -1
            else:
                Ytrain[i] = 0
        # print '=========Ytrain=======\n', Ytrain
        # print 'self.learner_1=======\n', self.learner_1

        '''use Xtain and Ytrain to train the random table'''
        self.learner.addEvidence(Xtrain, Ytrain)
        self.Y_in = self.learner.query(Xtrain)


    def testPolicy(self, symbol="IBM", \
                   sd=dt.datetime(2009, 1, 1), \
                   ed=dt.datetime(2010, 1, 1), \
                   sv=10000):
        '''Firstly assemble the indicators into the testing Dataframe (Xtest), then query the RTLearner for Ytrain'''
        '''calculate indicators'''
        stock_older_days = 45
        symbols = [symbol]
        prices, unused_a, unused_b = indicators.price_sma(start_date=(sd - dt.timedelta(days=stock_older_days)),
                                                          end_date=ed, symbols=symbols)
        first_trading_day = sd
        while first_trading_day not in prices.index:
            first_trading_day += dt.timedelta(days=1)
        prices = prices / prices.loc[first_trading_day]
        sma = prices.copy().rolling(14).mean()
        p_to_sma = prices / sma
        prices.columns = ['Price']
        sma.columns = ['sma']
        p_to_sma.columns = ['p/sma']

        rsi = indicators.rsi(start_date=(sd - dt.timedelta(days=stock_older_days)), end_date=ed, symbols=symbols)
        mfi = indicators.mfi(start_date=(sd - dt.timedelta(days=stock_older_days)), end_date=ed, symbols=symbols)
        vix = indicators.vix(start_date=sd, end_date=ed, symbols=symbols)
        rsi.columns = ['RSI']
        mfi.columns = ['MFI']
        vix.columns = ['VIX']

        '''cut indicators into proper size. i.e. betyween start_date and end_date'''

        prices = prices.loc[first_trading_day:]
        sma = sma.loc[first_trading_day:]
        p_to_sma = p_to_sma.loc[first_trading_day:]
        rsi = rsi.loc[first_trading_day:]
        mfi = mfi.loc[first_trading_day:]
        vix = vix.loc[first_trading_day:]

        '''' make empty portfolio for future use'''

        portfolio = prices.copy()
        portfolio.iloc[:, :] = np.nan

        '''assemble Xtest'''
        Xtest = pd.concat([p_to_sma, rsi, mfi, vix], axis=1, join_axes=[vix.index])
        # Xtrain.fillna(value=0, inplace=True)
        # print '=========Xtrain=======\n', Xtrain
        date_index = Xtest.index
        Xtest = Xtest.values[:, 1:]
        # print '=========Xtest=======\n', Xtest

        '''query for Ytest, then assemble it back to a dataframe for the market simulator'''

        Ytest = self.learner.query(Xtest)
        # print list(self.y_nparray[0])
        # print '=========Y_in=======\n', self.y_nparray
        y_df = pd.DataFrame(data=list(Ytest[0]), index=date_index, columns=['Ytest'])
        # note: use (data=list(self.y_nparray[0]) for bagged
        # print '====y_df====\n', y_df
        # print y_df

        '''simulating market, enter a position, then exit the position until lookback days passed '''
        curr_state = 'neutral'
        long_entry = []
        long_exit = []
        short_entry = []
        short_exit = []
        entry_point = 0

        for i in range(len(y_df)):
            if ((int(y_df.iloc[i])) == 1) & (curr_state == 'neutral'):
                # if (int(y_df.iloc[i])) == 1:
                curr_state = 'long'
                portfolio.iloc[i, 0] = 1000
                entry_point = i
                long_entry.append(portfolio.iloc[i:].index[0])

            elif ((int(y_df.iloc[i])) == -1) & (curr_state == 'neutral'):
                # elif (int(y_df.iloc[i])) == -1:
                curr_state = 'short'
                portfolio.iloc[i, 0] = -1000
                entry_point = i
                short_entry.append(portfolio.iloc[i:].index[0])

            if (i >= entry_point + self.lookback) & (curr_state == 'long'):
                portfolio.iloc[i, 0] = 0
                curr_state = 'neutral'
                entry_point = 0
                long_exit.append(portfolio.iloc[i:].index[0])

            elif (i >= entry_point + self.lookback) & (curr_state == 'short'):
                portfolio.iloc[i, 0] = 0
                curr_state = 'neutral'
                entry_point = 0
                short_exit.append(portfolio.iloc[i:].index[0])

        '''good old market simulator, generating the df_trade'''

        portfolio.fillna(method='ffill', inplace=True)
        portfolio.fillna(0, inplace=True)
        # print '======end portfolio====\n', portfolio
        df_trade = portfolio - portfolio.shift(1)
        df_trade.iloc[0] = portfolio.iloc[0]
        # print '=====df_ttrade=====\n', type(df_trade)
        return df_trade


if __name__ == "__main__":
    test_learner = StrategyLearner()
    test_learner.addEvidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=10000)
    trades = test_learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=10000)
