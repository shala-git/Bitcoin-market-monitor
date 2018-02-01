#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-01-11
import eventlet
import sys,os
sys.path.append("..")
import time
import traceback
import config
from AccountBalance import *

class AccountDataUpdate(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()

        pass

    def _load_agent(self):
        # add agent btcchina
        agent_balance = AccountBalance()
        self._agents.append(agent_balance)

        # add other transaction agent
        # ...
        pass

    def update_price(self):
        #raise NameError('Exception Raise')
        logger.info('Price module task start - agents total %d' % (len(self._agents)))
        for agent in self._agents:
            logger.info('agent "%s"' % (agent.name))

            # get price
            logger.info('Get data')
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
            time.sleep(config.BALANCE_UPDATE_INTERVAL)
            pass
        pass
    pass

def main():
    updater = AccountDataUpdate()
    updater.run()
    pass

if __name__=='__main__':
    main()
