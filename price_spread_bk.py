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
from lib.logger_service import logger


class SpreadPrice(object):
    '''
    '''
    def __init__(self):
        self._exchange = config.EXCHANGE_XXX
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'Spread'
        self.bithumb_ticker_index=['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP', 'QTUM', 'EOS']
        self.zb_ticker_index=['btc_qc','eth_qc','dash_qc','ltc_qc','etc_qc','xrp_qc','qtum_qc','eos_qc']
    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        try:
            query = 'select last(value) from Exchange where index=\'KRW\'' 
            result = self.client.query(query)
            exchange_value = result.raw['series'][0]['values'][0][1]

            for i in range(0, len(self.bithumb_ticker_index)):
                print self.bithumb_ticker_index[i]
                query = 'select last(buy) from ZB where index=\'' + self.zb_ticker_index[i] + '\'' 
                result = self.client.query(query)
                zb_value = result.raw['series'][0]['values'][0][1]
                query = 'select last(buy_krw) from Bithumb where index=\''+self.bithumb_ticker_index[i]+'\''
                result = self.client.query(query)
                bithumb_value = result.raw['series'][0]['values'][0][1]
                if i == 0:
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = ((float(bithumb_value) * 9.98 / self._exchange - float(zb_value)) * 100000
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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
                    spread_value = float(bithumb_value) * float(exchange_value) *0.998 *0.99925 / self._exchange - float(zb_value)
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

    # request json sample:
    #
    #     {
    #         "ticker": {
    #             "high": "1473.89",
    #             "low": "1361.00",
    #             "buy": "1445.01",
    #             "sell": "1445.95",
    #             "last": "1443.07",
    #             "vol": "47175.19000000"
    #         }
    #     }
    def _parse(self, data):
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

