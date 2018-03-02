#!/usr/bin/env python
from fixerio import Fixerio
import json

class Exchange(object):
    def __init__(self):#, influxdb_client):
        self.fxrio = Fixerio()
        self.exchange_data = {}
        #self.client=influxdb_client
        #self._request_timeout = int(config.REQUEST_TIMEOUT)
        #self._price = 0.0
        self._name = 'Exchange'
        self.baselist = {'CNY','USD','KRW'}
        self.exchange_data = {}
        for index in self.baselist:
            self.exchange_data[index] = None

    @property
    def name(self):
        return self._name

    def query(self, callback_func=None):
        for index in self.baselist:
            res = self.fxrio.latest(base=index)
            self.parse_exchange(index,res)
        if callback_func is not None:
            callback_func(self.exchange_data)
            
    def parse_exchange(self, base, data):
        #data = json.loads(jsondata)
        data_dict = {}
        for key in data['rates']:
            if key in self.baselist:
                data_dict[key] = data['rates'][key]
        self.exchange_data[base] = data_dict      
        
def main():
    ex = Exchange()
    ex.query(callbacktest)

def callbacktest(dic):
    print ('%s - callback '%dic)

if __name__=='__main__':
    main()

