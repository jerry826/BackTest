# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: demo.py
@time: 2016/5/19 0:09
"""

from backtest import BackTest

def func():
	pass


class Strategy(BackTest):
	def __init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq):
		BackTest.__init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq)

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''
		self.strat


		universe = self.broker.get_universe()
		for symbol in universe:
			self.broker.order_pct('zz500', 0.01)


def main():
	bt = Strategy(model_name='mm',
	              begin_time="2013-01-01",
	              end_time="2015-11-01",
	              path='E:\\data',
	              universe = 'zz500',
	              begin_equity=  100000000,
	              fee = 0.002,
	              freq =5)
	pos, close, nav = bt.start()

if __name__ == '__main__':
	main()