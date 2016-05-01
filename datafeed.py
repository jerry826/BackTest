# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: datafeed.py
@time: 2016/4/30 14:37
"""

import os
from datetime import datetime
import pandas as pd
import numpy as np




class datafeed(object):
	'''
	datafeed
	'''
	def __init__(self,universe='allA',begin_date='2014-01-01',end_date='2015-01-01',path='E:\\data'):
		'''

		'''
		self.__universe=universe
		self.__begin_date=begin_date
		self.__end_date=end_date
		self.__path=path
		self.__data=pd.DataFrame()

	def initialize(self):
		'''

		:return:
		'''
		print('########  Read data  ########')

		self.__data=pd.DataFrame()
		if self.__universe=='allA':
			path=self.__path+'\\mktQuotation_bar'
			dates=[int(x[-12:-4]) for x in os.listdir(path)[:-1]]
			begin_date=int(''.join(self.__begin_date.split('-')))
			end_date=int(''.join(self.__end_date.split('-')))
			dates=[x for x in dates if (x >= begin_date and x <= end_date)]
			for date in dates:
				temp=pd.read_csv(path+'\\mktQuotation_bar_'+str(date)+'.csv',encoding='GBK')
				temp.loc[:,'date']=datetime.strptime(str(date),'%Y%m%d')
				self.__data=self.__data.append(temp)
			self.__data=self.__data.set_index('date')

		elif self.__universe=='zz500':
			xlsx=pd.ExcelFile(self.__path+'\\中证500测试数据.xlsx')
			df=pd.read_excel(xlsx, 'Sheet1')
			df.columns=['date','time','open','high','low','close','volume','AMT']
			df=df.set_index('date')
			self.__data=df[self.__begin_date:self.__end_date]
		else:
			raise ValueError("No such data type" )
		if len(self.__data) == 0:
			raise ValueError("The data required is not available" )

		print('Get '+str(len(self.__data))+' obersevations from '+self.__begin_date+' to '+self.__end_date)
		print('########     Done    ########')



	def hist_data_fetch(self,begin_date,end_date):
		'''
		:param begin_date:  format '2011-01-01'
		:param end_date: format '2011-01-01'
		:return: multi periods historical stock data
		'''
		if  int(''.join(begin_date.split('-'))) > int(''.join(end_date.split('-'))):
			raise ValueError("Begin date should be equal or smaller than end date")
		else:
			return self.__data[begin_date:end_date]




def main():
	dd=datafeed(universe='zz500')
	dd.initialize()
	df= dd.hist_data_fetch('2014-02-02','2014-03-01')

if __name__ == '__main__':
	pass