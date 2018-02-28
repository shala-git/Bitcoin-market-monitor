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
#from lib.api_service import WorkManager

import json

#import config
#from lib.logger_service import logger

class InfluxDBHelper(object):
    '''
    '''
    def __init__(self):
        self._url = config.PRICE_INTERFACE['huobi']
        self.client=InfluxDBClient('localhost',8086,'root',',','grafana')

    def _getDataFromURL(self,json_body):
        try:
            lock.acquire()
            self.client.write_points(json_body)
            lock.release()
        except (Exception):
            logger.error('HTTP Error: %d\t%s\t%s\t%s' % (e.code, e.reason, e.geturl(), e.read()))

def main():
    print(get_ticker("btcusdt"))
    pass

if __name__ == '__main__':
    main()
