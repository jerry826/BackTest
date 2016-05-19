# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.cn
@file: datafeed.py
@time: 2016/4/30 14:37
"""

import datetime
import os
import pandas as pd


class datafeed(object):
	'''
	datafeed
	'''

	def __init__(self, universe='allA', begin_date='2014-01-01', end_date='2015-01-01', path='E:\\data'):
		'''
		:param universe: 'allA', 'zz500', stock id list
		:param begin_date:
		:param end_date:
		:param path:
		:return:
		'''
		self.__universe = universe
		self.__begin_date = begin_date
		self.__end_date = end_date
		self.__path = path
		self.__count = 0
		self.__date_list = []
		self.__length = 0
		self.__day1 = ''
		self.__day2 = ''
		self.data = pd.DataFrame()

	@property
	def time_length(self):
		return self.__length

	@property
	def start_day(self):
		return self.__day1

	@property
	def end_day(self):
		return self.__day2

	def initialize(self):
		'''
		Initialize the class and read data
		:return:
		'''
		print('######## Reading data ########')
		print(self.__universe)

		if self.__universe == 'allA' or isinstance(self.__universe, list):
			self.__path += '\\mktQuotation_bar'  # set the path
			date_list = sorted([int(x[-12:-4]) for x in os.listdir(self.__path)[:-1]])  # get the date list

			self.__date_list = [x for x in date_list if
			                    x >= int(''.join(self.__begin_date.split('-'))) and x <= int(
				                    ''.join(self.__end_date.split('-')))]

			self.__length = len(self.__date_list)  # get the length of date list
			day1 = str(self.__date_list[0])
			day2 = str(self.__date_list[-1])
			self.__day1 = day1[0:4] + '-' + day1[4:6] + '-' + day1[6:8]
			self.__day2 = day2[0:4] + '-' + day2[4:6] + '-' + day2[6:8]

		elif self.__universe == 'zz500':
			xlsx = pd.ExcelFile(self.__path + '\\中证500测试数据.xlsx')
			df = pd.read_excel(xlsx, 'Sheet1')
			self.data = self.__data_transform(df)
			self.data = self.data[self.__begin_date:self.__end_date]
			print(self.__begin_date)
			print(self.__end_date)
			self.__date_list = self.data.index
			self.__length = len(self.__date_list)
			day1 = str(self.__date_list[0])
			day2 = str(self.__date_list[-1])

		else:
			raise ValueError("No such data type")
		print('Get ' + str(self.__length) + ' obersevations from ' + str(self.__day1) + ' to ' + str(self.__day2))
		print('########     Done     ########')

	def data_fetch(self):
		if self.__count == self.__length:
			print('No more data avaiable')
			dt = self.__day2
			trading_data = pd.DataFrame()
			return dt, trading_data
		else:
			if self.__universe == 'allA' or isinstance(self.__universe, list):
				dt = self.__date_list[self.__count]
				trading_data = pd.read_csv(self.__path + '\\mktQuotation_bar_' + str(dt) + '.csv', encoding='GBK')
				trading_data.loc[:, 'date'] = datetime.datetime.strptime(str(dt), '%Y%m%d')
				if isinstance(self.__universe, list):
					# select the data in the universe
					trading_data = trading_data[[x in self.__universe for x in trading_data['sec_code']]]
				trading_data = trading_data.set_index('date')
				self.__count += 1
				return datetime.datetime.strptime(str(dt), '%Y%m%d'), trading_data

			elif self.__universe == 'zz500':
				trading_data = self.data.iloc[self.__count:self.__count+1,:]
				dt = self.__date_list[self.__count]
				self.__count += 1
				return dt, trading_data
			else:
				pass



	def __data_transform(self, df):
		df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'AMT']
		df['sec_code'] = 'zz500'
		df['trade_status'] = u'交易'
		df['maxupordown'] = 0
		df['adjfactor'] = 1
		df.loc[:, 't1'] = list(map(lambda t: t.strftime("%Y-%m-%d"), df['date']))
		df.loc[:, 't2'] = list(map(lambda t: t.strftime("-%H-%M"), df['time']))
		df.loc[:, 't'] = list(
			map(lambda t: datetime.datetime.strptime(t, "%Y-%m-%d-%H-%M"), df.loc[:, 't1'] + df.loc[:, 't2']))
		df = df.set_index('t')
		return df





def main():
	dd = datafeed(universe='zz500')
	dd.initialize()
	l = dd.time_length
	for i in range(0, l + 1):
		dt, temp = dd.data_fetch()
		print(dt)
	print(dd.data_fetch())


if __name__ == '__main__':
	from strat import *
	import datetime
	dd = datafeed(universe='zz500',begin_date="2013-01-01",
	              end_date="2015-11-01")
	dd.initialize()
	st = Strat('hl', 'allA', 5)
	for i in range(1000):
		date, temp = dd.data_fetch()
		signal = st.update(date, temp)


