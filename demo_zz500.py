# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: demo_zz500.py
@time: 2016/5/20 17:47
"""


from backtest import BackTest


class Strategy(BackTest):
	def __init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq,length, lag,short, price_type):
		BackTest.__init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq,length, lag,short, price_type)

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''

		MA5 = self.strat.MA(5,'close')  # get MA5
		MA10 = self.strat.MA(10,'close') # get MA10

		# if MA5['zz500'] > MA10['zz500'] - 0.5:
		# 	self.broker.order_pct_to('zz500',0.8)
		# else:
		# 	self.broker.order_pct_to('zz500',0)
		self.broker.order_pct_to('zz500',1)

def main():
	bt = Strategy(model_name='mm',
	              begin_time="2013-01-01",
	              end_time="2013-03-01",
	              path='E:\\data',
	              universe = 'zz500',
	              begin_equity=  100000000,
	              fee = 0.002,
	              freq =2,
				  length=10,
				  lag=1,
	              short=True)
	perf, risk = bt.start()

if __name__ == '__main__':
	main()