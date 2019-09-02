"""MC2-P1: Market simulator. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import os 			  		 			     			  	   		   	  			  	
from util import get_data, plot_data


def author():
    return 'hxia40'  # replace tb34 with your Georgia Tech username.
 			  		 			     			  	   		   	  			  	
def compute_portvals(orders_file = "./orders/orders-01.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code 			  		 			     			  	   		   	  			  	
    # NOTE: orders_file may be a string, or it may be a file object. Your 			  		 			     			  	   		   	  			  	
    # code should work correctly with either input 			  		 			     			  	   		   	  			  	
    # TODO: Your code here

    # ''' check if the orders_file is a DataFrame or a string - seems like no need to implent this'''
    # if isinstance(orders_file, pd.DataFrame):
    #     print 'dataframe!'
    # else:
    #     print "warning, code did not return a DataFrame"

    '''read in the orders and set them in Date order'''
        
    orders_df = pd.read_csv(orders_file, parse_dates=True, na_values=['nan'])
    orders_df['Date'] = pd.to_datetime(orders_df['Date'])
    orders_df.sort_values('Date', axis=0, ascending=True, inplace=True, na_position='last')

    orders_df.set_index('Date', inplace=True)
    # print '======orders=======\n', orders_df

    '''read in the value of the stocks mentioned in the order dataframe and the time'''

    start_date = orders_df.index.values[0]
    end_date = orders_df.index.values[-1]

    symbols = list(set(orders_df['Symbol'].values))
    # print 'symbols', symbols
    stock_price = get_data(symbols, pd.date_range(start_date, end_date))
    stock_price['Cash'] = 1
    # print '===========stock_price=======\n', stock_price

    '''make 'holdings dataframe' according to the 'stock price dataframe' and the 'order drataframe' generated above'''

    holdings = pd.DataFrame(index=stock_price.index, columns=stock_price.columns)
    holdings = holdings.fillna(0)
    holdings['Cash'] = 0
    holdings['Cash'][0] = start_val

    for date, rows_orders in orders_df.iterrows():      # getting the index (date) from orders_df
        if rows_orders[1] == 'BUY':
            holdings.loc[date, rows_orders[0]] += rows_orders[2]
            holdings.loc[date, 'Cash'] -= (stock_price.loc[date, rows_orders[0]] * (1 + impact)) * rows_orders[2]
            holdings.loc[date, 'Cash'] -= commission
        elif rows_orders[1] == 'SELL':
            holdings.loc[date, rows_orders[0]] -= rows_orders[2]
            holdings.loc[date, 'Cash'] += (stock_price.loc[date, rows_orders[0]] * (1 - impact)) * rows_orders[2]
            holdings.loc[date, 'Cash'] -= commission

    for i in range(0, len(holdings)):
        if i > 0:
            holdings.iloc[i, :] += holdings.iloc[i - 1, :]

    # print '==============holdings============\n', holdings

    '''make 'portvals dataframe' by summing everything up.'''

    portvals = (holdings * stock_price).sum(axis=1)
    portvals = portvals.to_frame()

    # print '==============portvals============\n',portvals
    # print type(portvals)

    return portvals

 			  		 			     			  	   		   	  			  	
def test_code(): 			  		 			     			  	   		   	  			  	
    # this is a helper function you can use to test your code 			  		 			     			  	   		   	  			  	
    # note that during autograding his function will not be called. 			  		 			     			  	   		   	  			  	
    # Define input parameters 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    of = "./orders/orders-07.csv"
    sv = 1000000 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Process orders 			  		 			     			  	   		   	  			  	
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame): 			  		 			     			  	   		   	  			  	
        portvals = portvals[portvals.columns[0]] # just get the first column 			  		 			     			  	   		   	  			  	
    else: 			  		 			     			  	   		   	  			  	
        "warning, code did not return a DataFrame" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # Get portfolio stats 			  		 			     			  	   		   	  			  	
    # Here we just fake the data. you should use your code from previous assignments.
    '''calculate for our portval's parameters '''
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    daily_rets = portvals / portvals.shift(axis=0) - 1
    daily_rets = daily_rets[1:]
    rfr = 0.0
    cum_ret = portvals[-1] / portvals[0] - 1  # cumulative return
    avg_daily_ret = daily_rets.mean()  # average daily return
    std_daily_ret = daily_rets.std()  # standard deviation of daily return
    sharpe_ratio = ((daily_rets - rfr).mean() / std_daily_ret) * (252 ** 0.5)  # sharpe ratio, adjusted for daily sampling

    '''calculate for SPY's parameters '''
    SPY_portval = get_data(['SPY'], pd.date_range(start_date, end_date))
    # print 'spy portval', SPY_portval.iloc[-1, 0]

    daily_rets_SPY = (SPY_portval / SPY_portval.shift(axis=0)) - 1
    daily_rets_SPY = daily_rets_SPY[1:]
    # print 'dayily return spy\n', daily_rets_SPY
    cum_ret_SPY = SPY_portval.iloc[-1, 0] / SPY_portval.iloc[0, 0] - 1  # cumulative return
    # print 'cun return spy', cum_ret_SPY

    avg_daily_ret_SPY = daily_rets_SPY.mean()[0]  # average daily return
    std_daily_ret_SPY = daily_rets_SPY.std()[0]  # standard deviation of daily return
    sharpe_ratio_SPY = ((daily_rets_SPY - rfr).mean()[0] / std_daily_ret_SPY) * (
                252 ** 0.5)  # sharpe ratio, adjusted for daily sampling
    #
    #
    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])
 			  		 			     			  	   		   	  			  	
if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    # compute_portvals()
    test_code()
