# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: backtest.py
@time: 2016/4/30 14:03
"""

from strat import *
from broker import *
from portfolio import *
from datafeed import *
from analyzer import *
from tqdm import tqdm

class BackTest(object):
	'''
	Back-test platform

	'''

	def __init__(self, model_name, begin_time="2011-02-01", end_time="2015-11-01", begin_equity=100000000, fee=0.003,
	             position=0.7, extra_position=0.1, path=r"C:\Users\Administrator\Desktop\alpha_output\allA",
	             universe='allA'):
		self.__name=model_name
		self.__begin_date=begin_time
		self.__end_date=end_time
		self.path=path
		self.begin_equity=begin_equity
		self.__fee=fee
		self.__position = position
		self.extra_position=extra_position
		self.__universe=universe


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
		self.__datafeed = datafeed(self.__universe, self.__begin_date, self.__end_date)
		self.__datafeed.initialize()
		self.__length = self.__datafeed.time_length
		self.__strat = strat(self.__name, 'allA', 7, 2)
		self.__broker = broker(self.__fee, 0.002)
		self.__port = portfolio(self.begin_equity)

		for i in tqdm(range(0, self.__length)):
			date, temp = self.__datafeed.data_fetch()
			signal = self.__strat.update(date, temp)
			transaction_volumn, transaction_fee, cur_positison, end_equity_balance, delta_cash = self.__broker.order(
				signal, self.__port.cur_position, self.__port.cur_balance, temp)
			self.__port.update_port(cur_positison, end_equity_balance, transaction_fee, delta_cash, temp, date)
			print('------------------------')
			print(date)
			print('end value: ' + str(end_equity_balance))
			print('fee: ' + str(transaction_fee))
			print('delta cash: ' + str(delta_cash))

		self.__analyzer = analyzer(self.__port.hist_log)
		self.__analyzer.cal()
		self.__analyzer.plot()




def main():
	bt = BackTest('test')
	bt.start()

if __name__ == '__main__':
	bt = BackTest('demo', begin_time="2012-02-01", end_time="2013-11-01")
	bt.start()
