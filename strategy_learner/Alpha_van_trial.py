from alpha_vantage.timeseries import TimeSeries

import matplotlib.pyplot as plt
ts = TimeSeries(key='47Q1IUB8QM5SP6IK', output_format='pandas', indexing_type='date') # indexing_type='date' or integer'
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday(symbol='SPY',interval='1min', outputsize='full')
print(data.tail(2))
# print data
# print '=========meta_data===\n'
# print meta_data
data['4. close'].plot()
plt.show()