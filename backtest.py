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
from risk import *

class BackTest(object):
	'''
	Back-test platform
	'''
	def __init__(self, model_name='demo', begin_time="2011-02-01", end_time="2015-11-01", begin_equity=100000000000, fee=0.003,
	             path=r"C:\Users\Administrator\Desktop\allA",
	             universe='allA',freq=5,length=5, lag=1, short=False,price_type='close'):
		self.path = path
		self.begin_equity = begin_equity
		self.freq = freq
		self.name = model_name
		self.__begin_date = begin_time
		self.__end_date = end_time
		self.fee = fee
		self.lag = lag
		self.universe = universe
		self.datafeed = datafeed(universe = self.universe,
		                           begin_date = self.__begin_date,
		                           end_date = self.__end_date,
		                           path=path)
		self.datafeed.initialize()
		self.length = length
		self.strat = Strat(universe, length, lag)
		self.broker = Broker(self.fee,price_type,short, begin_equity,begin_time)
		self.analyzer = Analyzer(date = begin_time)
		self.risk = Risk(date = begin_time)


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
		for date_id in range(0,self.lag+self.length):
			dt, trading_data = self.datafeed.data_fetch()
			self.strat.update(dt, trading_data)
		for date_id in (range(self.lag+self.length,self.datafeed.time_length)):
			# get daily data
			dt, trading_data = self.datafeed.data_fetch()
			# add the data into broker
			self.broker.update_info(dt, trading_data)
			self.strat.update(dt, trading_data)
			# get the used signals and make orders
			if date_id%self.freq == 1 and date_id > (self.length+self.lag):
				self.handle_data()
			# execute the orders
			self.broker.execute(output=False)
			# update the portfolio value at close price
			self.broker.update_value()


		pos, close, nav, cash, trade = self.broker.get_position_report()

		# perf analysis
		self.analyzer.analysis(nav, pos, close, cash, trade)
		summary = self.analyzer.cal()
		self.analyzer.plot()
		self.analyzer.to_csv()

		# risk analysis
		self.risk.analysis(summary)
		return pos, close, nav, trade



	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''
		universe = self.broker.get_universe()
		#for symbol in universe:
		#	self.broker.order_pct(symbol, 0.001)
		self.broker.order_pct_to('000001.SZ', -0.5)

def main():
	bt = BackTest('mm', begin_time="2013-04-01", end_time="2013-11-01",path='E:\\data',universe = ['000001.SZ', '000019.SZ'],short=True)
	pos, close, nav , trade = bt.start()

if __name__ == '__main__':
	main()


