import sys
import Adafruit_DHT
import time
from influxdb import client as influxdb
import datetime
from pytz import timezone

humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, 4)

if humidity is not None and temperature is not None:
        influxHost = 'localhost'
        influxPort = '8086'
        influxUser = 'grafana'
        influxPasswd = 'password'
        influxdbName = 'dhtTest'

        influx_metric = [{
                'measurement': 'TemperatureSensor',
                'time': datetime.datetime.now(timezone('CET')),
                'fields': {
                        'temperature': temperature,
                        'humidity': humidity
                }
        }]

        try:
                db = influxdb.InfluxDBClient(influxHost, influxPort, influxUser, influxPasswd, influxdbName)
                db.write_points(influx_metric)
        finally:
                db.close()
