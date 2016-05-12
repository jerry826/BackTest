# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: broker.py
@time: 2016/5/4 21:53
"""

import math
from collections import defaultdict

import numpy as np
import pandas as pd

from portfolio import portfolio

class broker(object):
	'''

	'''
	def __init__(self,commission=0.002,price_type='vwap',short=False):
		'''

		:param commission: commission fee
		:param price_type: vwap or close or open
		:param short: True or False
		'''
		self.commission = commission
		self.price = price_type
		self.short = short


		self.port = portfolio(begin_equity=1000000,commission=commission)
		self.order_list = []
		self.order_count = 0
		self.execute_index = False

		self.trade_volume = 0.0
		self.trade_cost = 0.0
		self.trade_log = defaultdict()


	def execute(self):
		if not self.execute_index:
			# execute the orders
			for order in self.order_list:
				info = Trade_info(cash=self.port.cash,
				                  symbol=order.symbol,
				                  price=self.trading_data.loc[order.symbol,'adj_trade'],
				                  maxupordown=self.trading_data.loc[order.symbol,'maxupordown'],
				                  status=self.trading_data.loc[order.symbol,'trade_status'],
				                  portfolio_value=self.port.portfolio_value,
				                  position=self.port.positions[order.symbol],
				                  commission=self.commission,
				                  short=self.short)
				# validate the orders
				order.validate(info)
				self.port.update(order)
				self.trade_volume += abs(100*order.valid_price*order.valid_volume*(1+self.commission))
				self.trade_cost += abs(100*order.valid_price*order.valid_volume*self.commission)
				print(order)

			# record the trade results
			self.trade_log[self.date] = {'trade_volume':self.trade_volume, 'trade_cost': self.trade_cost, 'order num':self.order_count}
			self.execute_index = True
			self.trade_summary()

		else:
			print('You cannot execute the orders twice in a single trade day ')

	def trade_summary(self):
		print('========================================================')
		print('Date: ' +str(self.date))
		print('Trade volume %0.1f'%self.trade_volume)
		print('Port cash %0.1f'%self.port.cash)
		print(self.port.positions)
		print('========================================================')


	def update_value(self):
		pass

	def update_info(self,date,trading_data):
		'''
		Get the new trading data and update the information
		:param date: trading date
		:param trading_data: trading data
		:return: none
		'''
		# add trading data
		self.trading_data = trading_data.reset_index().set_index('sec_code')
		self.trading_data.loc[:,'adj_close'] = self.trading_data.loc[:,'close']*self.trading_data.loc[:,'adjfactor']
		self.trading_data.loc[:,'adj_trade'] = (self.trading_data.loc[:,self.price]*self.trading_data.loc[:,'adjfactor'])
		self.trade_info = (self.trading_data.loc[:,['adj_close','adj_trade','trade_status','maxupordown']]).to_dict(orient='index')
		self.date = date

		# reset the daily trading variable
		self.transaction_cost = 0.0
		self.trade_volume = 0.0
		self.order_count = 0.0
		self.execute_index = False
		self.order_list = []

	def order(self, symbol, amount):
		'''

		:param symbol: stock symbol
		:param amount: order size
		:return:
		'''

		self.order_list.append(Order_num(symbol,amount))
		self.order_count += 1

	def order_to(self,symbol,amount):
		'''

		:param symbol: stock symbol
		:param amount: target position
		:return: none
		'''
		self.order_list.append(Order_num_to(symbol, amount))
		self.order_count += 1

	def order_pct(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: order size (pct of value)
		:return: none
		'''
		self.order_list.append(Order_pct(symbol, pct))
		self.order_count += 1

	def order_pct_to(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: target pct of value
		:return: none
		'''
		self.order_list.append(Order_pct_to(symbol, pct))
		self.order_count += 1



	def get_hist_log(self):
		return self.trade_log

	def trade_result(self):
		return self.date, self.trade_volume, self.trade_cost



def trade_status(self, symbol):
	'''
	Calculate whether a stock can be traded in this day
	:param symbol: stock symbol
	:return: True if the stock is available for trading
	'''
	return (self.__trade_info[symbol]['trade_status'] == '交易' and self.__trade_info[symbol]['maxupordown'] == 0)


class Trade_info(object):
	'''

	'''
	def __init__(self,cash,symbol,price,maxupordown,status,portfolio_value,position,commission=0.001,short=False):
		self.__cash = cash
		self.__symbol = symbol
		self.__price = price
		self.__maxupordown = maxupordown
		self.__status = status
		self.__position = position
		self.__portfolio_value = portfolio_value
		self.max_amount = self.__calculate_max(cash,price,commission)
		self.min_amount = self.__calculate_min(short,position)


	def __calculate_max(self,cash,price,commission):
		return math.floor(cash/((price*(1+commission)*100)))

	def __calculate_min(self,short,position):
		if not short:
			return -position
		else:
			return -float("inf")

	@property
	def symbol(self):
		return self.__symbol

	@property
	def maxupordown(self):
		return self.__maxupordown

	@property
	def status(self):
		return self.__status

	@property
	def position(self):
		return self.__position

	@property
	def portfolio_value(self):
		return self.__portfolio_value

	@property
	def cash(self):
		return self.__cash

	@property
	def price(self):
		return self.__price


class Order(object):
	'''

	'''
	def __init__(self,symbol, num):
		self.amount = num
		self.symbol = symbol
		self.__valid_volume = 0.0
		self.__valid_price = 0.0
		self.validation = False

	@property
	def valid_price(self):
		return self.__valid_price

	@property
	def valid_volume(self):
		return self.__valid_volume

	def validations(self,trade_amount,info):
		if (not info.maxupordown) and info.status == u'交易':
			self.__valid_volume = min(max(info.min_amount, trade_amount), info.max_amount)
		else:
			self.__valid_volume = 0
		self.__valid_price = info.price
		self.validation = True

	def __repr__(self):
		if self.validation:
			return('Symbol:'+str(self.symbol) + '; price %0.3f'%self.valid_price +'; volume %0.1f' %self.valid_volume +' .')
		else:
			return 'The order has not been validated'


class Order_num(Order):
	'''

	'''
	def __init__(self, symbol,num):
		Order.__init__(self,symbol,num)

	def validate(self,info):
		trade_amount = self.amount
		self.validations(trade_amount,info)


class Order_num_to(Order):
	'''

	'''
	def __init__(self, symbol, num):
		Order.__init__(self,symbol, num)


	def validate(self, info):
		trade_amount = self.amount - info.position
		self.validations(trade_amount,info)


class Order_pct(Order):
	'''

	'''
	def __init__(self, symbol, num):
		Order.__init__(self,symbol, num)


	def validate(self, info):
		trade_amount = math.floor(self.amount*info.portfolio_value/(info.price*100))
		self.validations(trade_amount,info)



class Order_pct_to(Order):
	'''

	'''
	def __init__(self, symbol, num):
		Order.__init__(self,symbol, num)

	def validate(self, info):

		trade_amount = math.floor(self.amount * info.portfolio_value / (info.price * 100))-info.position

		self.validations(trade_amount,info)





def main():
	pass


def test():
	from datafeed import datafeed
	from portfolio import portfolio
	import random
	bk = broker()
	dd = datafeed(universe='allA')
	dd.initialize()

	for i in range(10):
		date, temp = dd.data_fetch()
		bk.update_info(date, temp)
		x = random.random()
		bk.order_pct('000789.SZ', 0.1)
		bk.order_pct('601928.SH', 0.1)
		bk.update_value()
		bk.execute()


if __name__ == '__main__':
	test()



