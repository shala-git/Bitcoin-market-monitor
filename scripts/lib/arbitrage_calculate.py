#!/usr/bin/env python
#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# author: jahyeonbeak@gmail.com
# date:   2018-03-07

# systemic class
import os
import sys
import time
sys.path.append("..")
from settings import arbitrage_config
from lib.catch_huobi_usdt import catchusdt

class ArbitrageCalculate(object):
    '''
    '''

    def __init__(self):
        #
        self.exchange = {}
        self.price_data = {}
        self.arbitrage_list = []
        pass
    
    def set_exchange(self, data):
        self.exchange = data
        pass

    def set_price_data(self, platform, data):
        self.price_data[platform] = data
        #print (data)

    def run_calculate(self):
        try:
            self.arbitrage_list = []
            for source in arbitrage_config.ARBITRAGE_SOURCE:
                buy_fee = arbitrage_config.TRADE_FEE[source] #买入费率
                #买入币价格
                if source.find('huobi') > -1:
                    buy_price = min(catchusdt._run()) # 买入价格
                else:
                    buy_price = float(self.price_data[source][0]['fields']['buy_usd']) # 买入价格
                print ('买入价格 每个 %s 人民币'%buy_price)
                
                transfer_fee = arbitrage_config.TRANSFER_FEE[source] #转币费率
                buy_one_final_amount = (buy_price - (buy_price * buy_fee)) / buy_price # 最终买入量
                transefr_final_amount = buy_one_final_amount - transfer_fee # 最终转币后剩余量
                for target in arbitrage_config.ARBITRAGE_TARGET:
                    target_market = None
                    if target.find('bithumb') > -1:
                        target_market = 'bithumb'
                    else:
                        target_market = target
                    if target_market == 'bithumb':
                        #卖出价格
                        sell_price = float(self.price_data[target_market][0]['fields']['sell_krw']) #得到韩币卖出价格
                        print ('卖出价格 每个 %s 韩币'%sell_price)
                        sell_fee = arbitrage_config.TRADE_FEE[target] # 得到卖出费率
                        final_price_amount = (transefr_final_amount - (transefr_final_amount * sell_fee)) * sell_price # 最终卖出金额
                        print ('最终卖出价格 买入1个btc后除去交易费率和转币费率和卖出费率后得到 %s 韩币'%final_price_amount)
                        final_exchange = int(self.exchange['CNY']['KRW']) #韩币/RMB 汇率
                        print ('韩币/RMB 汇率 %s'%final_exchange)
                        final_margin = float('%.2f' % (((final_price_amount / (final_exchange + 0) - buy_price) / (buy_price))*100 )) #利润比例
                        final_margin_1 = float('%.2f' % (((final_price_amount / (final_exchange + 1) - buy_price) / (buy_price))*100 )) #利润比例
                        final_margin_2 = float('%.2f' % (((final_price_amount / (final_exchange + 2) - buy_price) / (buy_price))*100 )) #利润比例
                        final_margin_3 = float('%.2f' % (((final_price_amount / (final_exchange + 3) - buy_price) / (buy_price))*100 )) #利润比例
                        final_margin_4 = float('%.2f' % (((final_price_amount / (final_exchange + 4) - buy_price) / (buy_price))*100 )) #利润比例
                        final_margin_5 = float('%.2f' % (((final_price_amount / (final_exchange + 5) - buy_price) / (buy_price))*100 )) #利润比例
                        print ("目标市场 : %s, final margin : %s, 汇率+1 final margin : %s, 汇率+2 final margin : %s, 汇率+3 final margin : %s, 汇率+4 final margin : %s, 汇率+5 final margin : %s"%(target, final_margin, final_margin_1, final_margin_2,final_margin_3,final_margin_4,final_margin_5))
                        arbitrage_source = {
                            "measurement": 'arbitrage',
                            "tags": {
                                "market": ('%s-%s')%(source,target),
                            },
                            "fields": {
                            "exchange": final_exchange,
                            "margin+0": final_margin,
                            "margin+1": final_margin_1,
                            "margin+2": final_margin_2,
                            "margin+3": final_margin_3,
                            "margin+4": final_margin_4,
                            "margin+5": final_margin_5
                            #"vol_usd":float(source['vol'])
                            }
                        }
                        self.arbitrage_list.append(arbitrage_source)
                        
                    else:
                        sell_price = float(self.price_data[target_market][0]['fields']['sell_usd'])
                        sell_fee = arbitrage_config.TRADE_FEE[target]
                        final_price_amount = (transefr_final_amount - (transefr_final_amount * sell_fee)) * sell_price
                        final_margin = (final_price_amount - buy_price) / buy_price
                        return None                    
                    #print ("target is : %s, buy one final amount : %s, transfer final amount : %s, sell price amount : %s, final margin : %s"%(target, buy_one_final_amount,transefr_final_amount,final_price_amount,final_margin))
                return self.arbitrage_list
        except Exception as e:
            print (e)
            return None
            pass
        


# Create One Instance of Logger Class
calculate = ArbitrageCalculate()
def main():
    print(catchusdt._run())
    ddd = [{'measurement': 'bithumb', 'tags': {'coin': 'BTC', 'base': 'KRW'}, 'fields': {'buy_usd': 10792.542959999999, 'buy_cny': 68535.8928, 'buy_krw': 11736000.0, 'high_usd': 11528.230959999999, 'high_cny': 73207.7328, 'high_krw': 12536000.0, 'last_usd': 10794.382179999999, 'last_cny': 68547.5724, 'last_krw': 11738000.0, 'low_usd': 10546.08748, 'low_cny': 66970.8264, 'low_krw': 11468000.0, 'sell_usd': 10793.46257, 'sell_cny': 68541.7326, 'sell_krw': 11737000.0}}]
    aaa = [{'measurement': 'huobi', 'tags': {'coin': 'btcusdt', 'base': 'USD'}, 'fields': {'buy_usd': 10576.8, 'buy_cny': 67165.85303999999, 'high_usd': 72040.089308, 'last_usd': 10580.2, 'last_cny': 67187.44406000001, 'low_usd': 10529.81, 'low_cny': 66867.452443, 'sell_usd': 10580.15, 'sell_cny': 67187.12654499999}}]
    ccc = {'KRW': {'CNY': 0.0058398, 'USD': 0.00091961}, 'USD': {'CNY': 6.3503, 'KRW': 1087.4}, 'CNY': {'KRW': 171.24, 'USD': 0.15747}}
    calculate.set_exchange(ccc)
    calculate.set_price_data('bithumb', ddd)
    calculate.set_price_data('huobi', aaa)
    print(calculate.run_calculate())
    
    pass

if __name__ == '__main__':
    main()
