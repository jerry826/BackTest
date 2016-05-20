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
		self.avg_cost = 0


	@property
	def symbol(self):
		return self.__symbol

	@property
	def position(self):
		return self.__amount

	@property
	def position_value(self):
		'''
		Return the position value
		:return:
		'''
		# print(self.symbol)
		# print('avg %0.2f'%self.avg_cost)
		# print('amount %0.2f' %self.__amount)
		# print('cur close: %0.2f' %self.cur_close)
		return abs(self.avg_cost*self.__amount*100)+self.__amount*(self.cur_close-self.avg_cost)*100

	def update_position(self,order):
		'''
		Update the position amount from the order
		:param order:
		:param date:
		:return: none
		'''
		if order.validation:
			pos_old = self.__amount
			pos_new = order.valid_volume+self.__amount
			if pos_old*pos_new > 0:
				self.avg_cost = (self.avg_cost*self.__amount + order.valid_volume*order.valid_price)/(self.__amount+order.valid_volume)
			else:
				# change the direction of position
				self.avg_cost = order.valid_price
			self.__amount = self.__amount + order.valid_volume  # update amount
			self.order_log.append(order)  # add this order to the order list
			self.__symbol = order.symbol
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

	def get_avg_cost(self):
		return self.avg_cost

class Portfolio(object):
	def __init__(self, begin_equity=10000000,commission=0.002,start_date='2011-01-01'):
		'''
		Initializing the portfolio
		:param begin_equity: the initial equity value
		:param commission: commission fee
		'''
		self.__stock_value = 0
		self.__cash = begin_equity
		self.commission = commission
		self.__positions = defaultdict(Position)
		self.start_date = start_date
		self.date = start_date
		self.nav_log = {}
		self.cash_log = {}

	@property
	def cash(self):
		return self.__cash
	@property
	def positions(self):
		return self.__positions

	@property
	def portfolio_value(self):
		return self.__cash + self.__stock_value

	@property
	def stock_value(self):
		return self.__stock_value

	def update(self, order,output=False):
		'''
		Update the position according to the order received
		:param order: order from broker
		:param output: whether print the update result
		:return: transaction fee and the change of cash balance
		'''
		if order.validation:
			# update the order information into the position class
			pos_old = self.__positions[order.symbol].position
			pos_new = pos_old+order.valid_volume
			avg_cost = self.__positions[order.symbol].get_avg_cost()

			# calculate the transaction fees(if the order is short type, the valid_volume is negative)
			fee = abs(order.valid_price*abs(order.valid_volume)*self.commission*100)

			# calculate the trade amount
			trade_amount = abs(order.valid_price*abs(order.valid_volume)*(1+self.commission)*100)
			# calculate the delta cash
			delta_cash = 0
			if pos_new*pos_old >0:
				if pos_new > 0:
					delta_cash = order.valid_volume*order.valid_price*100
				else:
					delta_cash = -order.valid_volume*order.valid_price*100

			elif pos_new * pos_old < 0:
				if pos_new > 0:
					# new long; old short
					delta_cash = order.valid_price*pos_new*100 + pos_old*(2*avg_cost-order.valid_price)*100
				else:
					# new short; old long
					delta_cash = -pos_old*order.valid_price*100 - pos_new*order.valid_price*100
			else:
				if pos_old == 0:
					delta_cash = abs(pos_new)*order.valid_price*100
				else:
					if pos_old>0:
						delta_cash = -pos_old*order.valid_price*100
					else:
						delta_cash = pos_old*(2*avg_cost-order.valid_price)*100
			delta_cash += fee

			self.__positions[order.symbol].update_position(order)

			self.__cash -= delta_cash
			if output:
				print('fee: %0.2f' % fee)
				print('cash available: %0.2f'%self.__cash)
			return fee, trade_amount, delta_cash
		else:
			print('The order need to be validated first before execution')
			return 0, 0, 0

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
		# print(list(pos.position_value for pos in list(self.__positions.values())))


		self.__stock_value = sum( pos.position_value for pos in list(self.__positions.values()))
		self.nav_log[date] = self.__stock_value+self.__cash
		self.cash_log[date] = self.__cash
		# self.position_summary()

	def position_summary(self):
		'''
		Print the position summary
		:return: None
		'''
		print([self.__positions.keys()])
		print([x.position for x in self.__positions.values()])

	def get_nav_log(self):
		'''
		Return the historical nav data
		:return: the nav log
		'''
		return self.nav_log

	def get_cash_log(self):
		'''
		Return the historical cash data
		:return: the cash log
		'''
		return self.cash_log


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

	def get_hist_position_log(self):
		hist_pos = {}
		for symbol in self.__positions:
			pos = self.__positions[symbol]
			hist_pos[symbol] = pos.position_log
		return hist_pos

	def get_hist_close_log(self):
		hist_close = {}
		for symbol in self.__positions:
			pos = self.__positions[symbol]
			hist_close[symbol] = pos.close_log
		return hist_close





def test():
	port = portfolio()
	print(port.cash)



if __name__ == '__main__':
	test()
