#!/bin/sh
influxd backup -database grafana ./influxdb
cp /var/lib/grafana/grafana.db ./
cp /etc/grafana/grafana.ini ./
