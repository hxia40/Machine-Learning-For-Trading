"""Manual Strategy.
 			  		 			     			  	   		   	  			  	
Student Name: Hui Xia (replace with your name)
GT User ID: hxia40 (replace with your User ID)
GT ID: 903459648 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data
import marketsimcode as sim
import indicators
import matplotlib.pyplot as plt

class ManualStrategy(object):
    def __init__(self):
        pass

    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username.

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        symbols = [symbol]

        stock_price, sma, p_to_sma = indicators.price_sma(start_date = sd, end_date = ed, symbols = symbols)
        rsi = indicators.rsi(start_date = sd, end_date = ed, symbols = symbols)
        mfi = indicators.mfi(start_date=sd, end_date=ed, symbols=symbols)
        vix = indicators.vix(start_date=sd, end_date=ed, symbols=symbols)

        portfolio = stock_price.copy()
        portfolio.iloc[:, :] = np.nan
        # print '======begining portfolio====\n', portfolio
        # print portfolio

        curr_state = 'neutral'
        long_entry = []
        long_exit = []
        short_entry = []
        short_exit = []

        for i in range(len(portfolio)):
            # print curr_state
            if (rsi.iloc[i, 0] < 30) & (p_to_sma.iloc[i, 0] < 1) & (curr_state != 'long') & (vix.iloc[i, 0] < 50):
                portfolio.iloc[i, 0] = 1000
                curr_state = 'long'
                long_entry.append(portfolio.iloc[i:].index[0])

            elif (mfi.iloc[i, 0] > 70) & (p_to_sma.iloc[i, 0] > 1) & (curr_state != 'short') & (vix.iloc[i, 0] > 20):
                portfolio.iloc[i, 0] = -1000
                curr_state = 'short'
                short_entry.append(portfolio.iloc[i:].index[0])

            if (rsi.iloc[i, 0] >= 55) & (curr_state == 'long'):
                portfolio.iloc[i, 0] = 0
                curr_state = 'neutral'
                long_exit.append(portfolio.iloc[i:].index[0])

            elif (mfi.iloc[i, 0] <= 45) & (curr_state == 'short'):
                portfolio.iloc[i, 0] = 0
                curr_state = 'neutral'
                short_exit.append(portfolio.iloc[i:].index[0])

        portfolio.fillna(method='ffill', inplace=True)
        portfolio.fillna(0, inplace=True)
        # print '======end portfolio====\n', portfolio
        df_trade = portfolio - portfolio.shift(1)
        df_trade.iloc[0] = portfolio.iloc[0]
        # print '=====df_ttrade=====\n', df_trade
        return df_trade, long_entry, long_exit, short_entry, short_exit


if __name__ == "__main__":
    '''
    **************
    In-sample data
    **************
    '''

    ms = ManualStrategy()
    df_trades_ms, long_entry, long_exit, short_entry, short_exit = \
        ms.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    sv = 100000

    df_benchmark = df_trades_ms.copy()
    df_benchmark.iloc[:, 0] = 0
    df_benchmark.iloc[0, 0] = 1000
    # print '==============dfbenchmark============\n', df_benchmark

    # Process orders

    portvals_ms = sim.compute_portvals(orders_file=df_trades_ms, start_val=sv, commission=9.95, impact=0.005)
    portvals_ms = portvals_ms / portvals_ms[0]

    ben_portval = sim.compute_portvals(orders_file=df_benchmark, start_val=sv, commission=9.95, impact=0.005)
    ben_portval = ben_portval / ben_portval[0]
    # print '==============ben_portval============\n', ben_portval

    plt.figure(figsize=(8, 4))
    plt.gcf().clear()
    plt.plot(portvals_ms.index, portvals_ms, label='Manual Strategy Portfolio', color='R')
    plt.plot(portvals_ms.index, ben_portval, label='Benchmark', color='G')
    plt.axvline(x=long_entry[0], color='Blue', label='Long Entry')
    plt.axvline(x=short_entry[0], color='Black', label='Short Entry')
    for m in long_entry:
        plt.axvline(x=m, color='Blue')
    # for i in long_exit:
    #     plt.axvline(x=i, color='Orange')
    for n in short_entry:
        plt.axvline(x=n, color='Black')
    # for j in short_exit:
    #     plt.axvline(x=j, color='Purple')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Part 3: Manual Strategy')
    plt.legend(loc='best')
    plt.savefig('Figure6.png')
    plt.gcf().clear()

    start_date = portvals_ms.index[0]
    end_date = portvals_ms.index[-1]
    rfr = 0.0

    '''calculate for Manual Portfolio's parameters '''
    daily_rets_ms = portvals_ms / portvals_ms.shift(axis=0) - 1
    daily_rets_ms = daily_rets_ms[1:]
    cum_ret_ms = portvals_ms[-1] / portvals_ms[0] - 1  # cumulative return
    avg_daily_ret_ms = daily_rets_ms.mean()  # average daily return
    std_daily_ret_ms = daily_rets_ms.std()  # standard deviation of daily return
    sharpe_ratio_ms = ((daily_rets_ms - rfr).mean() / std_daily_ret_ms) * (252 ** 0.5)  # sharpe ratio

    '''calculate for benchmark(invest 1000 shares of JPM)'s parameters '''

    daily_rets_ben = (ben_portval / ben_portval.shift(axis=0)) - 1
    daily_rets_ben = daily_rets_ben[1:]
    cum_ret_ben = ben_portval.iloc[-1] / ben_portval.iloc[0] - 1  # cumulative return
    # print 'cun return ben', cum_ret_ben

    avg_daily_ret_ben = daily_rets_ben.mean()  # average daily return
    std_daily_ret_ben = daily_rets_ben.std()  # standard deviation of daily return
    sharpe_ratio_ben = ((daily_rets_ben - rfr).mean() / std_daily_ret_ben) * (
                252 ** 0.5)  # sharpe ratio, adjusted for daily sampling
    # #
    #
    # Compare portfolio against $SPX

    print '**************'
    print 'In-sample data'
    print '**************'
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Manual: {}".format(sharpe_ratio_ms)
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_ben)
    print
    print "Cumulative Return of Manual: {}".format(cum_ret_ms)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_ben)
    print
    print "Standard Deviation of Manual: {}".format(std_daily_ret_ms)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_ben)
    print
    print "Average Daily Return of Manual: {}".format(avg_daily_ret_ms)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_ben)
    print
    print "Final Manual Portfolio Value: {}".format(portvals_ms[-1])
    print "Final Benchmark Portfolio Value: {}".format(ben_portval[-1])

    '''
    **************
    Out-of-sample data
    **************
    '''


    df_trades_ms, long_entry, long_exit, short_entry, short_exit = \
        ms.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    sv = 100000

    df_benchmark = df_trades_ms.copy()
    df_benchmark.iloc[:, 0] = 0
    df_benchmark.iloc[0, 0] = 1000
    # print '==============dfbenchmark============\n', df_benchmark

    # Process orders

    portvals_ms = sim.compute_portvals(orders_file=df_trades_ms, start_val=sv, commission=9.95, impact=0.005)
    portvals_ms = portvals_ms / portvals_ms[0]

    ben_portval = sim.compute_portvals(orders_file=df_benchmark, start_val=sv, commission=9.95, impact=0.005)
    ben_portval = ben_portval / ben_portval[0]


    plt.plot(portvals_ms.index, portvals_ms, label='Manual Strategy Portfolio', color='R')
    plt.plot(portvals_ms.index, ben_portval, label='Benchmark', color='G')
    plt.axvline(x=long_entry[0], color='Blue', label='Long Entry')
    plt.axvline(x=short_entry[0], color='Black', label='Short Entry')
    for m in long_entry:
        plt.axvline(x=m, color='Blue')
    # for i in long_exit:
    #     plt.axvline(x=i, color='Orange')
    for n in short_entry:
        plt.axvline(x=n, color='Black')
    # for j in short_exit:
    #     plt.axvline(x=j, color='Purple')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Part 4: Comparative Analysis')
    plt.legend(loc='best')
    plt.savefig('Figure7.png')
    plt.gcf().clear()

    start_date = portvals_ms.index[0]
    end_date = portvals_ms.index[-1]
    rfr = 0.0


    '''calculate for Manual Portfolio's parameters '''
    daily_rets_ms = portvals_ms / portvals_ms.shift(axis=0) - 1
    daily_rets_ms = daily_rets_ms[1:]
    cum_ret_ms = portvals_ms[-1] / portvals_ms[0] - 1  # cumulative return
    avg_daily_ret_ms = daily_rets_ms.mean()  # average daily return
    std_daily_ret_ms = daily_rets_ms.std()  # standard deviation of daily return
    sharpe_ratio_ms = ((daily_rets_ms - rfr).mean() / std_daily_ret_ms) * (252 ** 0.5)  # sharpe ratio

    '''calculate for benchmark(invest 1000 shares of JPM)'s parameters '''

    daily_rets_ben = (ben_portval / ben_portval.shift(axis=0)) - 1
    daily_rets_ben = daily_rets_ben[1:]
    cum_ret_ben = ben_portval.iloc[-1] / ben_portval.iloc[0] - 1  # cumulative return
    # print 'cun return ben', cum_ret_ben

    avg_daily_ret_ben = daily_rets_ben.mean()  # average daily return
    std_daily_ret_ben = daily_rets_ben.std()  # standard deviation of daily return
    sharpe_ratio_ben = ((daily_rets_ben - rfr).mean() / std_daily_ret_ben) * (
            252 ** 0.5)  # sharpe ratio, adjusted for daily sampling

    print '**************'
    print 'Out-of-sample data'
    print '**************'
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Manual: {}".format(sharpe_ratio_ms)
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_ben)
    print
    print "Cumulative Return of Manual: {}".format(cum_ret_ms)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_ben)
    print
    print "Standard Deviation of Manual: {}".format(std_daily_ret_ms)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_ben)
    print
    print "Average Daily Return of Manual: {}".format(avg_daily_ret_ms)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_ben)
    print
    print "Final Manual Portfolio Value: {}".format(portvals_ms[-1])
    print "Final Benchmark Portfolio Value: {}".format(ben_portval[-1])