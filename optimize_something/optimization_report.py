"""MC1-P2: Optimize a portfolio. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as sco


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), \
                       syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=True):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all.fillna(method='ffill')
    prices_all.fillna(method='bfill')
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case

    def sharpe_ratio(allocs):
        """Compute sharpe ratio using the equation of the sharpe ratio and the allocs of the assets

            Parameters
            ----------
            allocs: four-element list/array, all values between 0-1

            Returns sharpe ratio as a single real value
            """
        normed = prices_all / (prices_all.iloc[0])

        # calculating "each stock in syms"'s portfolio by multipling 'normalized stock price' with allocs
        alloced = normed[syms] * allocs
        port_val = alloced.sum(axis=1)

        # calculating daily return by dividing one day by the previous day minus 1
        daily_rets = port_val/port_val.shift(axis=0) - 1
        daily_rets = daily_rets[1:]
        rfr = 0.0
        # print '/nmean return'
        # print (daily_rets - rfr).mean()
        # print 'std'
        # print daily_rets.std()

        sr_in = ((daily_rets - rfr).mean() / daily_rets.std()) * (252 ** 0.5)  # sharpe ratio, adjusted for daily sampling
        # print 'sr'
        # print sr_in
        return sr_in * (-1)


    # call optimizer to minimize error function
    number_of_assets= len(syms)
    ini_guess = list(number_of_assets * [1.0 / number_of_assets])
    # print 'number_of_assets'
    # print number_of_assets
    # print 'ini_guess'
    # print ini_guess
    # print type(ini_guess)
    constraints = ({'type': 'eq', 'fun': lambda inputs: 1 - np.sum(inputs)})
    bounds = tuple((0, 1) for i in range(number_of_assets))
    result = sco.minimize(sharpe_ratio, ini_guess, method='SLSQP', bounds= bounds, constraints=constraints)
    allocs = result.x
    # print 'allocs'
    # print sum(allocs)
    # print 'result'
    # print result
    normed = prices_all / (prices_all.iloc[0])

    # calculating "each stock in syms"'s portfolio by multipling 'normalized stock price' with allocs
    alloced = normed[syms] * allocs
    port_val = alloced.sum(axis=1)
    prices_SPY = normed['SPY']
    print'/nport_val'
    print port_val

    # calculating daily return by dividing one day by the previous day minus 1
    daily_rets = port_val/port_val.shift(axis=0) - 1
    daily_rets = daily_rets[1:]
    rfr = 0.0
    cr = port_val[-1] / port_val[0] - 1  # cumulative return
    adr = daily_rets.mean()  # average daily return
    sddr = daily_rets.std()  # standard deviation of daily return
    sr = ((daily_rets - rfr).mean() / sddr) * (252 ** 0.5)  # sharpe ratio, adjusted for daily sampling

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot(title='Daily Portfolio Value and SPY', fontsize=12)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        plt.show()

        # plot_data(df_temp, title="Daily Portfolio Value and SPY", xlabel="Date", ylabel="Price")
        # plt.savefig('Optimization_report_2.png')
        # plt.plot(port_val.index.values, port_val, label='Portfolio')
        # plt.plot(port_val.index.values, prices_SPY, label='SPY')
        # # plt.gcf().subplots_adjust
        # plt.ylabel('Price')
        # plt.xlabel('Date')
        # plt.grid()
        # plt.title('Daily Portfolio Value and SPY')
        # plt.legend()
        # # plt.plot(range(252), port_val, label='xyz')
        # plt.savefig('Optimization_report_2.png')
        # # plt.show()

    return allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    # start_date = dt.datetime(2009, 1, 1)
    # end_date = dt.datetime(2010, 1, 1)
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM', 'JPM']
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    # allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, \
    #                                                     syms=symbols, \
    #                                                     gen_plot=False)
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=True)      

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
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
