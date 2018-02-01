#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-31

import os,sys
sys.path.append("..")
import traceback
import urllib
import urllib2
import time
from influxdb import InfluxDBClient

import json

import config
from lib.logger_service import logger
from lib.api_service import WorkManager

class OkexPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['okex']
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._request_timeout = int(config.REQUEST_TIMEOUT)
        self._price = 0.0
        self._name = 'http://www.okex.com'
        self.ticker_index={'btc_usdt', 'eth_usdt', 'ltc_usdt', 'etc_usdt', 'bch_usdt'}

    @property
    def name(self):
        return self._name

    def _getDataFromURL(self,index):
        try:
            textmod ='.do?symbol=%s' % index
            #textmod = urllib.urlencode(textmod)
            req = urllib2.Request(url = '%s%s' % (self._url,textmod))
            response = urllib2.urlopen(req, timeout=self._request_timeout)
            res = response.read()
            data = json.loads(res)
            buy_value = data['ticker']['buy']#ÂòÒ»¼Û
            high_value = data['ticker']['high']#×î¸ß¼Û
            last_value = data['ticker']['last']#×îÐÂ³É½»¼Û
            low_value = data['ticker']['low']#×îµÍ¼Û
            sell_value = data['ticker']['sell']#ÂôÒ»¼Û
            vol_value = data['ticker']['vol'] #24Ð¡Ê±³É½»Á¿
            json_body = [
                {
                    "measurement": "okex",
                    "tags": {
                    "coin": index,
                        "index": index
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
            self.client.write_points(json_body)
        except urllib2.HTTPError, e:
            logger.error('HTTP Error: %d\t%s\t%s\t%s' % (e.code, e.reason, e.geturl(), e.read()))
        except urllib2.URLError, e:
            logger.error('URL Error: %s ' % (e.reason))

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

    pass

def main():
    p = OkexPrice()
    print p.query_self()
    pass

if __name__ == '__main__':
    main()
