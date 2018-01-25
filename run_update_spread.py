#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: justinli.ljt@gmail.com
# date:   2013-11-05

import sys,os
import time
import traceback

import config
from logger_service import logger
from price_spread import SpreadPrice

class SpreadUpdater(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()

        pass

    def _load_agent(self):
        # add agent btcchina
        agent = SpreadPrice()
        self._agents.append(agent)
        # add other transaction agent
        # ...
        pass

    def update_spread(self):
        #raise NameError('Exception Raise')
        logger.info('task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            logger.info('agent "%s"' % (agent.name))

            # get price
            logger.info('1. get price')
            ret = agent.query()
            

        pass

    def run(self):
        while True:
            try:
                self.update_spread()
            except Exception, e:
                logger.error(traceback.format_exc())
                logger.error(str(e))
            time.sleep(config.PRICE_UPDATE_INTERVAL)
            pass
        pass
    pass

def main():
    updater = SpreadUpdater()
    updater.run()
    pass

if __name__=='__main__':
    main()

