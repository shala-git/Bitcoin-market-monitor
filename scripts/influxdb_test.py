#!/usr/bin/env python
from fixerio import Fixerio
import sys
sys.path.append("..")
from scripts

def main():
    
    fxrio = Fixerio()
    print(fxrio.latest(base='CNY'))
    pass

if __name__=='__main__':
    main()

