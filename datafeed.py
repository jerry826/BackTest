# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: datafeed.py
@time: 2016/4/30 14:37
"""

from datetime import *
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

		if self.__universe == 'allA':
			self.__path = self.__path + '\\mktQuotation_bar'  # set the path
			self.__date_list = sorted([int(x[-12:-4]) for x in os.listdir(self.__path)[:-1]])  # get the date list

			self.__date_list = [x for x in self.__date_list if
			                    x >= int(''.join(self.__begin_date.split('-'))) and x <= int(
				                    ''.join(self.__end_date.split('-')))]


			self.__length = len(self.__date_list)  # get the length of date list
			self.__day1 = str(self.__date_list[0])
			self.__day2 = str(self.__date_list[-1])
			self.__day1 = self.__day1[0:4] + '-' + self.__day1[4:6] + '-' + self.__day1[6:8]
			self.__day2 = self.__day2[0:4] + '-' + self.__day2[4:6] + '-' + self.__day2[6:8]
		# begin_date = int(''.join(self.__begin_date.split('-')))
		# end_date = int(''.join(self.__end_date.split('-')))
		# dates = [x for x in dates if (x >= begin_date and x <= end_date)]
		# for date in dates:
		#	temp = pd.read_csv(path + '\\mktQuotation_bar_' + str(date) + '.csv', encoding='GBK')
		#	temp.loc[:, 'date'] = datetime.strptime(str(date), '%Y%m%d')
		#	self.__data = self.__data.append(temp)
		# self.__data = self.__data.set_index('date')


		# elif self.__universe == 'zz500':
		#	xlsx = pd.ExcelFile(self.__path + '\\中证500测试数据.xlsx')
		##	df = pd.read_excel(xlsx, 'Sheet1')
		#	df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume', 'AMT']
		#	df = df.set_index('date')
		#	self.__data = df[self.__begin_date:self.__end_date]
		else:
			raise ValueError("No such data type")
		# if len(self.__data) == 0:
		#	raise ValueError("The data required is not available")

		print('Get ' + str(self.__length) + ' obersevations from ' + str(self.__day1) + ' to ' + str(self.__day2))
		print('########     Done     ########')

	def data_fetch(self):
		if self.__count == self.__length:
			print('No more data avaiable')
			date = self.__day2
			temp = pd.DataFrame()
		else:
			date = self.__date_list[self.__count]
			temp = pd.read_csv(self.__path + '\\mktQuotation_bar_' + str(date) + '.csv', encoding='GBK')
			temp.loc[:, 'date'] = datetime.strptime(str(date), '%Y%m%d')
			temp = temp.set_index('date')
			self.__count += 1

		return datetime.strptime(str(date), '%Y%m%d'), temp







def main():
	dd = datafeed(universe='allA')
	dd.initialize()
	l = dd.time_length
	for i in range(0, l + 1):
		date, temp = dd.data_fetch()
		print(date)
	print(dd.data_fetch())


if __name__ == '__main__':
	from strat import *

	dd = datafeed(universe='allA')
	dd.initialize()
	st = strat('hl', 'allA', 5)
	for i in range(1000):
		date, temp = dd.data_fetch()
		signal = st.update(date, temp)
