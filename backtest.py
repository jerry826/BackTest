# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: backtest.py
@time: 2016/4/30 14:03
"""

from datafeed import *



class BackTest(object):
	'''
	Back-test platform

	'''

	def __init__(self, model_name, begin_time="2010-02-01", end_time="2015-11-01", begin_equity=100000000, fee=0.003,
	             position=0.7, extra_position=0.1, path=r"C:\Users\Administrator\Desktop\alpha_output\allA",
	             universe='zz500'):
		self.__name=model_name
		self.__begin_date=begin_time
		self.__end_date=end_time
		self.path=path
		self.begin_equity=begin_equity
		self.__fee=fee
		self.position=position
		self.extra_position=extra_position
		self.__universe=universe
		self.__datafeed = datafeed(universe, begin_time, end_time)
		self.__datafeed.initialize()

	@property
	def begin_date(self):
		return self.__begin_date
	@begin_date.setter
	def begin_date(self,date):
		if '-' not in date:
			raise ValueError("Date format must be\"%Y-%m-%d\"" )
		self.__begin_date=date
	@property
	def end_date(self):
		return self.__end_date
	@end_date.setter
	def end_date(self,date):
		if '-' not in date:
			raise ValueError("Date format must be\"%Y-%m-%d\"" )
		self.__end_date=date

	def start(self):
		pass


def main():
	bt = BackTest('test')

if __name__ == '__main__':
	pass
