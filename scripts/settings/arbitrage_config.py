#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-03-06

#HUOBI_TRADE_FEE = 0.02 #火币买入费率
#HUOBI_TRANSFER_FEE = 0.001 #火币转币费率

TRADE_FEE ={'huobi':0.002,'bithumb':0.0015,'bithumb_coupon':0.00075}#买入费率
TRANSFER_FEE = {'huobi':0.001}#转币费率
ARBITRAGE_SOURCE = {'huobi'}
ARBITRAGE_TARGET = {'bithumb','bithumb_coupon'}
