# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: datafeed.py
@time: 2016/4/30 14:37
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime


def hist_data_fetch(universe,begin_date,end_date,path='E:\\data'):
	'''
	:param universe: only support 'allA' or 'zz500' now
	:param begin_date:  format '2011-01-01'
	:param end_date: format '2011-01-01'
	:param path: default path 'E:\\data'
	:return: multi periods historical stock data
	'''

	if universe=='allA':
		path=path+'\\mktQuotation_bar'
		dates=[int(x[-12:-4]) for x in os.listdir(path)[:-1]]
		begin_date=int(''.join(begin_date.split('-')))
		end_date=int(''.join(end_date.split('-')))
		dates=[x for x in dates if (x >= begin_date and x <= end_date)]
		df = pd.DataFrame()
		for date in dates:
			temp=pd.read_csv(path+'\\mktQuotation_bar_'+str(date)+'.csv',encoding='GBK')
			temp.loc[:,'date']=datetime.strptime(str(date),'%Y%m%d')
			df = df.append(temp)

	elif universe=='zz500':
		xlsx=pd.ExcelFile(path+'\\中证500测试数据.xlsx')
		df=pd.read_excel(xlsx, 'Sheet1')
		df.columns=['date','time','open','high','low','close','volume','AMT']
		df=df.set_index('date')
		df=df[begin_date:end_date]
	else:
		raise ValueError("No such data type" )
	if len(df) == 0:
		raise ValueError("The data required is not available" )
	return df

def cur_data_fetch(universe,date,path='E:\\data'):
	'''
	:param universe:  only support 'allA' or 'zz500' now
	:param date:  format '2011-01-01'
	:param path:  default path 'E:\\data'
	:return: one period historical stock data
	'''
	if universe=='allA':
		path=path+'\\mktQuotation_bar'
		date=int(''.join(date.split('-')))
		df=pd.read_csv(path+'\\mktQuotation_bar_'+str(date)+'.csv',encoding='GBK')
		df.loc[:,'date']=datetime.strptime(str(date),'%Y%m%d')
	elif universe=='zz500':
		xlsx=pd.ExcelFile(path+'\\中证500测试数据.xlsx')
		df=pd.read_excel(xlsx, 'Sheet1')
		df.columns=['date','time','open','high','low','close','volume','AMT']
		df=df.set_index('date')
		df=df.loc[df.index==date,:]
	else:
		raise ValueError("No such data type" )
	if len(df) == 0:
		raise ValueError("The data required is not available" )
	return df


def main():
	universe='allA'
	begin_date='2013-01-01'
	end_date='2013-01-10'
	data = hist_data_fetch(universe,begin_date,end_date,path='E:\\data')
	return data

if __name__ == '__main__':
	main()