#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-02-28

import os,sys
sys.path.append("..")
import traceback
import urllib
#import urllib2
import time
#from influxdb import InfluxDBClient
#from lib.api_service import WorkManager
from api.bithumb.easy_api import EasyAPI
from api.huobipro.HuobiServices import *
from api.influxdb.influxdb_helper import *
from settings import config

import json

#import config
#from lib.logger_service import logger

class PriceUpdater(object):
    '''
    '''
    def __init__(self, influxdb_client):
        #self._url = config.PRICE_INTERFACE['huobi']
        self.client=influxdb_client
        #self._request_timeout = int(config.REQUEST_TIMEOUT)
        self.exchange = {}
        self._name = 'PriceUpdater'

        self.bithumb_api=EasyAPI('','');

    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        num_of_threads = len(self.ticker_index)
        wm = WorkManager(num_of_threads)

        for index in self.ticker_index:
            wm.add_job(self._getDataFromURL, index)
        wm.start()
        wm.wait_for_complete()

        ret = True
        return ret,data

    def _parse(self, data):
        json_data = json.loads(data)
        price = float(json_data['ticker']['last'])
        return price

    def query(self):
        ret, data = self._wget()
        logger.info('request %s' % ret)
        #if ret:
        #    self._price = self._parse(data)
        #    logger.info('price %0.2f' % (self._price))
        return data

    def query_self(self):
        ret, data = self._wget()
        logger.info('request %s - "%s"' % (ret, data))
        #if ret:
        #    self._price = self._parse(data)
        #    logger.info('price %0.2f' % (self._price))
        return data

    def set_exchange(self, data):
        self.exchange = data
        pass

    def bithumb_updater(self, platform='bithumb'):
        res = self.bithumb_api.get_ticker('ALL')
        market_list = list(config.BITHUMB_MARKET)
        for index in market_list:
            if res['status'] == '0000':
                source = {}
                source['buy'] = res['data'][index]['buy_price']
                source['high'] = res['data'][index]['max_price']
                source['last'] = res['data'][index]['closing_price']
                source['low'] = res['data'][index]['min_price']
                source['sell'] = res['data'][index]['sell_price']

                #vol_value = data['data'][index]['volume_1day']
                insert_data = self.parse_influxdb_data(source,'bithumb',index)
                self.save(insert_data)
    def huobi_updater(self, platform='huobi'):
        i=0
        market_list = list(config.HUOBI_MARKET)
        while i < len(market_list):
            res = get_ticker(market_list[i])
            if res is None:
                continue
            else:
                source = {}
                source['buy'] = res['tick']['bid'][0]
                source['high'] = res['tick']['high']#���߼�
                source['last'] = res['tick']['close']#���³ɽ���
                source['low'] = res['tick']['low']#���ͼ�
                source['sell'] = res['tick']['ask'][0]#��һ��

                #vol_value = res['tick']['vol'] #24Сʱ�ɽ���

                insert_data = self.parse_influxdb_data(source,'huobi',market_list[i])
                self.save(insert_data)
            i += 1

    def parse_influxdb_data(self, source, platform, coin):
        if platform is 'huobi':
            db_data = [
                        {
                            "measurement": platform,
                            "tags": {
                                "coin": coin,
                                "base": config.TRADE_CURRENCY_BASE[platform]
                            },
                            "fields": {
                            "buy_usd": float(source['buy']),
                            "buy_cny": float(source['buy'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "high_usd": float(source['high']),
                            "high_usd": float(source['high'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "last_usd": float(source['last']),
                            "last_cny": float(source['last'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "low_usd": float(source['low']),
                            "low_cny": float(source['low'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "sell_usd": float(source['sell']),
                            "sell_cny": float(source['sell'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY'])
                            #"vol_usd":float(source['vol'])
                            }
                        }
                    ]
        if platform is 'bithumb':
            db_data = [
                        {
                            "measurement": platform,
                            "tags": {
                                "coin": coin,
                                "base": config.TRADE_CURRENCY_BASE[platform]
                            },
                            "fields": {
                            "buy_usd": float(source['buy'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "buy_cny": float(source['buy'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "high_usd": float(source['high'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "high_usd": float(source['high'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "last_usd": float(source['last'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "last_cny": float(source['last'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "low_usd": float(source['low'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "low_cny": float(source['low'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "sell_usd": float(source['sell'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "sell_cny": float(source['sell'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY'])
                            #"vol_usd":float(source['vol'])
                            }
                        }
                    ]

        return db_data
        pass
    def save(self, data):
        print(data)
        self.client.Insert(data)
        pass

    pass

def main():
    idb = InfluxDBHelper()
    exchangedata = {'KRW': {'CNY': 0.0058398, 'USD': 0.00091961}, 'USD': {'CNY': 6.3503, 'KRW': 1087.4}, 'CNY': {'KRW': 171.24, 'USD': 0.15747}}

    p = PriceUpdater(idb)
    p.set_exchange(exchangedata)
    p.bithumb_updater()
    p.huobi_updater()
    pass

if __name__ == '__main__':
    main()
