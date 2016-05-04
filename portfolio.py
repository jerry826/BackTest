# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: portfolio.py
@time: 2016/5/4 22:04
"""


class portfolio():
	def __init__(self, begin_equity=10000000):
		self.__cur_position = dict()
		self.__cur_cash = begin_equity
		self.__cur_balance = begin_equity
		self.__hist_log = dict()
		self.__cur_PnL = 0

	def update(self, cur_positison, end_position_value, transaction_fee, delta_cash, temp, date, ):
		self.__hist_log[date] = {'position': self.__cur_position, 'cash': self.__cur_cash,
		                         'balance': self.__cur_balance, 'PnL': self.__PnL}
		# update current position
		self.__cur_position = cur_positison
		# update current cash
		self.__cur_cash = self.__cur_cash + delta_cash - transaction_fee
		# update current balance
		last_balance = self.__balance
		self.__balance = end_position_value + self.__cur_cash
		# update PnL
		self.__cur_PnL = self.__balance - last_balance

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


if __name__ == '__main__':
	pass
