#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-11
import sys,os
import time
import traceback
from settings import config
from priceupdate import *
#from lib.logger_service import logger
from exchange import *

class BitMonitor(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()
        
        self.exchange_data = {}
        self.exchange_client = Exchange()
        ex_td = threading.Thread(target=self.update_exchange)
        self.isRun = True
        ex_td.start()

        pass

    def _load_agent(self):
        # add agent
        #agent_priceupdater = PriceUpdater()
        #self._agents.append(agent_priceupdater)

        # add other transaction agent
        # ...
        pass

    def update_price(self):
        #raise NameError('Exception Raise')
        #logger.info('Price module task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            #logger.info('agent "%s"' % (agent.name))

            # get price
            #logger.info('Get price')
            #ret = agent.query()
            ret = True
            if not ret:
                #logger.error('query failed, skip "%s"' % (agent.name))
                continue
        pass

    def exchange_callback(self, dic):
        self.exchange_data = dic
        print (self.exchange_data)
        
    def update_exchange(self):
        while self.isRun:
            self.exchange_client.query(self.exchange_callback)
            time.sleep(5)

    def run(self):
        while True:
            try:
                self.update_price()
            except (Exception):
                pass
                #logger.error(traceback.format_exc())
                #logger.error(str(e))
            time.sleep(3)
            pass
        pass
    pass

def main():
    bm = BitMonitor()
    bm.run()
    pass

if __name__=='__main__':
    main()
