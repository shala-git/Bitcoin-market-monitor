#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-27

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

class BitflyerPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['bitflyer']
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'http://www.bitflyer.jp'
        self.ticker_index={'BTC'}

    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        try:
            textmod = ''
            #textmod = urllib.urlencode(textmod)
            req = urllib2.Request(url = '%s%s' % (self._url,textmod))
            response = urllib2.urlopen(req, timeout=10)
            res = response.read()
            data = json.loads(res)
            query = 'select last(value) from Exchange where index=\'JPY\'' 
            result = self.client.query(query)
            exchange_value = result.raw['series'][0]['values'][0][1]
            for index in self.ticker_index:
                value = data['ask']
                json_body = [
                    {
                        "measurement": "Bitflyer",
                        "tags": {
                        "coin": index,
                            "index": index 
                        },
                        "fields": {
                        "buy": float(value) / exchange_value,
			"buy_jpy": float(value)
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
    # {"ask":1209716.000000000000,"bid":1181044.000000000000,"mid":1195380.000000000000}
    def _parse(self, data):
        #json_data = json.loads(data)
        #price = float(json_data['ticker']['last'])
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
    p = BitflyerPrice()
    print p.query_self()
    pass

if __name__ == '__main__':
    main()


