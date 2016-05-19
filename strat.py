# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: strat.py
@time: 2016/5/1 22:29
"""
import pandas as pd
import numpy as np


class Strat(object):
	'''
	Strat class. Calculate some technical signal using the historical data.
	'''

	def __init__(self, universe='allA', length=5, lag=1):
		'''

		:param name:
		:param universe: stock universe
		:param length: the time horizon need to calculate the signals
		:param lag: time lag, default 1
		'''
		self.hist_data = pd.DataFrame()
		self.length = length
		self.lag = lag
		self.date_list = []
		self.stock_list = []
		self.universe = universe

	def update(self, dt, df):
		'''

		:param date: date
		:param df: trade information
		:return:
		'''
		self.date_list.append(dt)  # add new date
		self.hist_data = pd.concat([self.hist_data, df])  # add new data
		# update the stock list
		self.stock_list = list(set(self.stock_list + list(df['sec_code'])))
		# clean the unused stock data
		if len(self.date_list) <= self.lag + self.length:
			pass
		else:
			self.hist_data = self.hist_data[self.date_list[-self.lag - self.length]:self.date_list[-1]]
		return None

	def gen_signal(self,data,name):
		'''
		Some simple signals for use
		:param data:
		:param name:
		:return:
		'''
		signal = dict()
		# demo1
		if name == 'demo':
			for stock in self.stock_list:
				signal[stock] = 1
		# close price signal
		elif name == 'hl':
			data = data.fillna(1)
			close = data.groupby('sec_code')['close'].mean()
			signal_temp = np.where(close > 10, 1, 0)*np.where(close < 15, 1, 0) + np.where(close > 16, -1, 0)
			for idx, stock in enumerate(close.index):
				if signal_temp[i] != 0:
					signal[stock] = signal_temp[idx]
		#
		elif name == 'mm':
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
		data_temp = self.__select_data(time_start=-length-self.lag, time_end=-1-self.lag, data_type='c')

		return data_temp.groupby('sec_code').mean()


	def MACD(self,length=5):
		'''
		MACD
		:param length: time length
		:return:
		'''
		pass

	def history(self,length=5,data_type='ohlc',universe=[]):
		'''
		History data
		:param length: time length
		:param type: 'ohlc
		:param universe:
		:return:
		'''

		x = self.__select_data(time_start=-length-self.lag,time_end=-1-self.lag,data_type=data_type)
		print(x.columns)
		return x


	def __select_data(self,time_start=0,time_end=1,data_type='ohlc'):
		'''
		Data selecting function
		:param time_start: 1,2,...,end
		:param time_end: 1,2,3....,end
		:param data_type: open, high, cow, close
		:return:
		'''
		config = {'o':'open',
				  'h':'high',
				  'l':'low',
				  'c':'close',
				  'a':'adjfactor',
				  'v':'AMT'}

		date_list = self.date_list[-time_start:-time_end]
		return self.hist_data[ [x in date_list for x in self.hist_data.index ]][[config[i] for i in data_type]]













def main():
	dd = datafeed(universe='allA')
	dd.initialize()
	st = Strat('hl', 'allA', 8, 2)
	for i in range(10):
		date, temp = dd.data_fetch()
		signal = Strat.update(date, temp)
	# print(signal)


if __name__ == '__main__':
	from datafeed import *
	dd = datafeed(universe='allA')
	dd.initialize()
	st = Strat('allA', 50, 3)
	for i in range(dd.time_length):
		date, temp = dd.data_fetch()
		print(date)
		print(len(temp))
		st.update(date, temp)
		print(st.history())

