import StrategyLearner as sl
import ManualStrategy as ms
import datetime as dt
import marketsimcode as sim
import matplotlib.pyplot as plt
import pandas as pd
import util as ut
import random

def author(self):
    return 'hxia40'  # replace tb34 with your Georgia Tech username.


if __name__ == "__main__":
    learner_sl = sl.StrategyLearner()
    learner_ms = ms.ManualStrategy()

    learner_sl.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)

    df_trades_sl = learner_sl.testPolicy(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
    df_trades_ms = learner_ms.testPolicy(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)[0]

    df_trades_sl.columns = ['JPM']
    df_trades_ms.columns = ['JPM']

    # print 'df_trades_sl'
    # print type(df_trades_sl)
    # print df_trades_sl
    # print 'df_trades_ms'
    # print type(df_trades_ms)
    # print df_trades_ms

    '''
    **************
    In-sample data
    **************
    '''

    df_benchmark = df_trades_sl.copy()
    df_benchmark.iloc[:, 0] = 0
    df_benchmark.iloc[0, 0] = 1000
    # print '==============dfbenchmark============\n', df_benchmark

    # Process orders
    portvals_sl = sim.compute_portvals(orders_file=df_trades_sl, start_val=100000, commission=0, impact=0.000)
    portvals_sl = portvals_sl / portvals_sl[0]
    # print '======sl======\n', portvals_sl

    portvals_ms = sim.compute_portvals(orders_file=df_trades_ms, start_val=100000, commission=0, impact=0.000)
    portvals_ms = portvals_ms / portvals_ms[0]
    # print '======ms======\n', portvals_ms

    ben_portval = sim.compute_portvals(orders_file=df_benchmark, start_val=100000, commission=0, impact=0.000)
    ben_portval = ben_portval / ben_portval[0]
    # print '==============ben_portval============\n', ben_portval

    plt.figure(figsize=(8, 4))
    plt.gcf().clear()
    plt.plot(portvals_ms.index, portvals_sl, label='Strategy Learner Portfolio', color='B')
    plt.plot(portvals_ms.index, portvals_ms, label='Manual Strategy Portfolio', color='R')
    plt.plot(portvals_ms.index, ben_portval, label='Benchmark', color='G')
    # for j in short_exit:
    #     plt.axvline(x=j, color='Purple')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Experiment 1: In-sample Data')
    plt.legend(loc='best')
    plt.savefig('Figure1.png')
    # plt.show()
    plt.gcf().clear()


    start_date = portvals_ms.index[0]
    end_date = portvals_ms.index[-1]
    rfr = 0.0

    '''calculate for StrategyLearner Portfolio's parameters '''
    daily_rets_sl = portvals_sl / portvals_sl.shift(axis=0) - 1
    daily_rets_sl = daily_rets_sl[1:]
    cum_ret_sl = portvals_sl[-1] / portvals_sl[0] - 1  # cumulative return
    avg_daily_ret_sl = daily_rets_sl.mean()  # average daily return
    std_daily_ret_sl = daily_rets_sl.std()  # standard deviation of daily return
    sharpe_ratio_sl = ((daily_rets_sl - rfr).mean() / std_daily_ret_sl) * (252 ** 0.5)  # sharpe ratio

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
    print "Sharpe Ratio of StrategyLearner: {}".format(sharpe_ratio_sl)
    print "Sharpe Ratio of Manual: {}".format(sharpe_ratio_ms)
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_ben)
    print
    print "Cumulative Return of StrategyLearner: {}".format(cum_ret_sl)
    print "Cumulative Return of Manual: {}".format(cum_ret_ms)
    print "Cumulative Return of Benchmark : {}".format(cum_ret_ben)
    print
    print "Standard Deviation of StrategyLearner: {}".format(std_daily_ret_sl)
    print "Standard Deviation of Manual: {}".format(std_daily_ret_ms)
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_ben)
    print
    print "Average Daily Return of StrategyLearner: {}".format(avg_daily_ret_sl)
    print "Average Daily Return of Manual: {}".format(avg_daily_ret_ms)
    print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_ben)
    print
    print "Final StrategyLearner Portfolio Value: {}".format(portvals_sl[-1])
    print "Final Manual Portfolio Value: {}".format(portvals_ms[-1])
    print "Final Benchmark Portfolio Value: {}".format(ben_portval[-1])