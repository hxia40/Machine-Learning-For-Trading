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

    trades_sl = df_trades_sl.astype(bool).sum(axis=0)
    trades_ms = df_trades_ms.astype(bool).sum(axis=0)
    # print 'trades_sl', trades_sl
    # print 'trades_ms', trades_ms

    '''
    **************
    In-sample data
    **************
    '''

    df_benchmark = df_trades_sl.copy()
    df_benchmark.iloc[:, 0] = 0
    df_benchmark.iloc[0, 0] = 1000
    # print '==============dfbenchmark============\n', df_benchmark

    i_list = []
    sharpe_ratio_sl_list = []
    sharpe_ratio_ms_list = []
    sharpe_ratio_ben_list = []
    cum_ret_sl_list = []
    cum_ret_ms_list = []
    cum_ret_ben_list = []
    std_daily_ret_sl_list = []
    std_daily_ret_ms_list = []
    std_daily_ret_ben_list = []

    for n in range(0, 1000, 10):
        # print 'n =', n
        i = float(n)/1000
        i_list.append(i)
        # print i_list
        # Process orders
        portvals_sl = sim.compute_portvals(orders_file=df_trades_sl, start_val=100000, commission=0, impact=i)
        portvals_sl = portvals_sl / portvals_sl[0]
        # print '======sl======\n', portvals_sl

        portvals_ms = sim.compute_portvals(orders_file=df_trades_ms, start_val=100000, commission=0, impact=i)
        portvals_ms = portvals_ms / portvals_ms[0]
        # print '======ms======\n', portvals_ms

        ben_portval = sim.compute_portvals(orders_file=df_benchmark, start_val=100000, commission=0, impact=i)
        ben_portval = ben_portval / ben_portval[0]
        # print '==============ben_portval============\n', ben_portval

        start_date = portvals_ms.index[0]
        end_date = portvals_ms.index[-1]
        rfr = 0.0

        '''calculate for StrategyLearner Portfolio's parameters '''
        daily_rets_sl = portvals_sl / portvals_sl.shift(axis=0) - 1
        daily_rets_sl = daily_rets_sl[1:]
        cum_ret_sl = portvals_sl[-1] / portvals_sl[0] - 1  # cumulative return
        # print cum_ret_sl
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

        sharpe_ratio_sl_list.append(sharpe_ratio_sl)
        sharpe_ratio_ms_list.append(sharpe_ratio_ms)
        sharpe_ratio_ben_list.append(sharpe_ratio_ben)
        cum_ret_sl_list.append(cum_ret_sl)
        cum_ret_ms_list.append(cum_ret_ms)
        cum_ret_ben_list.append(cum_ret_ben)
        std_daily_ret_sl_list.append(std_daily_ret_sl)
        std_daily_ret_ms_list.append(std_daily_ret_ms)
        std_daily_ret_ben_list.append(std_daily_ret_ben)

    # print i_list
    # print sharpe_ratio_sl_list
    # print sharpe_ratio_ms_list
    # print cum_ret_sl_list
    # print cum_ret_ms_list
    # print std_daily_ret_sl_list
    # print std_daily_ret_ms_list

    # plt.figure(figsize=(8, 4))

    # plt.plot(i_list, sharpe_ratio_sl_list, label='Strategy Learner Portfolio', color='B')
    # plt.plot(i_list, sharpe_ratio_ms_list, label='Manual Strategy Portfolio', color='R')
    # # plt.plot(i_list, sharpe_ratio_ben_list, label='Benchmark Portfolio', color='G')
    # plt.ylabel('Value')
    # plt.xlabel('Impact')
    # plt.title('Experiment 2: Impact of Impact - Sharpe Ratio')
    # plt.legend(loc='best')
    # plt.savefig('Figure2.png')
    # plt.show()
    # plt.gcf().clear()
    plt.plot(i_list[:20], cum_ret_sl_list[:20], label='Strategy Learner Portfolio', color='B')
    plt.plot(i_list[:20], cum_ret_ms_list[:20], label='Manual Strategy Portfolio', color='R')
    # plt.plot(i_list, cum_ret_ben_list, label='Bnechmark Portfolio', color='G')
    plt.ylabel('Value')
    plt.xlabel('Impact')
    plt.title('Experiment 2: Impact of Impact - Cumulative Return')
    plt.legend(loc='best')
    plt.savefig('Figure2.png')
    plt.show()
    plt.gcf().clear()

    plt.plot(i_list, cum_ret_sl_list, label='Strategy Learner Portfolio', color='B')
    plt.plot(i_list, cum_ret_ms_list, label='Manual Strategy Portfolio', color='R')
    # plt.plot(i_list, cum_ret_ben_list, label='Bnechmark Portfolio', color='G')
    plt.ylabel('Value')
    plt.xlabel('Impact')
    plt.title('Experiment 2: Impact of Impact - Cumulative Return')
    plt.legend(loc='best')
    plt.savefig('Figure3.png')
    plt.show()
    plt.gcf().clear()

    # plt.plot(i_list, std_daily_ret_sl_list, label='Strategy Learner Portfolio', color='B')
    # plt.plot(i_list, std_daily_ret_ms_list, label='Manual Strategy Portfolio', color='R')
    # # plt.plot(i_list, std_daily_ret_ben_list, label='Benchmark Portfolio', color='R')
    # plt.ylabel('Value')
    # plt.xlabel('Impact')
    # plt.title('Experiment 2: Impact of Impact - Standard Deviation')
    # plt.legend(loc='best')
    # plt.savefig('Figure4.png')
    # plt.show()
    # plt.gcf().clear()