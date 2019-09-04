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
        trainX = Xtrain.values[:, 1:]
        # print '=========trainX=======\n'
        # print trainX

        self.N = 7
        nday_rt = prices.shift(-self.N) / prices - 1.0
        pd.set_option('display.max_rows', 1000)
        # print 'n days return: '
        # print nday_rt
        # print
        nday_rt[nday_rt > 0] = prices.shift(-self.N) / (prices * (1.0 + self.impact)) - 1.0
        nday_rt[nday_rt < 0] = prices.shift(-self.N) / (prices * (1.0 - self.impact)) - 1.0
        # print 'n days return: '
        # print nday_rt
        # print
        yvalues = nday_rt.copy()
        yvalues.iloc[:, :] = 0

        # go long when return is larger than 3%, go short when return is lower than -3%
        threshold = 0.03
        yvalues[nday_rt >= threshold] = 1
        yvalues[nday_rt <= -threshold] = -1
        # print xvalues == 0
        yvalues[trainX == 0] = 0
        trainY = np.array(yvalues)
        self.learner.addEvidence(trainX, trainY)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol="IBM", \
                   sd=dt.datetime(2009, 1, 1), \
                   ed=dt.datetime(2010, 1, 1), \
                   sv=10000):
        '''
        # # here we build a fake set of trades
        # # your code should return the same sort of data
        # dates = pd.date_range(sd, ed)
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        # prices = prices_all[[symbol, ]]
        # trading_days = prices.index
        #
        # price_sma, rsi, macd_hist = get_indicators(prices)
        #
        # xvalues = pd.concat([price_sma, rsi, macd_hist], ignore_index=True, axis=1)
        # # print '=====xvalues=====\n', xvalues
        # xvalues.fillna(value=0, inplace=True)
        # testX = np.array(xvalues)
        '''

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
        testX = Xtrain.values[:, 1:]
        # print '=========trainX=======\n', testX

        # print '==========textX====\n', testX
        triggers = self.learner.query(testX)
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
                if (option == 0.0) & (gap >= self.N):
                    trades.ix[triggers.index[i], :] = -1000
                    status = 'cash'
                    j = i
                elif (option == -1.0) & (gap >= self.N):
                    trades.ix[triggers.index[i], :] = -2000
                    status = 'short'
                    j = i
            elif status == 'short':
                if (option == 0.0) & (gap >= self.N):
                    trades.ix[triggers.index[i], :] = 1000
                    status = 'cash'
                    j = i
                elif (option == 1.0) & (gap >= self.N):
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
