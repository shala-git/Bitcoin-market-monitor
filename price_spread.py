#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import os,sys
import traceback
import urllib
import urllib2
import time
from influxdb import InfluxDBClient

import json

import config
#from lib.logger_service import logger


class SpreadPrice(object):
    '''
    '''
    def __init__(self):
        self._exchange = config.EXCHANGE_XXX
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'Spread'
        self.bithumb_ticker_index=['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP', 'QTUM', 'EOS'] #bithumb市场
        self.zb_ticker_index=['btc_qc','eth_qc','dash_qc','ltc_qc','etc_qc','xrp_qc','qtum_qc','eos_qc'] #ZB市场
    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        try:
            #从数据库中取得最后的汇率
            query = 'select last(value) from Exchange where index=\'KRW\''
            result = self.client.query(query)
            exchange_value = result.raw['series'][0]['values'][0][1]
            
            #从数据库中取得最后插入的数据
            for i in range(0, len(self.bithumb_ticker_index)):
                print self.bithumb_ticker_index[i]
                query = 'select last(buy) from ZB where index=\'' + self.zb_ticker_index[i] + '\''
                result = self.client.query(query)
                zb_value = result.raw['series'][0]['values'][0][1]
                query = 'select last(buy_krw) from Bithumb where index=\''+self.bithumb_ticker_index[i]+'\''
                result = self.client.query(query)
                bithumb_value = result.raw['series'][0]['values'][0][1]
                #根据公式求的所需数据
                if i == 0:
                    #BTC
                    spread_value = (float(bithumb_value) *0.998 / self._exchange - float(zb_value)) * 100000 / float(zb_value)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 1:
                    #ETH
                    spread_value = ((float(bithumb_value) *9.98 / self._exchange - (float(zb_value) * 10)) * 100000)/(float(zb_value)*10)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 2:
                    #DASH
                    spread_value = (float(bithumb_value) *14.983 / self._exchange - (float(zb_value) * 15)) * 100000/(float(zb_value)*15)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 3:
                    #LTC
                    spread_value = (float(bithumb_value) *59.93 / self._exchange - (float(zb_value) * 60)) * 100000/(float(zb_value)*60)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 4:
                    #ETC
                    spread_value = (float(bithumb_value) *299.69 / self._exchange - (float(zb_value) * 300)) * 100000/(float(zb_value)*300)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 5:
                    #XRP
                    spread_value = (float(bithumb_value) *7991.9 / self._exchange - (float(zb_value) * 8000)) * 100000/(float(zb_value)*8000)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 6:
                    #QTUM
                    spread_value = (float(bithumb_value) *299.69 / self._exchange - (float(zb_value) * 300)) * 100000/(float(zb_value)*300)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
                if i == 7:
                    #EOS
                    spread_value = (float(bithumb_value) *998 / self._exchange - (float(zb_value) * 1000)) * 100000/(float(zb_value)*1000)
                    json_body = [
                        {
                            "measurement": "Spread",
                            "tags": {
                            "coin": self.bithumb_ticker_index[i],
                                "index": self.bithumb_ticker_index[i]
                            },
                            "fields": {
                            "spread": spread_value
                            }
                        }
                    ]
                    self.client.write_points(json_body)
            ret = True
        except :
            pass

        return ret,data
        json_data = json.loads(data)
        price = float(json_data['ticker']['last'])
        return price

    def query(self):
        ret, data = self._wget()
        #logger.info('request %s - "%s"' % (ret, data))
        #if ret:
        #    self._price = self._parse(data)
        #    logger.info('price %0.2f' % (self._price))
        return data

    pass

def main():
    p = SpreadPrice()
    print p.query()
    pass

if __name__ == '__main__':
    main()

