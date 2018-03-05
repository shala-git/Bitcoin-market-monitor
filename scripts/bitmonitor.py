#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-11
import sys,os
import time
import traceback
from settings import config
from priceupdate import *
from api.influxdb.influxdb_helper import *
from exchange import *

class BitMonitor(object):
    '''
    '''
    def __init__(self):
        self._agents = []


        self.exchange_data = {}
        self.exchange_client = Exchange()
        ex_td = threading.Thread(target=self.update_exchange)
        self.isRun = True
        ex_td.start()
        #logger.info('Exchange updater start')

        self.idb = InfluxDBHelper()
        self.pum = PriceUpdater(self.idb)
        self._load_agent()

        pass

    def _load_agent(self):
        # add agent
        agent_priceupdater = self.pum
        self._agents.append(agent_priceupdater)

        # add other transaction agent
        # ...
        pass

    def update_price(self):
        #raise NameError('Exception Raise')
        #logger.info('Main module task start')
        #logger.info('Price module task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            #logger.info('agent "%s"' % (agent.name))
            # get price
            #exchangedata = {'KRW': {'CNY': 0.0058398, 'USD': 0.00091961}, 'USD': {'CNY': 6.3503, 'KRW': 1087.4}, 'CNY': {'KRW': 171.24, 'USD': 0.15747}}
            #agent.set_exchange(exchangedata)
            ret = agent.query()
            if not ret:
                #logger.error('query failed, skip "%s"' % (agent.name))
                continue
        pass

    def exchange_callback(self, dic):
        self.exchange_data = dic
        self.pum.set_exchange(self.exchange_data)
        print

    def update_exchange(self):
        while self.isRun:
            self.exchange_client.query(self.exchange_callback)
            time.sleep(config.EXCHANGE_UPDATE_INTERVAL)

    def run(self):
        while self.isRun:
            try:
                self.update_price()
            except Exception as e:
                #logger.error(traceback.format_exc())
                #logger.error(str(e))
                pass
            time.sleep(config.PRICE_UPDATE_FASTEST_INTERVAL)
            pass
        pass
    pass

def main():
    bm = BitMonitor()
    bm.run()
    pass

if __name__=='__main__':
    main()
