"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=True):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value

    '''HX code start'''
    # port_val = prices_SPY # add code here to compute daily portfolio values
    # print prices_all[syms].iloc[0]

    # Normalizing stock prices
    normed = prices_all / (prices_all.iloc[0])
    # print normed

    # calculating "each stock in syms"'s portfolio by multipling 'normalized stock price' with allocs
    alloced = normed[syms] * allocs *sv
    port_SPY_only = normed['SPY'] * 1 *sv
    # print alloced
    # print port_SPY_only

    #calculating daily portfolio by adding all holding up together
    port_val = alloced.sum(axis = 1)
    # print port_val

    # calculating daily return by dividing one day by the previous day minus 1
    daily_rets = port_val.shift(axis = 0)/ port_val-1
    daily_rets = daily_rets[1:]
    # print 'daily_rets'
    # print daily_rets
    '''HX code end'''

    # Get portfolio statistics (note: std_daily_ret = volatility)

    '''HX code start'''
    # cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    cr = port_val[-1]/port_val[0] - 1   # cumulative return
    adr = daily_rets.mean()             # average daily return
    sddr = daily_rets.std()             # standard deviation of daily return
    sr = ((daily_rets - rfr).mean()/sddr)*(252 ** 0.5)              #  sharpe ratio, adjusted for daily sampling
    print cr
    print adr
    print sddr
    print sr
    '''HX code end'''
    # print port_val.index.values
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:

        # add code to plot here
        '''HX code start'''
        # df_temp = pd.concat([port_val, port_SPY_only], keys=['Portfolio', 'SPY'], axis=1)
        plt.plot(port_val.index.values, port_val/sv, label='Portfolio')
        plt.plot(port_val.index.values, port_SPY_only/sv, label='SPY')
        plt.gcf().subplots_adjust
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.grid()
        plt.title('Daily Portfolio Value and SPY')
        plt.legend()
        # plt.plot(range(252), port_val, label='xyz')
        # plt.savefig('access_portfolio.png')
        plt.show()
        # pass
    '''HX code end'''

    # Add code here to properly compute end value
    '''HX code start'''
    # ev = sv
    ev = port_val[-1]
    '''HX code end'''

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
