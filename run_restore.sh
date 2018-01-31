#!/bin/sh
sudo service influxdb stop
sudo influxd restore -database grafana -datadir /var/lib/influxdb/data/ ./influxdb
sudo service influxdb start
