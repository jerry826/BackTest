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

	def analysis(self,nav,output=True):
		'''
		Risk analysis
		:param nav: hostorical nav
		:return:
		'''
		self.data = pd.DataFrame(nav)




		if output:
			pass


if __name__ == '__main__':
	pass