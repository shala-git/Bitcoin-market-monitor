#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-09

import os,sys
sys.path.append("..")
import traceback
import urllib
import urllib2
import time
from influxdb import InfluxDBClient
import json
#from lib.api_service import WorkManager
from API.HuobiService import *

import config
from lib.logger_service import logger

class AccountBalance(object):
    '''
    '''
    def __init__(self):
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self.ticker_index={'btc','ustd','eth','ltc','etc','bch'}

    @property
    def name(self):
        return self._name

    def _getDataFromURL(self,index):
        try:
            textmod ={'market':index}
            textmod = urllib.urlencode(textmod)
            url = '%s%s%s' % (self._url,'?',textmod)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req, timeout=self._request_timeout)
            res = response.read()
            data = json.loads(res)
            buy_value = data['ticker']['buy']# buy value
            high_value = data['ticker']['high']#24h high value
            last_value = data['ticker']['last']#last value
            low_value = data['ticker']['low']#24h low value
            sell_value = data['ticker']['sell']#sell value
            vol_value = data['ticker']['vol'] #24Сʱ�ɽ���
            json_body = [
                {
                    "measurement": "ZB",
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

    def _get_balance(self):
        ret = False
        data = None

        data = get_balance()
        balance_list = data['data']['list']
        list_count = len(balance_list)
        for balance_index in balance_list:
            if balance_index['currency'] in self.ticker_index:
                print balance_index
                json_body = [
                    {
                        "measurement": "AccountBalance",
                        "tags": {
                            "currency": balance_index['currency']
                            "type": balance_index['type']
                        },
                        "fields": {
                            "balance": float(balance_index['balance'])
                        }
                    }
                ]
                self.client.write_points(json_body)
        print list_count

        #vol_value = data['ticker']['vol'] #24Сʱ�ɽ���
        data = None
        ret = True
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
        ret, data = self._get_balance()
        logger.info('request %s' % ret)
        #if ret:
        #    self._price = self._parse(data)
        #    logger.info('price %0.2f' % (self._price))
        return data

    def query_self(self):
        ret, data = self._get_balance()
        logger.info('request %s - "%s"' % (ret, data))
        #if ret:
        #    self._price = self._parse(data)
        #    logger.info('price %0.2f' % (self._price))
        return data

    pass

def main():
    p = AccountBalance()
    print p.query_self()
    pass

if __name__ == '__main__':
    main()
