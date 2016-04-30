# -*- encoding=utf8 -*-
"""
@author: Jerry
@contact: lvjy3.15@sem.tsinghua.edu.com
@file: datafeed.py
@time: 2016/4/30 14:37
"""

import os
import pandas as pd



def hist_data_fetch(universe,begin_date,end_date,path='E:\\data'):
	'''
	:param universe: only support 'allA' or 'zz500' now
	:param begin_date:
	:param end_date:
	:param path: default path 'E:\\data'
	:return: historical stock data
	'''

	if universe=='allA':
		path=path+'\\mktQuotation_bar'
		dates=list(map(lambda x:(x[-12:-4]),os.listdir(path)))



	elif universe=='zz500':
		xlsx = pd.ExcelFile(path+'\\中证500测试数据.xlsx')
		df = pd.read_excel(xlsx, 'Sheet1')
		df.columns = ['date','time','open','high','low','close','volume','AMT']
		df = df.set_index('date')
		df = df[begin_date:end_date]

	else:
		raise ValueError("No such data type" )

	return df

def cur_data_fetch(universe,date,path='E:\\data'):
	if universe=='allA':
		path = path+'\\mktQuotation_bar'
	elif universe=='zz500':
		pass
	else:
		raise ValueError("No such data type" )
	pass

def main():
	universe='zz500'
	begin_date='20130101'
	end_date='20130110'
	hist_data_fetch(universe,begin_date,end_date,path='E:\\data')


if __name__ == '__main__':
	main()