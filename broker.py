# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
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
	Broker class
	'''
	def __init__(self,commission=0.002,price_type='vwap',short=False):
		'''
		Initializing the broker class
		:param commission: commission fee, default 0.002
		:param price_type: vwap or close price or open price or other choices(close*0.5+open*0.5)
		:param short: True or False, True if shorting is allowed
		'''
		# set default parameters
		self.commission = commission
		self.price = price_type
		self.short = short
		#
		self.port = portfolio(begin_equity=1000000,commission=commission)
		self.order_list = []
		self.order_count = 0
		self.trading_data = pd.DataFrame()
		# two triggers
		self.execute_trigger = False
		self.update_trigger = False
		# daily recorder
		self.trade_volume = 0.0
		self.trade_cost = 0.0
		self.trade_log = defaultdict()

	def get_universe(self):
		universe = list(self.trading_data[(self.trading_data['maxupordown'] == 0) & (self.trading_data['trade_status'] == u'交易')].index)
		return universe

	def execute(self):
		'''
		Execute the orders separately
		:return: none
		'''
		if not self.execute_trigger:
			# execute the orders
			for order in self.order_list:
				info = Trade_info(cash=self.port.cash, # cash amount
				                  symbol=order.symbol,
				                  price=self.trading_data.loc[order.symbol,'adj_trade'],  # trade price
				                  maxupordown=self.trading_data.loc[order.symbol,'maxupordown'],
				                  status=self.trading_data.loc[order.symbol,'trade_status'],
				                  portfolio_value=self.port.portfolio_value,
				                  position=self.port.positions[order.symbol].position, # stock position
				                  commission=self.commission,
				                  short=self.short)
				# validate the orders
				order.validate(info)
				# execute the order
				self.trade_cost,self.trade_volume =self.port.update(order)
				print(order)

			# record the trade results
			self.trade_log[self.date] = {'trade_volume':self.trade_volume,
										 'trade_cost': self.trade_cost,
										 'order num':self.order_count}
			self.execute_trigger = True
			self.update_trigger = False
			self.trade_summary()

		else:
			print('You cannot execute the order twice in a single trade day or without update the data')

	def trade_summary(self):
		'''
		Print the trading result in a single day
		'''
		print('========================================================')
		print('Date: ' +str(self.date))
		print('Trade volume %0.1f'%self.trade_volume)
		print('Port cash %0.1f'%self.port.cash)

	def update_value(self):
		'''
		Update the portfolio value
		:return: none
		'''
		self.port.update_port(self.trading_data,self.date)
		print('Update value: Portfolio value  %0.1f' % self.port.portfolio_value)
		print('Update value: Cash value  %0.1f' % self.port.cash)
		print('Update value: Stock value  %0.1f' % self.port.portfolio_value)

	def update_info(self,date,trading_data):
		'''
		Get the new trading data and update the trade information
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
		self.order_list = []
		#
		self.update_trigger = True # Finish data update
		self.execute_trigger = False

	def order(self, symbol, amount):
		'''
		Standard trade order
		:param symbol: stock symbol
		:param amount: order size
		:return:
		'''

		self.order_list.append(Order_num(symbol,amount,self.date))
		self.order_count += 1

	def order_to(self,symbol,amount):
		'''

		:param symbol: stock symbol
		:param amount: target position
		:return: none
		'''
		self.order_list.append(Order_num_to(symbol, amount, self.date))
		self.order_count += 1

	def order_pct(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: order size (pct of value)
		:return: none
		'''
		self.order_list.append(Order_pct(symbol, pct,self.date))
		self.order_count += 1

	def order_pct_to(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: target pct of value
		:return: none
		'''
		self.order_list.append(Order_pct_to(symbol,pct,self.date))
		self.order_count += 1

	def get_hist_log(self):
		return self.trade_log

	def get_hist_perf(self):
		return self.port.get_hist_log()

	def trade_result(self):
		return self.date, self.trade_volume, self.trade_cost

	def get_position(self,symbol):
		'''
		get the position of a single stock in last trade day from portfolio
		:param symbol: stock symbol
		:return: the position size
		'''
		return self.port.get_position(symbol)

	def get_position_report(self):
		hist_pos = self.port.get_hist_close_log()
		hist_close = self.port.get_hist_close_log()
		return hist_pos,hist_close

	def get_weight(self,symbol):
		'''
		get the position of a single stock in last trade day from portfolio
		:param symbol: stock symbol
		:return: the stock weight
		'''
		return self.port.weight(symbol)






class Trade_info(object):
	'''
	Trade info class.
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
		'''
		Calculate the largest amount of stock which can be long
		:param cash: cash left in the account
		:param price: stock trade price
		:param commission: commission fee
		:return: largest long amount
		'''
		return math.floor(cash/((price*(1+commission)*100)))

	def __calculate_min(self,short,position):
		'''
		Calculate the largest amount of stock which can be short
		:param short: whether short is allowed
		:param position: current position
		:return: largest short amount
		'''
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
	Order class
	'''
	def __init__(self,symbol, num, date):
		'''

		:param symbol: stock symbol
		:param num: value for trade amount (pct or amount)
		:param date: trade date
		'''
		self.amount = num
		self.symbol = symbol
		self.__valid_volume = 0.0
		self.__valid_price = 0.0
		self.__date = date
		self.validation = False

	@property
	def valid_price(self):
		return self.__valid_price

	@property
	def valid_volume(self):
		return self.__valid_volume

	@property
	def date(self):
		return self.__date

	def validations(self,trade_amount,info):
		'''
		Validate the order
		:param trade_amount:
		:param info:
		:return:
		'''
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
	def __init__(self, symbol,num,date):
		Order.__init__(self,symbol,num,date)

	def validate(self,info):
		trade_amount = self.amount
		self.validations(trade_amount,info)


class Order_num_to(Order):
	'''

	'''
	def __init__(self,symbol,num,date):
		Order.__init__(self,symbol,num,date)


	def validate(self, info):
		trade_amount = self.amount - info.position
		self.validations(trade_amount,info)


class Order_pct(Order):
	'''

	'''
	def __init__(self,symbol,num,date):
		Order.__init__(self,symbol,num,date)


	def validate(self, info):
		trade_amount = math.floor(self.amount*info.portfolio_value/(info.price*100))
		self.validations(trade_amount,info)



class Order_pct_to(Order):
	'''

	'''
	def __init__(self, symbol,num,date):
		Order.__init__(self,symbol,num,date)

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

	for i in range(30):
		date, temp = dd.data_fetch()
		bk.update_info(date, temp)
		x = random.random()
		print('random: %0.3f' %x)
		bk.order_pct_to('000789.SZ', x)
		bk.execute()
		bk.update_value()



if __name__ == '__main__':
	test()



