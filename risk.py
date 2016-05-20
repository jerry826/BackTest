# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: risk.py
@time: 2016/5/19 2:23
"""


import pandas as pd
import numpy as np
import scipy.stats as stats

class Risk():
	def __init__(self, date):
		self.date = date
		self.risk = pd.DataFrame()
		self.var = 0.0


	def cal_draw_down_duration(self,drawdown):
		'''
		Calculate draw down duration
		:param drawdown: drawdown series
		:return: draw down duration
		'''
		duration = []
		length = 0
		for i in range(len(drawdown)):
			if drawdown[i] == 0:
				duration.append(length)
				length = 0
			else:
				length += 1
				duration.append(length)
		return duration

	def analysis(self,perf, output=True):
		'''
		Risk analysis
		:param perf: historical nav
		:param output: whether print the result
		:return:
		'''
		self.risk = perf
		# PnL Profit and Loss
		self.risk['PnL'] = self.risk['nav'] - self.risk['nav'].shift(1)
		# cash ratio
		self.risk['cash_ratio'] = self.risk['cash']/self.risk['nav']
		# daily volatility and annulized volatility
		self.risk['daily_volatility'] = self.risk['ret'].rolling(window=60).var()
		self.risk['annulized_volatility'] = self.risk['daily_volatility']*np.sqrt(252)
		# 30 day rolling return
		self.risk['ret_30d'] = self.risk['ret'].rolling(window=60).mean()

		# calculate VaR
		self.risk['unleverage_ret'] = self.risk['ret']/(1-self.risk['cash_ratio'])
		self.risk['unleverage_ret_30d'] = self.risk['unleverage_ret'].rolling(window=30).mean()
		self.risk['unleverage_volatiliy_30d'] = self.risk['unleverage_ret'].rolling(window=30).var()

		# VaR value at risk
		ret = stats.norm(0,1).ppf(1-0.999)
		self.risk['VaR_return'] = self.risk['unleverage_ret_30d'] + np.sqrt(self.risk['unleverage_volatiliy_30d'])*ret
		self.risk['VaR_0.999'] = (self.risk['nav']-self.risk['cash'])*self.risk['VaR_return']

		# max draw down duration
		self.risk['max_draw_down_duration'] = self.cal_draw_down_duration(self.risk.loc[:,'draw_down'])
		self.risk['max_draw_down_duration'] = self.risk['max_draw_down_duration'].cummax()

		# leverage
		self.risk['leverage'] = (self.risk['nav']-self.risk['cash'])/self.risk['nav']

		avg_pnl = self.risk['PnL'].mean()
		avg_cash_ratio = self.risk['cash_ratio'].mean()
		avg_leverage = self.risk['leverage'].mean()
		winning_rate = np.where(self.risk['ret']>0, 1, 0).sum()/len(self.risk)
		if output:
			print('--------------Rsik Analysis----------------')
			print('Average PnL : %0.1f' % avg_pnl)
			print('Average cash ratio : %0.3f' % avg_cash_ratio)
			print('Average leverage : %0.3f' % avg_leverage)
			print('Winning rate : %0.3f' % winning_rate)
			print('--------------------End--------------------')
		# save the result
		self.risk = self.risk.loc[:, ['nav', 'PnL', 'cash_ratio', 'annulized_volatility',
		                              'daily_volatility', 'VaR_0.999', 'max_draw_down_duration', 'leverage']]
		self.risk.to_csv('risk_analysis.csv')
		return self.risk

if __name__ == '__main__':
	pass