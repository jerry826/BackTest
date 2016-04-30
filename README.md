# BackTest
Quantitative trade back-test platform

# 回测框架

## 数据模块：datafeed

负责数据读取，清理，转换

Input：股票日度交易csv文件 或者 股指高频数据

Output：每日行情数据文件，如20150101.csv

## 策略模块：strat

负责策略逻辑，给出交易指令 

Input：交易品种的bars，Open-High-Low-Close-Volume (OHLCV)
Output: 信号signals，取值为(id,1,0,-1)，分别表示buy,hold,sell

## 交易模块：broker

负责接收并处理交易指令，包括模拟成交情况（如有），计算交易成本（非必须），计算交易冲击成本（非必须）

Input：交易信号
Output:  交易相关数据的tracing（仓位，交易费用，资金流）

## 组合模块：portfolio

负责动态计算



## 回测表现模块：analyzer

负责分析策略表现，提供净值曲线，年化收益率，年化波动率，最大回撤等指标的计算和输出

Inputs：交易相关数据
Output：策略评价指标，图形，回测报告等

## 风控模块：risk

根据实时数据返回当前情况下的账户风险指标，包括资金使用情况、剩余资金量、杠杆率、VaR这些信息。

Inputs：账户持仓信息

Output：风险指标



