#!/usr/bin/env python
#-*- coding:utf-8 -*-

PRICE_INTERFACE = {
        # zb价格接口
        'zb': 'http://api.zb.com/data/v1/ticker', #ZB市场接口
        'bithumb': 'https://api.bithumb.com/public/ticker/', #Bithumb市场接口
	'bitflyer': 'https://bitflyer.jp/api/echo/price', #bitflyer echo市场接口
	'okex': 'https://www.okex.com/api/v1/ticker',
	'huobi':'https://api.huobi.pro/market/detail/merged'
        }
EXCHANGE_INTERFACE = 'http://api.fixer.io/latest' # 汇率接口API
KRW_TO_USD = 0
KRW_TO_CNY = 0
USD_TO_CNY = 0
JPY_TO_CNY = 0
EXCHANGE_UPDATE_INTERVAL = 60 #汇率Update延时 60s
PRICE_UPDATE_INTERVAL = 5 #市场金额Update延时 5s
EXCHANGE_XXX = 190
