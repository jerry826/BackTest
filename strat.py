# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: strat.py
@time: 2016/5/1 22:29
"""
import pandas as pd
import numpy as np

class strat(object):
	'''
	strat class. Calculate some technical signal using the historical data.
	'''

	def __init__(self, name='demo', universe='allA', length=5, lag=1):
		'''

		:param name:
		:param universe: stock universe
		:param length: the time horizon need to calculate the signals
		:param lag: time lag, default 1
		'''
		self._hist_data = pd.DataFrame()
		self._length = length
		self._name = name
		self._lag = lag
		self._date_list = []
		self._stock_list = []

	def update(self, date, df):
		'''

		:param date: date
		:param df: trade information
		:return:
		'''
		self._date_list.append(date)  # add new date
		self._hist_data = pd.concat([self._hist_data, df])  # add new data
		# update the stock list
		self._stock_list = list(set(self._stock_list + list(df['sec_code'])))
		# clean the unused stock data
		if len(self._date_list) <= self._lag + self._length:
			pass
		else:
			self._hist_data = self._hist_data[self._date_list[-self._lag - self._length]:self._date_list[-1]]

		print('data length : ' + str(len(set(self._hist_data.index))))
		# calculate the signals
		# if the data is not enough, there is no signal
		# if len(self._date_list) < self._lag + self._length:
		# 	signal = dict()
		# # using gen_signal function to generate signals
		# else:
		# 	temp = self._hist_data[self._date_list[-self._length - self._lag]:self._date_list[-self._lag - 1]]
		# 	signal = self.__gen_signal(temp)
		# 	print('signal data length : ' + str(len(set(temp.index))))
		return None

	def __gen_signal(self, data):
		signal = dict()
		# demo1
		if self._name == 'demo':
			for stock in self._stock_list:
				signal[stock] = 1
		# close price signal
		elif self._name == 'hl':
			data = data.fillna(1)
			close = data.groupby('sec_code')['close'].mean()
			signal_temp = np.where(close > 10, 1, 0) * np.where(close < 15, 1, 0) + np.where(close > 16, -1, 0)
			for i, stock in enumerate(close.index):
				if signal_temp[i] != 0:
					signal[stock] = signal_temp[i]

		elif self._name == 'mm':
			close = data.groupby('sec_code')['close'].mean()
			signal = pd.Series(np.where(close.rank(pct=True) > 0.95, 1, -1), index=close.index)
			signal = signal.to_dict()
		return signal

	def MA(self,length=5,price='close'):
		'''
		Moving average
		:param length: time length
		:param price:
		:return:
		'''
		pass

	def MACD(self,length=5):
		pass

	def history(self,length=5,type='ohlc'):
		pass










def main():
	dd = datafeed(universe='allA')
	dd.initialize()
	st = strat('hl', 'allA', 8, 2)
	for i in range(10):
		date, temp = dd.data_fetch()
		signal = strat.update(date, temp)
	# print(signal)


if __name__ == '__main__':
	from datafeed import *
	dd = datafeed(universe='allA')
	dd.initialize()
	st = strat('demo', 'allA', 50, 3)
	for i in range(1000):
		date, temp = dd.data_fetch()
		signal = st.update(date, temp)
