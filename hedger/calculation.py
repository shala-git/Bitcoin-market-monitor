#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import traceback
import time
import math
import marketConfig

class Hedger(object):
    """演算脚本"""
    def __init__(self, arg):
        for market_index in marketConfig.MARKET_NAME:
            self.market_dict = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
        print self.market_dict
    def _buy(self):
    def _sell(self):
    def _move(self):
