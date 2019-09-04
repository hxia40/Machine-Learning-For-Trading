"""Theoretically Optimal Strategy.
 			  		 			     			  	   		   	  			  	
Student Name: Hui Xia (replace with your name)
GT User ID: hxia40 (replace with your User ID)
GT ID: 903459648 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import matplotlib.pyplot as plt
from util import get_data, plot_data
import marketsimcode as sim

class TheoreticallyOptimalStrategy(object):
    def __init__(self):
        pass

    def author(self):
        return 'hxia40'  # replace tb34 with your Georgia Tech username.

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
        symbols = [symbol]

        stock_price = get_data(symbols, pd.date_range(sd, ed), addSPY=True, colname='Adj Close')
        # plot_data(stock_price)
        stock_price.fillna(method='ffill', inplace=True)
        stock_price.fillna(method='bfill', inplace=True)
        stock_price.drop(['SPY'], axis=1, inplace=True)
        stock_price = stock_price / stock_price.iloc[0, 0]
        daily_return = stock_price - stock_price.shift(1)
        # print daily_return

        portfolio = daily_return.copy().where(daily_return < 0, 1000)
        portfolio = portfolio.where(portfolio == 1000, -1000)
        portfolio = portfolio.shift(-1)
        # print portfolio
        df_trade = portfolio - portfolio.shift(1)
        df_trade.iloc[0] = portfolio.iloc[0]
        df_trade.fillna(0, inplace=True)
        # print df_trade
        return df_trade


if __name__ == "__main__":

    '''
    **************
    In-sample data
    **************
    '''
    tos = TheoreticallyOptimalStrategy()
    df_trades_tos = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    sv = 100000
    # print '============df_trades_tos=======\n', df_trades_tos
    df_benchmark = df_trades_tos.copy()
    df_benchmark.iloc[:, 0] = 0
    df_benchmark.iloc[0, 0] = 1000
    # print '==============dfbenchmark============\n', df_benchmark

    # Process orders
    portvals_tos = sim.compute_portvals(orders_file=df_trades_tos, start_val=sv, commission=0.0, impact=0.0)
    portvals_tos = portvals_tos / portvals_tos[0]

    ben_portval = sim.compute_portvals(orders_file=df_benchmark, start_val=sv, commission=0.0, impact=0.0)
    ben_portval = ben_portval / ben_portval[0]
    # print '==============ben_portval============\n', ben_portval
    plt.figure(figsize=(8, 4))
    plt.gcf().clear()
    plt.plot(portvals_tos.index, portvals_tos, label='Theoretically Optimal Portfolio', color='R')
    plt.plot(portvals_tos.index, ben_portval, label='Benchmark', color='G')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Part 2: Theoretically Optimal Strategy')
    plt.legend(loc='best')
    plt.savefig('Figure5.png')
    plt.gcf().clear()


    start_date = portvals_tos.index[0]
    end_date = portvals_tos.index[-1]
    rfr = 0.0
    '''calculate for our Theoretically Optimal Portfolio's parameters '''

    daily_rets_tos = portvals_tos / portvals_tos.shift(axis=0) - 1
    daily_rets_tos = daily_rets_tos[1:]
    cum_ret_tos = portvals_tos[-1] / portvals_tos[0] - 1  # cumulative return
    avg_daily_ret_tos = daily_rets_tos.mean()  # average daily return
    std_daily_ret_tos = daily_rets_tos.std()  # standard deviation of daily return
    sharpe_ratio_tos = ((daily_rets_tos - rfr).mean() / std_daily_ret_tos) * (252 ** 0.5)  # sharpe ratio


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
    print "Sharpe Ratio of Optimal: {}".format(sharpe_ratio_tos)
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_ben)
    print
    print "Cumulative Return of Optimal: {}".format(cum_ret_tos)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_ben)
    print
    print "Standard Deviation of Optimal: {}".format(std_daily_ret_tos)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_ben)
    print
    print "Average Daily Return of Optimal: {}".format(avg_daily_ret_tos)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_ben)
    print
    print "Final Optimal Portfolio Value: {}".format(portvals_tos[-1])
    print "Final Benchmark Portfolio Value: {}".format(ben_portval[-1])
