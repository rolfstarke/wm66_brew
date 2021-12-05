import sys
import adafruit_dht
import time
from influxdb import client as influxdb
import datetime

humidity, temperature = adafruit_dht.read(22, 4)

if humidity is not None and temperature is not None:
	influxHost = 'localhost'
	influxPort = '8086'
	influxUser = 'admin'
	influxPasswd = '12TUDdd.47'
	influxdbName = 'dhtTest'

	influx_metric = [{
		'measurement': 'TemperatureSensor',
		'time': datetime.datetime.now(),
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