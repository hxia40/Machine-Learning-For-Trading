"""MC2-P1: Indicators
 			  		 			     			  	   		   	  			  	
Student Name: Hui Xia (replace with your name)
GT User ID: hxia40 (replace with your User ID)
GT ID: 903459648 (replace with your GT ID)
""" 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
import pandas as pd 			  		 			     			  	   		   	  			  	
import numpy as np 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import os 			  		 			     			  	   		   	  			  	
from util import get_data
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def author():
    return 'hxia40'  # replace tb34 with your Georgia Tech username.

def price_sma(start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31), symbols = ['JPM'], lookback = 14):
    stock_price = get_data(symbols, pd.date_range(start_date, end_date), addSPY = True, colname = 'Adj Close')
    # plot_data(stock_price)
    stock_price.fillna(method = 'ffill', inplace = True)
    stock_price.fillna(method='bfill', inplace=True)
    stock_price.drop(['SPY'], axis = 1, inplace = True)
    stock_price = stock_price/ stock_price.iloc[0, 0]

    '''Making first indicator: price/SMA'''

    sma = stock_price.copy().rolling(lookback).mean()
    p_to_sma = stock_price / sma
    return stock_price, sma, p_to_sma


'''Making 2nd indicator: RSI'''
def rsi(start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31), symbols = ['JPM'], lookback = 14):
    stock_price = get_data(symbols, pd.date_range(start_date, end_date), addSPY = True, colname = 'Adj Close')
    # plot_data(stock_price)
    stock_price.fillna(method='ffill', inplace=True)
    stock_price.fillna(method='bfill', inplace=True)
    stock_price.drop(['SPY'], axis=1, inplace=True)
    daily_return = stock_price - stock_price.shift(1)

    up_gain = daily_return.copy().where(daily_return >= 0, 0)    # fill daily returns that are not >= 0 as zero.
    up_gain = up_gain.rolling(lookback).sum()

    down_loss = - (daily_return.copy().where(daily_return < 0, 0))     # fill daily returns that are not < 0 as zero.
    down_loss = down_loss.rolling(lookback).sum()
    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi = 100 - 100 / (1 + rs)
    rsi[rsi == np.inf] = 100             # if RSI = infinite, change its value to 100
    return rsi

'''Making 3rd indicator: MFI'''

def mfi(start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31), symbols = ['JPM'], lookback = 14):

    stock_price = get_data(symbols, pd.date_range(start_date, end_date), addSPY = True, colname = 'Adj Close')
    stock_price.fillna(method='ffill', inplace=True)
    stock_price.fillna(method='bfill', inplace=True)
    stock_price.drop(['SPY'], axis=1, inplace=True)

    volume_number = get_data(symbols, pd.date_range(start_date, end_date), addSPY=True, colname='Volume')
    volume_number.fillna(method='ffill', inplace=True)
    volume_number.fillna(method='bfill', inplace=True)
    volume_number.drop(['SPY'], axis=1, inplace=True)

    money_flow = stock_price * volume_number
    # print money_flow
    daily_return = stock_price - stock_price.shift(1)

    up_gain = money_flow.copy().where(daily_return >= 0, 0)    # fill daily returns that are not >= 0 as zero.
    # print '=====mfi up gain =====\n', up_gain
    up_gain = up_gain.rolling(lookback).sum()

    down_loss = money_flow.copy().where(daily_return < 0, 0)     # fill daily returns that are not < 0 as zero.
    # print '=====mfi down loss =====\n', down_loss
    down_loss = down_loss.rolling(lookback).sum()

    mf = (up_gain / lookback) / (down_loss / lookback)

    mfi = 100 - 100 / (1 + mf)
    mfi[mfi == np.inf] = 100             # if MFI = infinite, change its value to 100
    return mfi


'''Making 4th indicator: vix'''
def vix(start_date = dt.datetime(2008,1,1), end_date = dt.datetime(2009,12,31), symbols = ['JPM']):
    stock_price = get_data(['$VIX'], pd.date_range(start_date, end_date), addSPY = True, colname = 'Adj Close')
    # plot_data(stock_price)
    stock_price.fillna(method = 'ffill', inplace = True)
    stock_price.fillna(method='bfill', inplace=True)
    stock_price.drop(['SPY'], axis=1, inplace=True)
    return stock_price
#
#
# def test_code():
#     pass

if __name__ == "__main__":
    # rsi()
    # mfi()
    plt.figure(figsize=(8, 4))
    plt.gcf().clear()

    stock_price, sma, p_to_sma = price_sma()
        # , upper_bb, lower_bb, bbp
    '''plotting Indicator 1: Price / SMA'''
    plt.plot(stock_price.index, stock_price,  label='Price')
    plt.plot(stock_price.index, sma, label='SMA')
    plt.plot(stock_price.index, p_to_sma, label='Price/SMA')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Indicator 1: Price / SMA')
    plt.legend(loc='best')
    plt.savefig('Figure1.png')
    plt.gcf().clear()
    #
    #
    '''plotting Indicator 2: RSI'''
    rsi_values = rsi()
    plt.plot(stock_price.index, stock_price * 50, label='Price')
    plt.plot(stock_price.index, rsi_values, label='RSI')

    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Indicator 2: RSI')
    plt.legend()
    plt.savefig('Figure2.png')
    plt.gcf().clear()

    '''plotting Indicator 3: MFI'''
    mfi_values = mfi()
    plt.plot(stock_price.index, stock_price * 50, label='Price')
    plt.plot(stock_price.index, mfi_values, label='MFI')

    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Indicator 3: MFI')
    plt.legend()
    plt.savefig('Figure3.png')
    plt.gcf().clear()
    #
    '''plotting Indicator 4: VIX'''
    vix_values = vix()
    plt.plot(stock_price.index, stock_price * 50, label='Price')
    plt.plot(stock_price.index, vix_values, label='VIX')

    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.title('Indicator 4: VIX')
    plt.legend()
    plt.savefig('Figure4.png')
    plt.gcf().clear()






