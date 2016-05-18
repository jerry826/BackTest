# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: portfolio.py
@time: 2016/5/4 22:04
"""
from collections import defaultdict
import pandas as pd

class Positions(object):
	def __init__(self):
		pass


class Position(object):
	'''
	Position class for a single stock.
	Recording the historical transactions, the historical positions and the current close price

	'''
	def __init__(self, symbol='000001.SZ'):
		self.__symbol = symbol
		self.__amount = 0.0
		self.last_close = 0.0
		self.cur_close = 0.0
		self.date = None
		self.position_log = defaultdict(int)
		self.close_log = defaultdict(int)
		self.order_log = []

	@property
	def symbol(self):
		return self.__symbol

	@property
	def position(self):
		return self.__amount

	@property
	def position_value(self):
		return self.cur_close*self.__amount*100

	def update_position(self,order):
		'''
		Update the position amount from the order
		:param order:
		:param date:
		:return: none
		'''
		if order.validation:
			self.__amount = self.__amount+order.valid_volume # update amount
			self.order_log.append(order) # add this order to the order list

		else:
			print('The order has not been updated')

	def update_value(self,close,date):
		'''
		Update the position close price and record the price
		:param price: current close price
		:param date:  current date
		:return: none
		'''
		if close != 0:
			self.last_close = self.cur_close # record last close price
			self.cur_close = close # update current close price
		else:
			self.last_close = self.cur_close
		self.date = date # update date
		self.close_log[date] = self.cur_close # add the position into the position log
		self.position_log[date] = self.__amount  # add the close price into the price log


class portfolio(object):
	def __init__(self, begin_equity=10000000,commission=0.002,start_date='2011-01-01'):
		'''

		:param begin_equity: the initial equity value
		:param commission: commission fee
		'''
		self.__stock_value = 0
		self.__cash = begin_equity
		self.commission = commission
		self.__positions= defaultdict(Position)
		self.start_date = start_date
		self.date = start_date
		self.log = {}

	@property
	def cash(self):
		return self.__cash
	@property
	def positions(self):
		return self.__positions

	def update(self,order):
		'''
		Update the position according to the order received
		:param order: order from broker
		:return: transaction fee and the change of cash balance
		'''
		if order.validation:
			# update the order information into the  position
			self.__positions[order.symbol].update_position(order)
			# calculate the transaction fees
			fee = order.valid_price*abs(order.valid_volume)*self.commission*100
			print(fee)
			trade_volume = order.valid_volume*order.valid_price*(1+self.commission)*100
			self.__cash -=  trade_volume+fee
			return fee, abs(trade_volume)+fee
		else:
			print('The order need to be validated first before execution')
			return 0,0

	def update_port(self,data,date):
		'''
		Update the daily close price for all the position and calculate the portfolio value
		:param data: daily trading data
		:return: none
		'''
		# update date
		self.date = date
		for symbol in self.__positions.keys():
			# update the stock closing value
			if symbol in data.index:
				close = data.loc[symbol,'adj_close']
				self.__positions[symbol].update_value(close,self.date)
			else:
				self.__positions[symbol].update_value(0, self.date)
		# calculate the position value
		self.__stock_value = sum( pos.position_value for pos in list(self.__positions.values()))
		self.log[date] = self.__stock_value+self.__cash
		self.position_summary()

	def position_summary(self):
		print([x.symbol for x in self.__positions.values()])
		print([x.position for x in self.__positions.values()])

	def get_position(self,symbol):
		'''
		get the position of a single stock in last trade day
		:param symbol: stock symbol
		:return: the position size
		'''
		return self.__positions[symbol].position

	def get_weight(self,symbol):
		'''
		get the position of a single stock in last trade day
		:param symbol: stock symbol
		:return: the stock weight
		'''

		return self.__positions[symbol].position_value/(self.__stock_value+self.__cash)

	def get_hist_log(self):
		return self.log

	@property
	def cur_position(self):
		return self.__positions

	@property
	def cash(self):
		return self.__cash

	@property
	def portfolio_value(self):
		return self.__cash+self.__stock_value

	@property
	def stock_value(self):
		return self.__stock_value

	@property
	def cur_PnL(self):
		return None

	@property
	def hist_log(self):
		return None

	@property
	def hist_pos_log(self):
		return None

def test():
	port = portfolio()
	print(port.cash)



if __name__ == '__main__':
	test()
