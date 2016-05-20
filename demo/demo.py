# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: demo.py
@time: 2016/5/19 0:09
"""

from backtest import BackTest


class Strategy(BackTest):
	def __init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq,length, lag):
		BackTest.__init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq,length, lag)

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''
		portfolio_value = self.broker.portfolio_value()  # account value
		cash = self.broker.get_cash()  # cash available
		universe = self.broker.get_universe()  # stock can be traded

		buy_list = universe[0:50]
		hold_list = [stock for stock in buy_list if stock in universe]
		# sell first
		for stock in universe:
			if stock not in hold_list:
				self.broker.order_to(stock, 0)

		# change the position
		change = {}
		d = len(hold_list)
		for stock in hold_list:
			weight = self.broker.get_weight(stock)
			change[stock] = 1/d-weight
		# make the orders
		for stock in sorted(change, key=change.get):
			self.broker.order_pct_to(stock, change[stock])

def main():
	bt = Strategy(model_name='mm',
	              begin_time="2013-01-01",
	              end_time="2013-05-01",
	              path='E:\\data',
	              universe = 'allA',
	              begin_equity=  100000000,
	              fee = 0.002,
	              freq =5,
				  length=10,
				  lag=1)
	perf, risk = bt.start()

if __name__ == '__main__':
	main()