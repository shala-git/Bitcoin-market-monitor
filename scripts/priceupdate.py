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
from api.bithumb.easy_api import EasyAPI
from api.huobipro.HuobiServices import *
from api.okcoin.OkcoinSpotAPI import OKCoinSpot
from settings import config
from lib.arbitrage_calculate import calculate
from lib.timeformat import *

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
        self.okcoinSpot = OKCoinSpot(config.OKCOIN_RESTURL,'','')

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
        try:
            print('bithumb price updater')
            self.bithumb_updater()
            print('huobi price updater')
            self.huobi_updater()
            print('okcoin price updater')
            self.okcoin_updater()
            print('arbitrage calculation')
            arbitrage = calculate.run_calculate()
            if arbitrage is not None:
                self.client.Insert(arbitrage)
                pass
            return True
        except Exception as e:
            print (e)
            #logger.error('Error: %s' % str(e))
            return False

    def set_exchange(self, data):
        self.exchange = data
        calculate.set_exchange(data)
        pass

    def bithumb_updater(self, platform='bithumb'):
        try:
            res = self.bithumb_api.get_ticker('ALL')
            market_list = list(config.BITHUMB_MARKET)
            for index in market_list:
                if res['status'] == '0000':
                    source = {}
                    source['time'] = timestamp2rfc3339(int(res['data']['date']))
                    source['buy'] = res['data'][index]['buy_price']
                    source['high'] = res['data'][index]['max_price']
                    source['last'] = res['data'][index]['closing_price']
                    source['low'] = res['data'][index]['min_price']
                    source['sell'] = res['data'][index]['sell_price']

                    #vol_value = data['data'][index]['volume_1day']
                    insert_data = self.parse_influxdb_data(source,'bithumb',index)
                    self.save(insert_data)
        except Exception as e:
                print(e)
    def huobi_updater(self, platform='huobi'):
        i=0
        market_list = list(config.HUOBI_MARKET)
        while i < len(market_list):
            try:
                res = get_ticker(market_list[i])
                if res is None:
                    continue
                else:
                    source = {}
                    source['time'] = timestamp2rfc3339(int(res['ts']))
                    source['buy'] = res['tick']['bid'][0]
                    source['high'] = res['tick']['high']#���߼�
                    source['last'] = res['tick']['close']#���³ɽ���
                    source['low'] = res['tick']['low']#���ͼ�
                    source['sell'] = res['tick']['ask'][0]#��һ��

                #vol_value = res['tick']['vol'] #24Сʱ�ɽ���

                    insert_data = self.parse_influxdb_data(source,'huobi',market_list[i])
                    self.save(insert_data)
            except Exception as e:
                print(e)
            i += 1

    def okcoin_updater(self, platform='okcoin'):
        i=0
        market_list = list(config.OKCOIN_MARKET)
        while i < len(market_list):
            try:
                res = self.okcoinSpot.ticker(market_list[i])
                if res is None:
                    continue
                else:
                    source = {}
                    source['time'] = timestamp2rfc3339(int(res['date']))
                    source['buy'] = res['ticker']['buy']
                    source['high'] = res['ticker']['high']#���߼�
                    source['last'] = res['ticker']['last']#���³ɽ���
                    source['low'] = res['ticker']['low']#���ͼ�
                    source['sell'] = res['ticker']['sell']#��һ��

                    #vol_value = res['tick']['vol'] #24Сʱ�ɽ���
                    
                    insert_data = self.parse_influxdb_data(source,'okcoin',market_list[i])
                    self.save(insert_data)
            except Exception as e:
                print(e)
            i += 1

    def parse_influxdb_data(self, source, platform, coin):
        if platform is 'huobi' or 'okcoin':
            db_data = [
                        {
                            "measurement": platform,
                            "tags": {
                                "coin": coin,
                                "base": config.TRADE_CURRENCY_BASE[platform]
                            },
                            "time":source['time'],
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
                            "time":source['time'],
                            "fields": {
                            "buy_usd": float(source['buy'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "buy_cny": float(source['buy'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "buy_krw": float(source['buy']),
                            "high_usd": float(source['high'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "high_cny": float(source['high'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "high_krw": float(source['high']),
                            "last_usd": float(source['last'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "last_cny": float(source['last'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "last_krw": float(source['last']),
                            "low_usd": float(source['low'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "low_cny": float(source['low'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "low_krw": float(source['low']),
                            "sell_usd": float(source['sell'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['USD']),
                            "sell_cny": float(source['sell'])*float(self.exchange[config.TRADE_CURRENCY_BASE[platform]]['CNY']),
                            "sell_krw": float(source['sell'])
                            #"vol_usd":float(source['vol'])
                            }
                        }
                    ]

        return db_data
        pass
    def save(self, data):
        if data[0]['tags']['coin'].lower().find('btc') > -1:
            #print (data[0]['measurement'])
            #print (data)
            calculate.set_price_data(data[0]['measurement'], data)
        self.client.Insert(data)
        pass

    pass

def main():
    #idb = InfluxDBHelper()
    exchangedata = {'KRW': {'CNY': 0.0058398, 'USD': 0.00091961}, 'USD': {'CNY': 6.3503, 'KRW': 1087.4}, 'CNY': {'KRW': 171.24, 'USD': 0.15747}}

    p = PriceUpdater(None)
    p.set_exchange(exchangedata)
    p.query()
    pass

if __name__ == '__main__':
    main()
