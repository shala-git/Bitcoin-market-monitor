#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-05

import os,sys
import traceback
sys.path.append("..")
import urllib
import urllib2
import time
from influxdb import InfluxDBClient

import json

import config
from lib.logger_service import logger

class BithumbPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['bithumb']
        self._request_timeout = int(config.REQUEST_TIMEOUT)
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'http://www.bithumb.com'
        self.ticker_index={'BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP', 'BCH',# 'XMR', 'ZEC',
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
            response = urllib2.urlopen(req, timeout=self._request_timeout)
            res = response.read()
            data = json.loads(res)
            query = 'select last(value) from Exchange where index=\'KRW\''
            result = self.client.query(query)
            exchange_value = result.raw['series'][0]['values'][0][1]
            for index in self.ticker_index:

                buy_value = data['data'][index]['buy_price']
                high_value = data['data'][index]['max_price']
                last_value = data['data'][index]['closing_price']
                low_value = data['data'][index]['min_price']
                sell_value = data['data'][index]['sell_price']
                vol_value = data['data'][index]['volume_1day']

                json_body = [
                    {
                        "measurement": "Bithumb",
                        "tags": {
                        "coin": index,
                            "index": index
                        },
                        "fields": {
                        "buy": float(buy_value) / exchange_value,
                        "high":float(high_value) / exchange_value,
                        "last":float(last_value) / exchange_value,
                        "low":float(low_value) / exchange_value,
                        "sell":float(sell_value) / exchange_value,
                        "vol":float(vol_value) / exchange_value,
			            "buy_krw": float(buy_value),
                        "high_krw":float(high_value),
                        "last_krw":float(last_value),
                        "low_krw":float(low_value),
                        "sell_krw":float(sell_value)
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
    #{
    #"status": "0000",
    #"data": {
    #    "opening_price" : "504000",
    #    "closing_price" : "505000",
    #    "min_price"     : "504000",
    #    "max_price"     : "516000",
    #    "average_price" : "509533.3333",
    #    "units_traded"  : "14.71960286",
    #    "volume_1day"   : "14.71960286",
    #    "volume_7day"   : "15.81960286",
    #    "buy_price"     : "505000",
    #    "sell_price"    : "504000",
    #    "date"          : 1417141032622
    #   }
    #}
    def _parse(self, data):
        #json_data = json.loads(data)
        #price = float(data['ticker']['last'])
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

    pass

def main():
    p = BithumbPrice()
    print p.query_self()
    pass

if __name__ == '__main__':
    main()
