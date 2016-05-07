# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: broker.py
@time: 2016/5/4 21:53
"""

import math
import numpy as np
import pandas as pd


class broker(object):
	'''

	'''
	def __init__(self,fee=0.002,price_type='vwap',short=False):
		'''
		Initializing the broker class
		:param fee:
		:param cost:
		:param weights:
		:param position:
		:return:
		'''
		self.__unfinished_order = dict()
		self.__fee = fee
		self.__cash_balance = 10000
		self.__position_value = 10000
		self.__position = dict()
		self.__trading_data = pd.DataFrame()
		self.__price = price_type
		self.__hist_log = dict()
		self.__short = short


	def update_info(self,date,trading_data):
		'''
		Get the new trading data and update the information
		:param date: trading date
		:param trading_data: trading data
		:return: none
		'''
		self.__trading_data = trading_data.reset_index().set_index('sec_code')
		self.__trading_data.loc[:,'adj_close'] = self.__trading_data.loc[:,'close']*self.__trading_data.loc[:,'adjfactor']
		self.__trading_data.loc[:,'adj_trade'] = (self.__trading_data.loc[:,self.__price]*self.__trading_data.loc[:,'adjfactor'])
		self.__trade_info = (self.__trading_data.loc[:,['adj_close','adj_trade','trade_status','maxupordown']]).to_dict(orient='index')
		self.__date = date
		self.__hist_log[self.__date] = dict()

	def trade_status(self,symbol):
		'''
		Calculate whether a stock can be traded in this day
		:param symbol: stock symbol
		:return: True if the stock is available for trading
		'''
		return (self.__trade_info[symbol]['trade_status'] == '交易' and self.__trade_info[symbol]['maxupordown'] == 0)

	def take_order_list(self,order_list):
		'''
		Take a dict of order list and deal the orders together
		:param order_list: a trading order list
		:return: none
		'''
		for symbol, trade_order in order_list.items():
			if trade_order['order_type'] == '1':
				self.order(symbol,trade_order['amount'])
			elif trade_order['order_type'] == '2':
				self.order_to(symbol,trade_order['amount'])
			elif trade_order['order_type'] == '3':
				self.order_pct(symbol,trade_order['amount'])
			elif trade_order['order_type'] == '4':
				self.order_pct_to(symbol,trade_order['amount'])
			else:
				print('Invalid order type.')

	def order(self, symbol, amount):
		'''

		:param symbol: stock symbol
		:param amount: order size
		:return:
		'''
		self.__register(symbol)
		if self.trade_status(symbol):
			self.__order(symbol, amount)

	def order_to(self,symbol,amount):
		'''

		:param symbol: stock symbol
		:param amount: target position
		:return: none
		'''
		self.__register(symbol)
		if self.trade_status(symbol):
			self.__order(symbol, amount-self.__position[symbol])

	def order_pct(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: order size (pct of value)
		:return: none
		'''
		trade_price = self.__trade_info[symbol]['adj_close']
		self.__register(symbol)
		if self.trade_status(symbol):
			amount = math.floor(self.__position_value*pct/(trade_price*100))*100
			self.__order(symbol,amount)


	def order_pct_to(self,symbol,pct):
		'''

		:param symbol: stock symbol
		:param pct: target pct of value
		:return: none
		'''
		trade_price = self.__trade_info[symbol]['adj_close']
		self.__register(symbol)
		if self.trade_status(symbol):
			amount = math.floor(self.__position_value*pct/(trade_price*100))*100
			self.__order(symbol,amount-self.__position[symbol])

	def __order(self,symbol,amount):
		'''
		Place the order
		:param symbol: stock symbol
		:param amount: order amount
		:return: none
		'''
		trade_price = self.__trade_info[symbol]['adj_close']
		amount_up_limit = math.floor(self.__cash_balance/(100*trade_price*(1+self.__fee)))*100
		print(self.__cash_balance/(100*trade_price*(1+self.__fee)))
		print(amount_up_limit)
		if self.__short == False:
			amount_down_limit = -self.__position[symbol]
		else:
			amount_down_limit =-float('inf')
		amount = min(max(amount_down_limit,amount),amount_up_limit)
		# update cash balance
		self.__cash_balance = self.__cash_balance - trade_price*amount-abs(amount)*trade_price*self.__fee # update cash balance
		# update stock position
		self.__position[symbol] = self.__position[symbol]+amount
		# add transaction log
		self.__hist_log[self.__date][symbol] = {'price':trade_price,'amount':amount}
		print('Amount: '+ str(amount))
		print('Cash: '+ str(self.__cash_balance))
		print('Position: '+ str(self.__position[symbol]))
		print('Cost: ' + str(abs(amount)*trade_price*self.__fee))
		print('-----------------------------------')


	def __register(self,symbol):
		'''
		Register the stock symbol in the position log if the stock has not been traded before
		:param symbol: stock symbol
		:return:
		'''
		# add the stock into the stock log list
		if symbol not in self.__position.keys():
			self.__position[symbol] = 0

	def get_hist_log(self):
		return self.__hist_log


	def orderX(self, signal, hist_position, hist_balance, data):
		'''
		:param signal: trading signal comes from strat
		:param hist_position: the position information in last trade day
		:param hist_balance:  balance in last trade day
		:param data: trade information
		:return: the actual trade deal and the transaction cost
		'''
		order_list = dict()
		# merge the trade signal unfinished in last trade day
		for stock in self.__unfinished_order:
			last_order = self.__unfinished_order[stock]
			if stock not in signal.keys():
				cur_order = 0
			else:
				cur_order = signal[stock]
			# compare these two signals
			# same signal
			if last_order * cur_order == 1:
				pass
			# signal from opposite direction
			elif last_order + cur_order == 0:
				signal[stock] = 0
			# keep on clear the position
			elif last_order == -1 and cur_order == 0:
				signal[stock] = -1
			# stop build the position
			elif last_order == 1 and cur_order == 0:
				pass
			else:
				raise ValueError('Signals ' + str(last_order) + ' and ' + str(cur_order) + ' are invalid ')

		# check the trade status
		data = data.reset_index()
		data = data.set_index('sec_code')
		# trade status: 交易 停牌一小时 停牌一天
		data.loc[:, 'statu'] = np.where(data.loc[:, 'trade_status'] == u'交易', 1, 0) * np.where(
			data.loc[:, 'maxupordown'] == 0, 1, 0)
		status = data.loc[:, 'statu'].to_dict()
		# clear the unfinished orders
		self.__unfinished_order = dict()
		# update the orders
		stock_holing_list = list(hist_position.keys())

		for stock in signal.keys():
			if stock in status.keys():
				if signal[stock] == 1 and (stock not in hist_position):
					# positive signal and no position before
					if status[stock] == 1:
						order_list[stock] = signal[stock]
						stock_holing_list.append(stock)
					else:
						self.__unfinished_order[stock] = signal[stock]
				elif signal[stock] == -1 and (stock in hist_position):
					# negative signal and exits position before
					if status[stock] == 1:
						order_list[stock] = signal[stock]
						stock_holing_list.remove(stock)
					else:
						self.__unfinished_order[stock] = signal[stock]
				else:
					pass
			else:
				print(str(stock) + ' not in the market')

		# calculate the new position

		if self.__weights == 'equal':
			if len(stock_holing_list) > 0:
				data = data.fillna(0)
				position_size = hist_balance * self.__position / len(stock_holing_list)
				cur_position_size = dict()
				for stock in stock_holing_list:
					cur_position_size[stock] = position_size
				df2 = pd.Series(cur_position_size)
			else:
				df2 = pd.Series()
			df1 = pd.Series(hist_position)
			data.loc[:, 'hist_position_num'] = df1
			data.loc[:, 'cur_position_value'] = df2
			# calculate positive num(round to 100)

			data.loc[:, 'price'] = data.loc[:, 'adjfactor'] * (data.loc[:, 'open'] + data.loc[:, 'close']) / 2
			data.loc[:, 'cur_position_num'] = (data.loc[:, 'cur_position_value'] / (100 * data.loc[:, 'price'])).apply(
				round) * 100
			# calculate the trade volumn
			data = data.fillna(0)
			transaction_volume = np.sum(
				np.abs((data.loc[:, 'hist_position_num'] - data.loc[:, 'cur_position_num']) * data.loc[:, 'price']))
			delta_cash = np.sum(
				(data.loc[:, 'hist_position_num'] - data.loc[:, 'cur_position_num']) * data.loc[:, 'price'])
			transaction_fee = transaction_volume * self.__fee

			cur_positison = data.loc[data.loc[:, 'cur_position_num'] > 0, 'cur_position_num']
			end_equity_balance = sum(data.loc[:, 'cur_position_num'] * data.loc[:, 'close'] * data.loc[:, 'adjfactor'])
		else:
			raise ValueError('Bad choice')

		return transaction_volume, transaction_fee, cur_positison, end_equity_balance, delta_cash


def main():
	bk = broker()



if __name__ == '__main__':
	from datafeed import datafeed
	bk = broker()
	dd = datafeed(universe='allA')
	dd.initialize()
	for i in range(3):
		date, temp = dd.data_fetch()
		print(bk.update_info(date, temp))
		bk.order_to('000789.SZ',200)
		bk.order_to('000789.SZ',0)
		bk.order('000789.SZ',0)
		bk.order_pct_to('000789.SZ',1)
		bk.order_pct_to('000789.SZ',0)
		bk.order_pct_to('000789.SZ',0.5)
		bk.order_pct('000789.SZ',0.5)
		bk.order_to('601939.SH',0)
		bk.order_pct_to('000789.SZ',-1000)

	print(bk.get_hist_log())


