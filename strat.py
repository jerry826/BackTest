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

	def __init__(self, name='demo', universe='allA', lag=5):
		'''

		'''
		self.__hist_data = pd.DataFrame()
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
		if len(self.__date_list) <= self.__lag:
			signal = 0
		else:
			self.__hist_data = self.__hist_data[self.__date_list[-self.__lag]:self.__date_list[-1]]

		# calculate the signals
		## data is not enough, so there is no signal
		if len(self.__date_list) < self.__lag:
			signal = dict()
			for stock in self.__stock_list:
				signal[stock] = 0
		## using gen_signal function to generate signals
		else:
			signal = self.__gen_signal()
		return signal

	def __gen_signal(self):
		signal = dict()

		# demo
		if self.__name == 'demo':
			for stock in self.__stock_list:
				signal[stock] = 1
		# close price signal
		elif self.__name == 'hl':
			self.__hist_data = self.__hist_data.fillna(1)
			close = self.__hist_data.groupby('sec_code')['close'].mean()
			signal_temp = np.where(close > 10, 1, 0)
			print(len(close))
			print(len(self.__stock_list))
			print(len(signal_temp))

			assert (len(signal_temp) == len(close))
			for i, stock in enumerate(self.__stock_list):
				signal[stock] = signal_temp[i]

		return signal


def main():
	dd = datafeed(universe='allA')
	dd.initialize()
	st = strat('demo', 'allA', 5)
	for i in range(10):
		date, temp = dd.data_fetch()
		signal = strat.update(date, temp)
	# print(signal)


if __name__ == '__main__':
	from datafeed import *

	dd = datafeed(universe='allA')
	dd.initialize()
	st = strat('hl', 'allA', 5)
	for i in range(1000):
		date, temp = dd.data_fetch()
		signal = st.update(date, temp)
		print(signal['002002.SZ'])
