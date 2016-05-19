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
		self.nav = pd.DataFrame()
		self.var = 0.0

	def analysis(self,nav,output=True):
		'''
		Risk analysis
		:param nav: hostorical nav
		:return:
		'''
		self.nav = pd.DataFrame(nav)
		self.nav.columns = ['nav']
		self.nav = self.nav.sort_index()
		self.nav['PnL'] = self.nav['nav'] - self.nav['nav'].shift(1)
		self.nav['ret'] = self.nav['PnL'].pct_change()

		self.var = self.nav['ret'].var()


		if output:
			pass


if __name__ == '__main__':
	pass