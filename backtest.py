# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: backtest.py
@time: 2016/4/30 14:03
"""

from strat import *
from broker import *
from datafeed import *
from analyzer import *

class BackTest(object):
	'''
	Back-test platform
	'''
	def __init__(self, model_name, begin_time="2011-02-01", end_time="2015-11-01", begin_equity=100000000000, fee=0.003,
	             position=0.7, extra_position=0.1, path=r"C:\Users\Administrator\Desktop\alpha_output\allA",
	             universe='allA',freq=5):
		self.path = path
		self.begin_equity = begin_equity
		self.freq = freq
		self.__name = model_name
		self.__begin_date = begin_time
		self.__end_date = end_time
		self.__fee = fee
		self.__position = position
		self.__universe = universe
		self.__datafeed = datafeed(self.__universe, self.__begin_date, self.__end_date)
		self.__datafeed.initialize()
		self.__length = self.__datafeed.time_length
		self.__strat = Strat(self.__name, 'allA', 7, 2)
		self.__broker = Broker(self.__fee,'vwap',False, begin_equity,begin_time)
		self.__analyzer = Analyzer(date = "2011-02-01")

	@property
	def begin_date(self):
		return self.__begin_date

	@begin_date.setter
	def begin_date(self, dt):
		if '-' not in dt:
			raise ValueError("Date format must be\"%Y-%m-%d\"" )
		self.__begin_date = dt

	@property
	def end_date(self):
		return self.__end_date

	@end_date.setter
	def end_date(self, dt):
		if '-' not in dt:
			raise ValueError("Date format must be\"%Y-%m-%d\"" )
		self.__end_date = dt

	def start(self):
		# main loop
		for i in (range(0,self.__datafeed.time_length)):
			# get daily data
			dt, trading_data = self.__datafeed.data_fetch()
			# add the data into broker
			self.__broker.update_info(dt, trading_data)
			# get the used signals and make orders
			if i%self.freq == 1:
				self.handle_data()
			# execute the orders
			self.__broker.execute()
			# update the portfolio value at close price
			self.__broker.update_value()
			self.__strat.update(dt, trading_data)
			print('------------------------')
			print(dt)
		pos,close,nav = self.__broker.get_position_report()

		self.__analyzer.analysis(nav, pos, close)
		self.__analyzer.cal()
		self.__analyzer.plot()
		self.__analyzer.to_csv()
		return pos, close, nav

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''
		universe = self.__broker.get_universe()
		for symbol in universe:
			self.__broker.order_pct_to(symbol, 1/len(universe))


def main():
	bt = BackTest('mm', begin_time="2013-02-01", end_time="2015-11-01")
	pos, close, nav = bt.start()

if __name__ == '__main__':
	% time main()


