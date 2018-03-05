#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-03-01

import os,sys
import traceback
import urllib
#import urllib2
import time
import threading
from influxdb import InfluxDBClient
#from lib.api_service import WorkManager

import json
from settings import config
#from lib.logger_service import logger

class InfluxDBHelper(object):
    '''
    '''
    def __init__(self, dbname=None):
        if dbname is None:
            self.client=InfluxDBClient(config.INFLUXDB_IP,config.INFLUXDB_PORT,config.INFLUXDB_USER,',',config.INFLUXDB_DATABASE)
        else:
            self.client=InfluxDBClient(config.INFLUXDB_IP,config.INFLUXDB_PORT,config.INFLUXDB_USER,',',dbname)
        self.lock = threading.Lock()
    def Insert(self,json_body):
        try:
            if self.lock.acquire():
                self.client.write_points(json_body)
                #print('saved')
                self.lock.release()
        except Exception as e:
            print (e)
        #    logger.error('HTTP Error: %d\t%s\t%s\t%s' % (e.code, e.reason, e.geturl(), e.read()))

def main():
    test_json_body = [
                {
                    "measurement": "testdb",
                    "tags": {
                    "coin": 'test1',
                        "index": 'test2'
                    },
                    "fields": {
                    "buy": 1,
                    "high":2,
                    "last":3,
                    "low":4,
                    "sell":5,
                    "vol":666
                    }
                }
            ]
    idb = InfluxDBHelper()
    idb.Insert(test_json_body)
    pass

if __name__ == '__main__':
    main()
