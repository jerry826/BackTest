# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: risk.py
@time: 2016/5/19 2:23
"""


import pandas as pd

class Risk():
	def __init__(self, date):
		self.date = date
		self.perf = pd.DataFrame()
		self.var = 0.0

	def analysis(self,perf,output=True):
		'''
		Risk analysis
		:param nav: hostorical nav
		:return:
		'''
		self.perf = perf
		self.perf['PnL'] = self.perf['nav'] - self.perf['nav'].shift(1)
		self.perf['cash_ratio'] = self.perf['cash']/self.perf['nav']
		# self.perf['std'] = self.perf['ret'].rolling_var(window=10)
		self.perf.to_csv('risk_analysis.csv')

		if output:
			pass


if __name__ == '__main__':
	pass