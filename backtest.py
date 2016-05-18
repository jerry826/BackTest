# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: backtest.py
@time: 2016/4/30 14:03
"""

from strat import *
from broker import *
from portfolio import *
from datafeed import *
from analyzer import *

class BackTest(object):
	'''
	Back-test platform
	'''
	def __init__(self, model_name, begin_time="2011-02-01", end_time="2015-11-01", begin_equity=100000000, fee=0.003,
	             position=0.7, extra_position=0.1, path=r"C:\Users\Administrator\Desktop\alpha_output\allA",
	             universe='allA'):
		self.__name = model_name
		self.__begin_date = begin_time
		self.__end_date =end_time
		self.path = path
		self.begin_equity = begin_equity
		self.__fee = fee
		self.__position = position
		self.extra_position=extra_position
		self.__universe=universe
		self.__datafeed = datafeed(self.__universe, self.__begin_date, self.__end_date)
		self.__datafeed.initialize()
		self.__length = self.__datafeed.time_length
		self.__strat = strat(self.__name, 'allA', 7, 2)
		self.__broker = broker(self.__fee,'vwap')

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
		# main loop
		for i in (range(0,30)):
			# get daily data
			date, temp = self.__datafeed.data_fetch()
			# add the data into broker
			self.__broker.update_info(date, temp)
			# get the used signals and make orders
			self.handle_data()
			# execute the orders
			self.__broker.execute()
			# update the portfolio value at close price
			self.__broker.update_value()
			self.__strat.update(date, temp)
			print('------------------------')
			print(date)
			# print('end value: ' + str(end_equity_balance))
			# print('fee: ' + str(transaction_fee))
			# print('delta cash: ' + str(delta_cash))

		perf = self.__broker.get_hist_perf()
		print(perf)
		self.__analyzer = analyzer(perf)
		self.__analyzer.cal()
		self.__analyzer.plot()

		pos,close = self.__broker.get_position_report()

		return

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''
		universe = self.__broker.get_universe()
		print(universe)
		for symbol in universe[0:10]:
			self.__broker.order_pct(symbol, 0.005)


def main():
	bt = BackTest('test')
	bt.start()

if __name__ == '__main__':
	bt = BackTest('mm', begin_time="2012-02-01", end_time="2013-11-01")
	bt.start()

