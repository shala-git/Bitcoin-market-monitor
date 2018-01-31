#!/bin/sh
service influxdb restart
service grafana-server restart
nohup python run_update_exchange.py 1>/dev/null 2>&1 &
nohup python run_update_price.py 1>/dev/null 2>&1 &
nohup python run_update_spread.py 1>/dev/null 2>&1 &
