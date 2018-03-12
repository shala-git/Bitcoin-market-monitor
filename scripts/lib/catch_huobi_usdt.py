#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-03-07

# systemic class
import urllib.request
import urllib.parse
import urllib
import requests
import sys
from settings import arbitrage_config
import json

class CatchUSDT(object):
    '''
    '''

    def __init__(self):
        #
        self.exchange = {}
        self.price_data = []
        pass
    
    def _run(self):
        try:
            textmod ={'coinId':1, 'tradeType':1,'currentPage':1,'payWay':'','country':'','merchant':1,'online':1,'range':0}
            textmod = urllib.parse.urlencode(textmod)
            url = '%s%s%s' % (arbitrage_config.HUOBI_BTC_CNY_URL,'?',textmod)
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req, timeout=10)
            res = response.read()
            data = json.loads(res)

            price_list = data['data']
            self.price_data = []
            for price in price_list:
                if price['tradeCount'] > 0.5:
                    #print (price['fixedPrice'])
                    self.price_data.append(price['fixedPrice'])
            #print(min(self.price_data))
        except urllib.request.HTTPError as e:
            pass
        except urllib.request.URLError as e:
            pass
        return self.price_data

catchusdt = CatchUSDT()
def main():
    catchusdt._run()

    pass

if __name__ == '__main__':
    main()
