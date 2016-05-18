# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: analyzer.py
@time: 2016/5/5 16:18
"""

import pandas as pd
import numpy as np


class Analyzer(object):
	def __init__(self, date):
		self.date = date
		self.data = pd.DataFrame()
		self.pos = pd.DataFrame()
		self.close = pd.DataFrame()

	def analysis(self, nav, pos, close):
		self.data = pd.DataFrame(nav)
		self.data.columns = ['nav']
		self.data = self.data.sort_index()
		self.pos = pos
		self.close = close

	def cal(self, log_return = True):
		if log_return:

			self.data.loc[:, 'ret'] = np.log(self.data.loc[:, 'nav']/self.data.loc[:, 'nav'].shift(1))
			self.data.loc[:, 'cum_ret'] = self.data.loc[:, 'ret'].cumsum()
			self.data.loc[:, 'draw_down'] = self.data.loc[:, 'nav']/self.data.loc[:, 'nav'].cummax()-1
		else:
			self.data.loc[:, 'ret'] = self.data.loc[:, 'balance'].pct_change()
			self.data.loc[:, 'draw_down'] = -(
			(self.data.loc[:, 'cum_ret'] + 1).cummax() - (1 + self.data.loc[:, 'cum_ret'])) / (
			                                 1 + self.data.loc[:, 'cum_ret'].cummax())

		#self.__data.loc[:, 'turnover'] = self.__data.loc[:, 'trade volumn'] / self.__data.loc[:, 'balance']

		# calculate the peerformance index
		sharpe_ratio = np.sqrt(52) * (self.data.loc[:, 'ret']).mean() / (self.data.loc[:, 'ret']).std()
		year_ret = self.data.loc[:, 'ret'].mean() * 52
		max_draw_down = (self.data.loc[:, 'draw_down']).min()
		year_volatility = np.sqrt(52) * self.data.loc[:, 'ret'].std()
		#average_turnover = self.__data.loc[:, 'turnover'].mean()
		# output the index
		print('Sharpe ratio %0.3f' % sharpe_ratio)
		print('Average year return %0.3f' % year_ret)
		print('Maximum draw down %0.3f' % max_draw_down)
		print('Annualized return volatility %0.3f' % year_volatility)
		#print('Average turn over %0.3f' % average_turnover)
		return self.data

	def plot(self):
		self.data.loc[:, ['cum_ret', 'draw_down']].plot()

	def to_csv(self):
		self.pos.to_csv('pos.csv')
		self.close.to_csv('close.csv')
		self.data.to_csv('nav.csv')
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
