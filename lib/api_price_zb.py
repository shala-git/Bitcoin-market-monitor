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
from lib.api_service import WorkManager

import config
from lib.logger_service import logger

class ZBPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['zb']
        self._request_timeout = int(config.REQUEST_TIMEOUT)
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'http://www.zb.com'
        self.ticker_index={'btc_usdt','bcc_usdt',#'ubtc_usdt',
        'ltc_usdt','eth_usdt','etc_usdt',#'bts_usdt','eos_usdt','qtum_usdt','hsr_usdt','xrp_usdt'
        #,'bcd_usdt','dash_usdt',#
        'btc_qc',#bcc_qc,ubtc_qc,
        'ltc_qc',
        'eth_qc',
        'etc_qc',#bts_qc,
        'eos_qc',
        'qtum_qc',#hsr_qc,
        'xrp_qc',#bcd_qc,
        'dash_qc'
        }

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
    p = ZBPrice()
    print p.query_self()
    pass

if __name__ == '__main__':
    main()
