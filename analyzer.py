# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: analyzer.py
@time: 2016/5/5 16:18
"""

import pandas as pd
import numpy as np


class analyzer(object):
	def __init__(self, perf):
		self.__data = pd.DataFrame(list(perf.values()),columns=['balance'],index=perf.keys())


	def cal(self):
		# self.__data.loc[:, 'ret'] = self.__data.loc[:, 'balance'].pct_change()
		self.__data.loc[:, 'ret'] = np.log(self.__data.loc[:, 'balance']/self.__data.loc[:, 'balance'].shift(1))
		self.__data.loc[:, 'cum_ret'] = self.__data.loc[:, 'ret'].cumsum()

		# self.__data.loc[:, 'draw_down'] = -(
		# (self.__data.loc[:, 'cum_ret'] + 1).cummax() - (1 + self.__data.loc[:, 'cum_ret'])) / (
		#                                  1 + self.__data.loc[:, 'cum_ret'].cummax())

		self.__data.loc[:, 'draw_down'] = self.__data.loc[:, 'balance']/self.__data.loc[:, 'balance'].cummax()-1

		#self.__data.loc[:, 'turnover'] = self.__data.loc[:, 'trade volumn'] / self.__data.loc[:, 'balance']
		# calculate the peerformance index
		sharpe_ratio = np.sqrt(52) * (self.__data.loc[:, 'ret']).mean() / (self.__data.loc[:, 'ret']).std()
		year_ret = self.__data.loc[:, 'ret'].mean() * 52
		max_draw_down = (self.__data.loc[:, 'draw_down']).min()
		year_volatility = np.sqrt(52) * self.__data.loc[:, 'ret'].std()
		#average_turnover = self.__data.loc[:, 'turnover'].mean()
		# output the index
		print('Sharpe ratio %0.3f' % sharpe_ratio)
		print('Average year return %0.3f' % year_ret)
		print('Maximum draw down %0.3f' % max_draw_down)
		print('Annualized return volatility %0.3f' % year_volatility)
		#print('Average turn over %0.3f' % average_turnover)
		return self.__data

	def plot(self):
		self.__data.loc[:, ['cum_ret', 'draw_down']].plot()

		return None
	# self.__data.loc[:,'ret'].plot()


if __name__ == '__main__':
	# az = analyzer(p.hist_log)
	# data = az.cal()
	# az.plot()
	data = pd.read_csv('balance.csv')
	az = analyzer(data)
	data = az.cal()
	az.plot()
