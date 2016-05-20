# BackTest
Quantitative trade back-test platform

# 回测框架

## 回测模块：BackTest
回测框架

1. 可参考demo.py
2. 继承BackTest类
3. 在handle_data中实现策略并完成回测，主要可以从broker中获得历史持仓信息，从strat中获得指标、信号等信息，并通过broker下单

主要初始化参数：
* model_name：自定义模型名称
* begin_time：回测起始时间，格式 "2011-02-01"
* end_time：回测结束时间，格式 "2011-02-01"
* path：数据所在路径
* universe：股票池，支持'allA'，'zz500'，和自定义股票列表
* freq：策略刷新时间，默认为5
* length：所需历史时间长度（越短系统占用资源越少）
* lag：信息滞后期，默认为1，即交易日只能使用交易日前一天以及之前的股价信息
* short：是否允许做空，默认为False
* price_type：交易结算价，默认为'close'，可选'vwap','open'等
* output：是否输出中间结果，默认为False



## 数据模块：datafeed
### datafeed类，作为回测引擎
负责数据读取，清理，转换

1. 读取股票日度交易csv文件或者股指高频数据（支持universe='allA' 'zz500' 股票列表三种选择，不可更改）
2. 记录当前时间t
API:
* datafeed.data_fetch(返回一天的交易数据并自动更新内部时间)


## 策略模块：strat
### strat类
负责策略计算和信号输出

1. 从datafeed中获取数据，管理时间序列数据流，**捕获新值释放旧值**（指标计算跨度n和延时l）。
2. 输入策略逻辑，计算指标数值
3. 

API:
* strat.update(dt,df) 更新来自datafeed的数据
* strat.gen_signal(data,name) 生成一些个性化信号
* strat.MA(length,price) length期移动平均，price可以是close，open，high，low（复权价）
* strat.MACD() MACD线
* strat.history(length,data_type,universe) 批量返回历史数据，长度为length，universe为代码列表，data_type默认'ohlca'


## 交易模块：broker
### broker类
负责接收并处理交易指令，包括模拟成交情况（如有），计算交易成本（非必须），计算交易冲击成本（非必须）

1. 获取来自strat的交易信号，获取port的前一交易日的持仓，获取内部的前一日未完成交易
2. 根据前一日未完成交易信号更新来自strat的交易信号
3. 根据涨跌停处理交易信号，产生可执行交易和延迟交易
4. 根据前一日的持仓和交易信号计算当前持仓
5. 计算成交金额
6. 计算手续费金额

API：
* broker.get_universe() 返回当前交易日的可交易股票列表
* broker.order(symbol, amount) 买入（卖出）数量为amount的股票symbol
* broker.order_to(symbol, amount) 买入（卖出）一定量的股票使得股票symbol交易后的数量为amount
* broker.order_pct(symbol, amount)买入（卖出）价值为当前总价值的pct部分的证券symbol
* broker.order_pct_to(symbol, amount)买入（卖出）证券symbol使得其价值为虚拟账户当前总价值的pct部分
* broker.portfolio_value() 返回当前账户总价值
* broker.get_cash() 返回当前账户现价余额
* broker.get_hist_log() 返回历史订单列表
* broker.get_position(symbol) 返回某只股票的当前仓位
* broker.get_weight(symbol) 返回某只股票的当前所占仓位比例
* broker.get_hist_perf() 返回账户历史净值列表
* broker.get_position_report() 返回历史净值列表

## 组合模块：portfolio
### port类
负责动态计算

1. 获取来自broker的交易结果，更新当前仓位，现金量
2. 更新每日盈亏
3. 更新个股持仓时间
4. 更新其他跟踪数据

## 回测表现模块：analyzer
### analyzer类
负责分析策略表现，提供净值曲线，年化收益率，年化波动率，最大回撤等指标的计算和输出

1. 计算评价指标，包括夏普值，年化平均收益率，最大回撤，年化历史波动率
2. 图形展示
3. 输出回测报告，包括仓位表，收盘价表，历史表现评价表

## 风控模块：risk
### risk类
根据实时数据返回当前情况下的账户风险指标，包括资金使用情况、剩余资金量、杠杆率、VaR这些信息。

1. 获取来自port的持仓信息
2. 计算资金使用情况，杠杆率，剩余资金，盈亏比
3. 计算日度VaR(0.999)
4. 输出风险评价表




