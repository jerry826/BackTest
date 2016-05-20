# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: demo_pair_trade.py
@time: 2016/5/20 19:46
"""

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
	             path, universe,freq,length, lag, short):
		BackTest.__init__(self,model_name, begin_time, end_time, begin_equity, fee,
	             path, universe,freq,length, lag, short)

	def handle_data(self):
		'''
		The trade strategy part
		:return: none
		'''

		MA5 = self.strat.MA(5, 'close')  # get MA5
		MA20 = self.strat.MA(20, 'close')  # get MA10
		d1 = MA20['600886.SH'] / MA20['600674.SH']
		d2 = MA5['600886.SH'] / MA5['600674.SH']
		if d2 < d1:
			self.broker.order_pct_to('600886.SH', 0.25)
			self.broker.order_pct_to('600674.SH', -0.25)

		else:

			self.broker.order_pct_to('600886.SH', -0.25)
			self.broker.order_pct_to('600674.SH', 0.25)

def main():
	bt = Strategy(model_name='mm',
	              begin_time="2013-01-01",
	              end_time="2013-12-01",
	              path='E:\\data',
	              universe = ['600886.SH','600674.SH'],
	              begin_equity=  100000000,
	              fee = 0.002,
	              short=True,
	              freq =2,
				  length=10,
				  lag=1)
	perf, risk = bt.start()

if __name__ == '__main__':
	main()