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
from util import get_data, plot_data

def author():
    return 'hxia40'  # replace tb34 with your Georgia Tech username.
 			  		 			     			  	   		   	  			  	
def compute_portvals(orders_file = "./orders/orders-01.csv", start_val = 100000, commission=9.95, impact=0.005):

    '''read in the orders and set them in Date order'''
    if isinstance(orders_file, pd.DataFrame):
        orders_df = orders_file
    else:
        orders_df = pd.read_csv(orders_file, parse_dates=True, na_values=['nan'])
        orders_df['Date'] = pd.to_datetime(orders_df['Date'])
        orders_df.sort_values('Date', axis=0, ascending=True, inplace=True, na_position='last')

        orders_df.set_index('Date', inplace=True)
    # print '======orders=======\n', orders_df

    '''read in the value of the stocks mentioned in the order dataframe and the time'''
    # print "====orders_df====\n", orders_df

    start_date = orders_df.index.values[0]
    end_date = orders_df.index.values[-1]

    symbols = [orders_df.columns[0]]
    # print '=====symbols====\n', symbols
    stock_price = get_data(symbols, pd.date_range(start_date, end_date))
    stock_price.drop(['SPY'], axis=1, inplace=True)
    stock_price['Cash'] = 1
    # print '===========stock_price=======\n', stock_price

    '''make 'holdings dataframe' according to the 'stock price dataframe' and the 'order drataframe' generated above'''

    holdings = pd.DataFrame(index=stock_price.index, columns=stock_price.columns)
    holdings = holdings.fillna(0)
    holdings['Cash'] = 0
    holdings['Cash'][0] = start_val

    for date, rows_orders in orders_df.iterrows():      # getting the index (date) from orders_df

        if rows_orders[0] != 0:
            holdings.loc[date, symbols[0]] += rows_orders[0]
            holdings.loc[date, 'Cash'] -= (stock_price.loc[date, symbols[0]]) * rows_orders[0]
            holdings.loc[date, 'Cash'] -= commission
            holdings.loc[date, 'Cash'] -= abs((stock_price.loc[date, symbols[0]] * impact) * rows_orders[0])

            # print 'impact cost:', abs((stock_price.loc[date, symbols[0]] * impact) * rows_orders[0])

    for i in range(0, len(holdings)):
        if i > 0:
            holdings.iloc[i, :] += holdings.iloc[i - 1, :]

    # print '==============holdings============\n', holdings

    '''make 'portvals dataframe' by summing everything up.'''

    portvals = (holdings * stock_price).sum(axis=1)
    # portvals = portvals.to_frame()
    return portvals

def test_code(verbose=0):
    pass

if __name__ == "__main__":
    test_code()
    # if sys.argv[-1] == 'print_data':
    #     test_code(verbose=1)
    # else:
    #     test_code()
