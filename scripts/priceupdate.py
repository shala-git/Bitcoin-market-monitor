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
        
    def huobi_updater(self, platform='huobi'):
        print(self.exchange['KRW']['CNY'])
        i=0
        market_list = list(config.HUOBI_MARKET) 
        while i < len(market_list):
            res = get_ticker(market_list[i])
            if res is None:
                continue
            else:
                buy_value = res['tick']['bid'][0]
                high_value = res['tick']['high']#���߼�
                last_value = res['tick']['close']#���³ɽ���
                low_value = res['tick']['low']#���ͼ�
                sell_value = res['tick']['ask'][0]#��һ��
                vol_value = res['tick']['vol'] #24Сʱ�ɽ���
                json_body = [
                    {
                        "measurement": "huobi",
                        "tags": {
                        "coin": market_list[i],
                            "index": market_list[i]
                        },
                        "fields": {
                        "buy": float(buy_value),
                        "high":float(high_value),
                        "last":float(last_value),
                        "low":float(low_value),
                        "sell":float(sell_value),
                        "vol":float(vol_value)
                        }
                    }
                ]
                print (json_body)
                #self.client.Insert(json_body)
            i += 1
            
    def parse_influxdb_data(self, source, platform):
        if config.TRADE_CURRENCY_BASE[platform] is 'USD'
        
        db_data = [
                    {
                        "measurement": platform,
                        "tags": {
                            "coin": market_list[i],
                            "base": market_list[i]
                        },
                        "fields": {
                        "buy_usd": float(source['buy']),
                        "buy_cny": float(source['buy']*float(self.exchange['USD']['CNY'])),
                        "high":float(high_value),
                        "last":float(last_value),
                        "low":float(low_value),
                        "sell":float(sell_value),
                        "vol":float(vol_value)
                        }
                    }
                ]
        return db_data
        pass

    pass

def main():
    idb = InfluxDBHelper()
    exchangedata = {'KRW': {'CNY': 0.0058398, 'USD': 0.00091961}, 'USD': {'CNY': 6.3503, 'KRW': 1087.4}, 'CNY': {'KRW': 171.24, 'USD': 0.15747}}
    
    p = PriceUpdater(idb)
    p.set_exchange(exchangedata)
    p.huobi_updater()
    pass

if __name__ == '__main__':
    main()
