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

		self.cash = pd.DataFrame()
		self.trade = pd.DataFrame()

	def analysis(self, nav, pos, close, cash, trade):
		self.data = pd.DataFrame(nav)
		self.data.columns = ['nav']
		self.data = self.data.sort_index()

		self.pos = pos
		self.close = close

		self.data[trade.columns] = trade
		self.data['cash'] = cash


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

		self.data.loc[:, 'turnover'] = self.data.loc[:, 'trade_volume'] / self.data.loc[:, 'nav']

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
		'''
		ploting
		:return:
		'''
		self.data.loc[:, ['cum_ret', 'draw_down']].plot()
		return None

	def to_csv(self):
		'''
		Save the result
		:return:
		'''
		self.pos.to_csv('position_report.csv')
		self.close.to_csv('close_report.csv')
		self.data.to_csv('performance_report.csv')
		return None
	# self.__data.loc[:,'ret'].plot()


if __name__ == '__main__':
	# az = analyzer(p.hist_log)
	# data = az.cal()
	# az.plot()
	data = pd.read_csv('balance.csv')
	az = Analyzer(data)
	data = az.cal()
	az.plot()
