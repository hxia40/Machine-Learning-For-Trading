"""
Name: Shuyan Huang
ID: shuang379
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
        self.lookback = 7

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol="IBM", \
                    sd=dt.datetime(2008, 1, 1), \
                    ed=dt.datetime(2009, 1, 1), \
                    sv=10000):

        # stock_older_days = 30
        symbols = [symbol]
        prices, sma, p_to_sma = indicators.price_sma(start_date=sd, end_date=ed, symbols=symbols)
        prices.columns = ['Price']
        sma.columns = ['sma']
        p_to_sma.columns = ['p/sma']

        rsi = indicators.rsi(start_date=sd, end_date=ed, symbols=symbols)
        mfi = indicators.mfi(start_date=sd, end_date=ed, symbols=symbols)
        vix = indicators.vix(start_date=sd, end_date=ed, symbols=symbols)
        rsi.columns = ['RSI']
        mfi.columns = ['MFI']
        vix.columns = ['VIX']

        portfolio = prices.copy()
        portfolio.iloc[:, :] = np.nan

        Xtrain = pd.concat([p_to_sma, rsi, mfi, vix], axis=1)
        Xtrain.fillna(value=0, inplace=True)
        # print '=========Xtrain=======\n'
        # print Xtrain
        date_index = Xtrain.index
        Xtrain = Xtrain.values[:, 1:]
        # print '=========trainX=======\n'
        # print trainX

        Ytrain = (prices.shift(-self.lookback) / prices) - 1  # Ytrain is 14 day return
        # print '=========Ytrain=======\n', Ytrain
        Ytrain = Ytrain.values
        # Ytrain.nan_to_num(0, copy=True)shift
        # print '=========Ytrain=======\n', Ytrain
        YBUY = 0.03
        YSELL = -0.03
        for i in range(len(Ytrain)):
            if Ytrain[i] > YBUY:
                Ytrain[i] = 1
            elif Ytrain[i] < YSELL:
                Ytrain[i] = -1
            else:
                Ytrain[i] = 0
        # print '=========Ytrain=======\n', Ytrain
        # print 'self.learner_1=======\n', self.learner_1
        self.learner.addEvidence(Xtrain, Ytrain)
        self.Y_in = self.learner.query(Xtrain)


    def testPolicy(self, symbol="IBM", \
                   sd=dt.datetime(2009, 1, 1), \
                   ed=dt.datetime(2010, 1, 1), \
                   sv=10000):

        # stock_older_days = 30
        symbols = [symbol]
        prices, sma, p_to_sma = indicators.price_sma(start_date=sd, end_date=ed, symbols=symbols)
        prices.columns = ['Price']
        sma.columns = ['sma']
        p_to_sma.columns = ['p/sma']

        rsi = indicators.rsi(start_date=sd, end_date=ed, symbols=symbols)
        mfi = indicators.mfi(start_date=sd, end_date=ed, symbols=symbols)
        vix = indicators.vix(start_date=sd, end_date=ed, symbols=symbols)
        rsi.columns = ['RSI']
        mfi.columns = ['MFI']
        vix.columns = ['VIX']

        portfolio = prices.copy()
        portfolio.iloc[:, :] = np.nan

        Xtrain = pd.concat([p_to_sma, rsi, mfi, vix], axis=1)
        Xtrain.fillna(value=0, inplace=True)
        # print '=========Xtrain=======\n', Xtrain

        trading_days = Xtrain.index
        Xtest = Xtrain.values[:, 1:]
        # print '=========Xtest=======\n', Xtest

        
        triggers = self.learner.query(Xtest)
        # print '==========triggers====\n', triggers
        triggers = pd.DataFrame(triggers[0], index=trading_days)
        # use this for bag learner: triggers = pd.DataFrame(triggers[0], index=trading_days)

        status = 'cash'
        trades = prices.copy()
        trades.values[:, :] = 0  # set them all to nothing
        total_triggers = triggers.shape[0]
        trading_days = list(prices.index)
        j = 0

        for i in range(total_triggers):
            # option = triggers.ix[i, symbol][0]
            option = triggers.ix[i, 0]
            gap = trading_days.index(triggers.index[i]) - trading_days.index(triggers.index[j])
            if status == 'cash':
                if option == 1.0:
                    trades.ix[triggers.index[i], :] = 1000
                    status = 'long'
                    j = i
                elif option == -1.0:
                    trades.ix[triggers.index[i], :] = -1000
                    status = 'short'
                    j = i
            elif status == 'long':
                if (option == 0.0) & (gap >= self.lookback):
                    trades.ix[triggers.index[i], :] = -1000
                    status = 'cash'
                    j = i
                elif (option == -1.0) & (gap >= self.lookback):
                    trades.ix[triggers.index[i], :] = -2000
                    status = 'short'
                    j = i
            elif status == 'short':
                if (option == 0.0) & (gap >= self.lookback):
                    trades.ix[triggers.index[i], :] = 1000
                    status = 'cash'
                    j = i
                elif (option == 1.0) & (gap >= self.lookback):
                    trades.ix[triggers.index[i], :] = 2000
                    status = 'long'
                    j = i

        if self.verbose: print type(trades)  # it better be a DataFrame!
        if self.verbose: print trades
        return trades


if __name__ == "__main__":
    print "One does not simply think up a strategy"

    test_learner = StrategyLearner(verbose=False, impact=0.005)
    test_learner.addEvidence(symbol="ML4T-220", \
                             sd=dt.datetime(2008, 1, 1), \
                             ed=dt.datetime(2009, 12, 31), \
                             sv=10000)

    trades = test_learner.testPolicy(symbol="ML4T-220", \
                                     sd=dt.datetime(2008, 1, 1), \
                                     ed=dt.datetime(2009, 12, 31), \
                                     sv=10000)
