# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: strat.py
@time: 2016/5/1 22:29
"""
import pandas as pd
import numpy as np

class strat(object):
	'''
	strat
	'''

	def __init__(self, name='demo', universe='allA', length=5, lag=1):
		'''

		'''
		self.__hist_data = pd.DataFrame()
		self.__length = length
		self.__name = name
		self.__lag = lag
		self.__date_list = []
		self.__stock_list = []

	def update(self, date, df):
		self.__date_list.append(date)  # add new date
		self.__hist_data = pd.concat([self.__hist_data, df])  # add new data
		# update the stock list
		self.__stock_list = list(set(self.__stock_list + list(df['sec_code'])))
		# clean the unused stock data
		if len(self.__date_list) <= self.__lag + self.__length:
			pass
		else:
			self.__hist_data = self.__hist_data[self.__date_list[-self.__lag - self.__length]:self.__date_list[-1]]

		print('data length : ' + str(len(set(self.__hist_data.index))))
		# calculate the signals
		## if the data is not enough, there is no signal
		if len(self.__date_list) < self.__lag + self.__length:
			signal = dict()
		## using gen_signal function to generate signals
		else:
			temp = self.__hist_data[self.__date_list[-self.__length - self.__lag]:self.__date_list[-self.__lag - 1]]
			signal = self.__gen_signal(temp)
			print('signal data length : ' + str(len(set(temp.index))))
		return signal

	def __gen_signal(self, data):
		signal = dict()
		# demo
		if self.__name == 'demo':
			for stock in self.__stock_list:
				signal[stock] = 1
		# close price signal
		elif self.__name == 'hl':
			data = data.fillna(1)
			close = data.groupby('sec_code')['close'].mean()
			signal_temp = np.where(close > 10, 1, 0) * np.where(close < 15, 1, 0) + np.where(close > 16, -1, 0)
			for i, stock in enumerate(close.index):
				if signal_temp[i] != 0:
					signal[stock] = signal_temp[i]
		return signal


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
