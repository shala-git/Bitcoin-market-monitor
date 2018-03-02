#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-03-01

PRICE_INTERFACE = {
        # zb价格接口
        'zb': 'http://api.zb.com/data/v1/ticker', #ZB市场接口
        'bithumb': 'https://api.bithumb.com/public/ticker/', #Bithumb市场接口
	'bitflyer': 'https://bitflyer.jp/api/echo/price', #bitflyer echo市场接口
	'okex': 'https://www.okex.com/api/v1/ticker',
	'huobi':'https://api.huobi.pro/market/detail/merged'
        }

EXCHANGE_BASE = 'CNY' # 汇率基础
EXCHANGE_TARGET = {'JPY','USD','KRW'}
EXCHANGE_UPDATE_INTERVAL = 60*60 #汇率Update延时 1小时

PRICE_UPDATE_FASTEST_INTERVAL = 5 #市场金额Update延时 最快 5s
PRICE_UPDATE_SLOWEST_INTERVAL = 5 #市场金额Update延时 最慢 5s

REQUEST_TIMEOUT = 5

BALANCE_UPDATE_INTERVAL = 60


EXCHANGE_XXX = 190

#INFLUXDB configs
INFLUXDB_IP = 'localhost'
INFLUXDB_PORT = 8086
INFLUXDB_USER = 'root'
INFLUXDB_DATABASE = 'grafana'

#Market资料
HUOBI_MARKET={'btcusdt','ethusdt','ltcusdt','etcusdt','bchusdt'} #火币
BITHUMB_MARKET={'ALL'} #bithumb
#各个平台API基础货币类型
TRADE_CURRENCY_BASE = {
        # zb价格接口
        'zb': 'http://api.zb.com/data/v1/ticker', #ZB市场基础币种
        'bithumb': 'KRW', #Bithumb市场基础币种
	'bitflyer': 'https://bitflyer.jp/api/echo/price', #bitflyer市场基础币种
	'okex': 'https://www.okex.com/api/v1/ticker',#okex市场基础币种
	'huobi':'USD'#火币市场基础币种
        }