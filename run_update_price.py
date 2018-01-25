#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import sys,os
import time
import traceback

import config
from logger_service import logger
from api_price_bithumb import BithumbPrice
from api_price_zb import ZBPrice

class PriceUpdater(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()

        pass

    def _load_agent(self):
        # add agent btcchina
        agent_zb = ZBPrice()
        self._agents.append(agent_zb)
        agent_bithumb = BithumbPrice()
        self._agents.append(agent_bithumb)
        # add other transaction agent
        # ...
        pass

    def update_price(self):
        #raise NameError('Exception Raise')
        logger.info('task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            logger.info('agent "%s"' % (agent.name))

            # get price
            logger.info('1. get price')
            ret = agent.query()
            if not ret:
                logger.error('query failed, skip "%s"' % (agent.name))
                continue

        pass

    def run(self):
        while True:
            try:
                self.update_price()
            except Exception, e:
                logger.error(traceback.format_exc())
                logger.error(str(e))
            time.sleep(config.PRICE_UPDATE_INTERVAL)
            pass
        pass
    pass

def main():
    updater = PriceUpdater()
    updater.run()
    pass

if __name__=='__main__':
    main()

