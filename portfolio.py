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

	'''
	def __init__(self, symbol):
		self.__symbol = symbol
		self.amount = 0.0
		self.last_close = 0.0
		self.cur_close = 0.0
		self.position_log = defaultdict(int)
		self.close_log = defaultdict(int)

	@property
	def symbol(self):
		return self.__symbol

	@property
	def position_value(self):
		return self.cur_close*self.amount

	def update_position(self,order,date):
		'''
		Update the position amount from the order
		:param order:
		:param date:
		:return: none
		'''
		if order.validation:
			self.amount = self.amount+order.valid_volume
			self.position_log[date] = {'position':self.amount}
		else:
			print('The order has not been updated')

	def update_value(self,price,date):
		'''
		Update the position close price and record the price
		:param price: current close price
		:param date:  current date
		:return: none
		'''
		self.last_close = self.cur_close
		self.cur_close = price
		self.close_log[date] = {'close price':self.cur_close}


class portfolio(object):
	def __init__(self, begin_equity=10000000,commission=0.002):
		'''

		:param begin_equity: the initial equity value
		:param commission: commission fee
		'''
		self.portfolio_value = begin_equity
		self.__cash = begin_equity
		self.__positions = defaultdict(int)
		self.commission = commission
		self.PnL = 0
		self.position_log = {}
		self.start_date = None

	@property
	def cash(self):
		return self.__cash
	@property
	def positions(self):
		return self.__positions

	def update(self,order):
		if order.validation:
			# update
			self.__positions[order.symbol] += order.valid_volume
			self.__cash -=  order.valid_volume*order.valid_price*(1+self.commission)*100


	def update_port(self,data):
		'''

		:param data: daily trading data
		:return:
		'''
		# set the portfolio value to zero
		self.portfolio_value = 0
		for position in self.__positions:
			# update the stock closing value
			position.update_value(data)
			# update the whole portfolio value
			self.portfolio_value += position.position_value()



	@property
	def cur_position(self):
		return self.__cur_position

	@property
	def cur_cash(self):
		return self.__cur_cash

	@property
	def cur_balance(self):
		return self.__cur_balance

	@property
	def cur_PnL(self):
		return self.__cur_PnL

	@property
	def hist_log(self):
		return self.__hist_log

	@property
	def hist_pos_log(self):
		return self.__hist_pos_log




if __name__ == '__main__':
	pass
