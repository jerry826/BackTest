# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: broker.py
@time: 2016/5/4 21:53
"""

import numpy as np
import pandas as pd


class broker():
	'''

	'''

	def __init__(self, fee=0.002, cost=0.002, weights='equal', position=0.7):

		self.__unfinished_order = dict()
		self.__fee = fee
		self.__cost = cost
		self.__weights = weights
		self.__position = position

	def order(self, signal, hist_position, hist_balance, data):
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
	transaction_volumn, transaction_fee, cur_positison = bk.order({'000001.SZ': 1, '000002.SZ': 1}, dict(), 10000000,
	                                                              data)
	print(transaction_volumn)
	print(transaction_fee)
	print(cur_positison)


if __name__ == '__main__':
	bk = broker()

