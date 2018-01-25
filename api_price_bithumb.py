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

class BithumbPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['bithumb']
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'http://www.bithumb.com'
        self.ticker_index={'BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP', #'BCH', 'XMR', 'ZEC', 
        'QTUM', #'BTG', 
        'EOS'}

    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        try:
            textmod = 'ALL'
            #textmod = urllib.urlencode(textmod)
            req = urllib2.Request(url = '%s%s' % (self._url,textmod))
            response = urllib2.urlopen(req, timeout=10)
            res = response.read()
            data = json.loads(res)
            query = 'select last(value) from Exchange where index=\'KRW\'' 
            result = self.client.query(query)
            exchange_value = result.raw['series'][0]['values'][0][1]
            for index in self.ticker_index:
                value = data['data'][index]['buy_price']
                json_body = [
                    {
                        "measurement": "Bithumb",
                        "tags": {
                        "coin": index,
                            "index": index 
                        },
                        "fields": {
                        "buy": float(value) / exchange_value,
			"buy_krw": float(value)
                        }
                    }
                ]
                self.client.write_points(json_body)
            ret = True
        except urllib2.HTTPError, e:
            logger.error('HTTP Error: %d\t%s\t%s\t%s' % (e.code, e.reason, e.geturl(), e.read()))
        except urllib2.URLError, e:
            logger.error('URL Error: %s' % (e.reason))
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
    p = BithumbPrice()
    print p.query()
    pass

if __name__ == '__main__':
    main()

