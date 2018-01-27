#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-09

import os,sys
import traceback
import urllib
import urllib2
import time
from influxdb import InfluxDBClient

import json

import config
from lib.logger_service import logger

class ZBPrice(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['zb']
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')
        self._price = 0.0
        self._name = 'http://www.zb.com'
        self.ticker_index={#'btc_usdt','bcc_usdt','ubtc_usdt','ltc_usdt','eth_usdt','etc_usdt','bts_usdt','eos_usdt','qtum_usdt','hsr_usdt','xrp_usdt'
        #,'bcd_usdt','dash_usdt',#
        'btc_qc',#bcc_qc,ubtc_qc,
        'ltc_qc',
        'eth_qc',
        'etc_qc',#bts_qc,
        'eos_qc',
        'qtum_qc',#hsr_qc,
        'xrp_qc',#bcd_qc,
        'dash_qc',#bcc_btc,ubtc_btc,ltc_btc,eth_btc,etc_btc,bts_btc,eos_btc,qtum_btc,hsr_btc,xrp_btc,bcd_
        #btc,dash_btc,
        #'sbtc_usdt',
        #sbtc_qc,sbtc_btc,
        #'ink_usdt',#ink_qc,ink_btc,
        #'tv_usdt',
        #tv_qc,tv_btc,
        #'bcx_usdt',
        #bcx_qc,bcx_btc,
        #'bth_usdt',
        #bth_qc,bth_btc,
        #'lbtc_usdt',
        #lbtc_qc,lbtc_btc,
        #'chat_usdt',
        #chat_qc,chat_btc,
        #'hlc_usdt',
        #hlc_qc,hlc_btc,
        #'bcw_usdt',
        #bcw_qc,bcw_btc,
        #'btp_usdt'}
        #,btp_qc,btp_btc,bitcny_qc
        }

    @property
    def name(self):
        return self._name

    def _wget(self):
        ret = False
        data = None
        try:
            for index in self.ticker_index:
                textmod ={'market':index}
                textmod = urllib.urlencode(textmod)
                req = urllib2.Request(url = '%s%s%s' % (self._url,'?',textmod))
                response = urllib2.urlopen(req, timeout=10)
                res = response.read()
                data = json.loads(res)
                value = data['ticker']['buy']
                json_body = [
                    {
                        "measurement": "ZB",
                        "tags": {
                        "coin": index,
                            "index": index 
                        },
                        "fields": {
                        "buy": float(value)
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
    p = ZBPrice()
    print p.query()
    pass

if __name__ == '__main__':
    main()

