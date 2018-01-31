#!/bin/sh
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.6.3_amd64.deb
sudo apt-get install -y adduser libfontconfig
sudo dpkg -i grafana_4.6.3_amd64.deb
sudo apt-get install influxdb
sudo service grafana-server start
sudo update-rc.d grafana-server defaults
sudo chown -R root:grafana ./grafana/grafana.ini
sudo chown -R grafana:grafana ./grafana/grafana.db
sudo cp ./grafana/grafana.ini /etc/grafana/grafana.ini
sudo cp ./grafana/grafana.db /var/lib/grafana/grafana.db
sudo service grafana-server restart
sudo apt-get install python2.7
sudo apt-get install python-pip
sudo pip install influxdb
