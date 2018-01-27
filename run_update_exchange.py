#!/usr/bin/env python
import sys,os
import time
import traceback

import config
from lib.logger_service import logger
from lib.api_exchange import Exchange

class ExchangeUpdater(object):
    '''
    '''
    def __init__(self):
        self._agents = []
        self._load_agent()

        pass

    def _load_agent(self):
        # add agent btcchina
        agent = Exchange()
        self._agents.append(agent)

        # add other transaction agent
        # ...
        pass

    def update_exchange(self):
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
                self.update_exchange()
            except Exception, e:
                logger.error(traceback.format_exc())
                logger.error(str(e))
            time.sleep(config.EXCHANGE_UPDATE_INTERVAL)
            pass
        pass
    pass

def main():
    updater = ExchangeUpdater()
    updater.run()
    pass

if __name__=='__main__':
    main()

